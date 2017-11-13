#!_PYTHONLOC
# -*- coding: cp1252 -*-
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import string
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import *


def DisplayError(message, display_header = 0):
        if display_header:
                PrintHeader('Advanced Search')
                PrintNavbar('adv_search_results', 0, 0, 0, 0)
        print '<h2>Error: %s</h2>' % message
	PrintTrailer('adv_search_results', 0, 0)
        sys.exit(0)

class advanced_search:
        def __init__(self):
                user = User()
                user.load()
                user.load_moderator_flag()
                self.user = user
                self.form = {}
                self.start = 0
                self.search_type = ''
                self.order_by = ''
        	self.dbases = []
        	self.term_list = []
        	self.conjunction_list = []
        	self.join_list = []
        	self.operator_list = []
        	self.terms = ''
        	self.query = ''
        	self.records = []
        	self.num = 0

        def parse_parameters(self):
                sys.stderr = sys.stdout
                raw_form = cgi.FieldStorage()

                try:
                        # Strip leading and trailing spaces if the user's preferences call for it;
                        # move the parameters to a new dictionary, 'form'
                        for key in raw_form.keys():
                                value = raw_form[key].value
                                if not self.user.keep_spaces_in_searches:
                                        value = string.strip(value)
                                if value:
                                        self.form[key] = value

                        self.start = int(self.form['START'])
                        self.search_type = self.form['TYPE']
                        if self.search_type not in ('Author', 'Title', 'Publication'):
                                raise
                        self.order_by = self.formatEntry(self.form['ORDERBY'])
                except:
                        DisplayError('Invalid Search parameters', 1)

        def set_search_type(self):
                if self.search_type == 'Author':
                        self.SQLterm = self.MakeAuthorSQLterm
                        self.executeQuery = self.executeAuthorQuery
                elif self.search_type == 'Title':
                        self.SQLterm = self.MakeTitleSQLterm
                        self.executeQuery = self.executeTitleQuery
                elif self.search_type == 'Publication':
                        self.SQLterm = self.MakePubSQLterm
                        self.executeQuery = self.executePubQuery

        def ProcessSort(self):
                self.sort = self.formatEntry(self.order_by)
                if self.search_type == 'Publication' and self.sort not in ('pub_title', 'pub_ctype',
                                                         'pub_tag', 'pub_year',
                                                         'pub_isbn', 'pub_price',
                                                         'pub_pages', 'pub_ptype',
                                                         'pub_frontimage'):
                        DisplayError("Unknown sort field: %s" % sort)
                elif self.search_type == 'Author' and self.sort not in ('author_canonical',
                                                            'author_lastname',
                                                            'author_legalname',
                                                            'author_birthplace',
                                                            'author_birthdate',
                                                            'author_deathdate'):
                        DisplayError("Unknown sort field: %s" % sort)
                elif self.search_type == 'Title' and self.sort not in ('title_title',
                                                            'title_copyright',
                                                            'title_ttype'):
                        DisplayError("Unknown sort field: %s" % sort)
                if self.sort == 'pub_pages':
                        self.sort = 'CAST(pub_pages as SIGNED)'
                elif self.sort == 'pub_price':
                        self.sort = "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_price,' ',''),'$',''),'C',''),'A',''),'M',''),'D',''),'£',''),'F',''),'€',''),'z&#322;',''),'NZ',''),'t',''),'ƒ','')*100"
                if self.search_type == 'Author':
                        if self.sort != 'author_canonical':
                                self.sort += ', author_canonical'
                elif self.search_type == 'Title':
                        if self.sort != 'title_title':
                                self.sort += ', title_title'
                        if self.sort != 'title_copyright':
                                self.sort += ', title_copyright'
                elif self.search_type == 'Publication':
                        if self.sort != 'pub_title':
                                self.sort += ', pub_title'
                        if self.sort != 'pub_year':
                                self.sort += ', pub_year'

        def ProcessTerms(self):
                # Special case for "Show All Titles"
                if (self.search_type == 'Title') and self.form.has_key('exact'):
                        self.ProcessTerm(self.form.get('exact'), 'exact', 'exact')

                if self.form.has_key('TERM_1'):
                        self.ProcessTerm(self.form.get('TERM_1'), self.form.get('USE_1'), self.form.get('OPERATOR_1'))
                if not self.term_list:
                        DisplayError("No search data entered")

                # If we have term 2, only include the conjunction if there was also
                # a term 1 (otherwise, term 2 is the first term, and the conjunction
                # does not apply).
                if self.form.has_key('TERM_1') and self.form.has_key('CONJUNCTION_1') and self.form.has_key('TERM_2'):
                        self.ProcessConjunction(self.form.get('CONJUNCTION_1'))

                if self.form.has_key('TERM_2'):
                        self.ProcessTerm(self.form.get('TERM_2'), self.form.get('USE_2'), self.form.get('OPERATOR_2'))

                # If we have term 3, only include the conjunction if there was also a preceding term
                if (self.form.has_key('TERM_1') or self.form.has_key('TERM_2')) and self.form.has_key('CONJUNCTION_2') and self.form.has_key('TERM_3'):
                        self.ProcessConjunction(self.form.get('CONJUNCTION_2'))

                if self.form.has_key('TERM_3'):
                        self.ProcessTerm(self.form.get('TERM_3'), self.form.get('USE_3'), self.form.get('OPERATOR_3'))

        def ProcessTerm(self, term, use, operator):
                term = normalizeInput(term)
                if not term:
                        return
                raw_entry = term
                entry = self.formatEntry(term)
                self.validateTerm(use, entry)

                self.checkValidOperator(operator)
                self.operator_list.append(operator)

                if use == 'pub_isbn':
                        # Search for possible ISBN variations
                        isbn_values = isbnVariations(entry)
                        isbn_count = 0
                        sql_value = '('
                        for isbn_value in isbn_values:
                                padded_entry = self.padEntry(operator, isbn_value)
                                if isbn_count:
                                        if operator in ('notexact', 'notcontains'):
                                                sql_value += ' and '
                                        else:
                                                sql_value += ' or '
                                sql_value += "pubs.pub_isbn %s" % padded_entry
                                isbn_count += 1
                        sql_value += ")"
                else:
                        sql_value = self.padEntry(operator, entry)

                (new_term, new_dbases, new_joins) = self.SQLterm(use, entry, sql_value)
                self.term_list.append(new_term)
                self.mergeTableInfoLists(self.dbases, new_dbases)

                for join in new_joins:
                        if join not in self.join_list:
                                self.join_list.append(join)

        def checkValidOperator(self, operator):
                operators = ('exact', 'notexact', 'contains', 'notcontains', 'starts_with', 'ends_with')
                if operator not in operators:
                        message = 'Valid operators are: '
                        for operator in operators:
                                message += operator
                                message += ', '
                        print '<h2>%s</h2>' % (message[:-2])
                        PrintTrailer('adv_search_results', 0, 0)
                        sys.exit(0)

        def padEntry(self, operator, entry):
                if operator == 'exact':
                        padded_entry = "like '%s'" % entry
                elif operator == 'notexact':
                        padded_entry = "not like '%s'" % entry
                elif operator == 'contains':
                        padded_entry = "like '%%%s%%'" % entry
                elif operator == 'notcontains':
                        padded_entry = "not like '%%%s%%'" % entry
                elif operator == 'starts_with':
                        padded_entry = "like '%s%%'" % entry
                elif operator == 'ends_with':
                        padded_entry = "like '%%%s'" % entry
                else:
                        print '<h2>An unexpected error has occurred. Please post the URL of this Web page on the Moderator noticeboard.</h2>'
                        PrintTrailer('adv_search_results', 0, 0)
                        sys.exit(0)
                return padded_entry

        def validateTerm(self, field, value):
                if field == 'month':
                        (year, month, error) = validateMonth(value)
                        if error:
                                DisplayError(error)
                elif field == 'title_ttype':
                        ttypes = ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'COVERART', 'EDITOR', 'ESSAY', 'INTERIORART', 'INTERVIEW', 'NONFICTION', 'NOVEL', 'OMNIBUS', 'POEM', 'REVIEW', 'SERIAL', 'SHORTFICTION')
                        if value.upper() not in ttypes:
                                message = 'Valid title types are: '
                                for ttype in ttypes:
                                        message += ttype
                                        message += ", "
                                DisplayError(message[:-2])
                elif field in ('title_graphic', 'title_non_genre', 'title_jvn', 'title_nvz'):
                        if value.lower() not in ('yes', 'no'):
                                DisplayError('Valid Yes/No value required')
                elif field == 'pub_ctype':
                        ttypes = ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'FANZINE', 'MAGAZINE', 'NONFICTION', 'NOVEL', 'OMNIBUS')
                        if value.upper() not in ttypes:
                                message = 'Valid title types are: '
                                for ttype in ttypes:
                                        message += ttype
                                        message += ", "
                                DisplayError(message[:-2])
                elif field == 'pub_month':
                        (year, month, error) = validateMonth(value)
                        if error:
                                DisplayError(error)

        def mergeTableInfoLists(self, dest, src):
                for sti in src:
                        found = 0
                        for dti in dest:
                                if dti == sti:
                                        found = 1
                                        dti.mergeHints(sti)
                                        break
                        if not found:
                                dest.append(sti)

        def ProcessConjunction(self, raw_conjunction):
                self.checkValidConjunction(raw_conjunction)
                conjunction = self.formatEntry(raw_conjunction)
                self.conjunction_list.append(conjunction)

        def checkValidConjunction(self, value):
                conjunctions = ('AND', 'OR')
                if value not in conjunctions:
                        message = 'Valid conjunctions are: '
                        for op in conjunctions:
                                message += op
                                message += ', '
                        print '<h2>%s</h2>' % (message[:-2])
                        PrintTrailer('adv_search_results', 0, 0)
                        sys.exit(0)

        def formatEntry(self, value):
                value = db.escape_string(value)
                # Change asterisks to % because * is also a supported wildcard character
                value = string.replace(value, '*', '%')
                return value

        def MakeTerms(self):
                # If we have two conjunctions and only one of them is an OR,
                # group the adjoining terms and the OR together
                if (self.conjunction_list and (len(self.conjunction_list) == 2) and (self.conjunction_list[0] != self.conjunction_list[1])):
                        if (self.conjunction_list[0] == "OR"):
                                self.term_list[0] = "(" + self.term_list[0]
                                self.term_list[1] = self.term_list[1] + ")"
                        else:
                                self.term_list[1] = "(" + self.term_list[1]
                                self.term_list[2] = self.term_list[2] + ")"

                # Construct the clause of term(s).  We wrap this in parens to avoid
                # unintended interaction with the join clauses.
                o = 0
                self.terms = "("
                for term in self.term_list:
                        self.terms += term
                        if o < len(self.conjunction_list):
                                self.terms = self.terms + " " + self.conjunction_list[o] + " "
                                o = o + 1
                self.terms += ")"

                # Add the join clauses to the end
                for join in self.join_list:
                        self.terms = self.terms + " and " + join

        def executePubQuery(self):
                self.query = "select distinct pubs.* from "
                self.makeTableQuery()
                self.search()
                PrintPubsTable(self.records, 'adv_search', self.user, 100)

        def executeAuthorQuery(self):
                self.query = "select distinct authors.* from "
                self.makeTableQuery()
                self.search()
                PrintAuthorTable(self.records, 1, 100, self.user)
                if self.user.moderator:
                        self.PrintMergeButton()

        def executeTitleQuery(self):
                self.query = "select distinct titles.* from "
                self.makeTableQuery()
                self.search()
                PrintTitleTable(self.records, 1, 100, self.user)
                self.PrintMergeButton()

        def search(self):
                db.query(self.query)
                result = db.store_result()
                self.num = result.num_rows()

                if not self.num:
                        print "<h2>No records found</h2>"
                        PrintTrailer('adv_search_results', 0, 0)
                        sys.exit(0)

                record = result.fetch_row()
                while record:
                        self.records.append(record[0])
                        record = result.fetch_row()

        def makeTableQuery(self):
                first = 1
                for dbase in self.dbases:
                        tclause = dbase.tname
                        firstHint = 1
                        for hint in dbase.hints:
                                if firstHint:
                                        tclause += " " + hint
                                        firstHint = 0
                                else :
                                        tclause += ", " + hint
                        if first:
                                self.query += tclause
                                first = 0
                        else:
                                self.query += "," + tclause
                self.query += " where %s order by %s limit %d,%d" % (self.terms, self.sort, self.start, 101)

        def print_merges(self):
                if self.search_type == 'Author' and self.user.moderator:
                        self.print_help_merge('authors', 'av_merge')

                if self.search_type == 'Title':
                        self.print_help_merge('titles', 'tv_merge')

        def print_help_merge(self, record_type, script):
                print '<div id="HelpBox">'
                print '<b>Help on merging %s: </b>' % record_type
                print '<a href="http://%s/index.php/Editing:Merging_%s">Editing:Merging %s</a><p>' % (WIKILOC, record_type.title(), record_type.title())
                print '</div>'
                print '<form METHOD="POST" ACTION="/cgi-bin/edit/%s.cgi">' % script

        def PrintNextPage(self):
                if search.num < 101:
                        return
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % HTFAKE
                print '<p>'
                for key in self.form.keys():
                        if key == 'START':
                                key_value = self.start + 100
                        else:
                                key_value = cgi.escape(self.form[key], True)
                        print '<input NAME="%s" value="%s" type="HIDDEN">' % (key, key_value)
                print '<input TYPE="SUBMIT" VALUE="Next page (%d - %d)">' % (self.start+101, self.start+200)
                print '</form>'

        def PrintMergeButton(self):
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Merge Selected Records">'
                print '</form>'
                print '<hr>'

        def MakeTitleSQLterm(self, field, value, sql_value):

                # Set up default values
                joins = []
                dbases = [tableInfo('titles')]

                if field == 'title_title':
                        clause = "titles.title_title %s" % sql_value
                elif field == 'title_trans_title':
                        clause = "trans_titles.trans_title_title %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('trans_titles')]
                        joins = ['trans_titles.title_id=titles.title_id']
                elif field == 'title_copyright':
                        clause = "SUBSTRING(titles.title_copyright,1,4) %s" % sql_value
                elif field == 'month':
                        clause = "SUBSTRING(titles.title_copyright,1,7) %s" % sql_value
                elif field == 'title_ttype':
                        clause = "titles.title_ttype %s" % sql_value
                elif field in ('title_storylen', 'title_content', 'title_graphic', 'title_non_genre', 'title_jvn', 'title_nvz'):
                        clause = "titles.%s %s" % (field, sql_value)
                elif field in ('author_canonical', 'author_birthplace', 'author_birthdate', 'author_deathdate'):
                        clause = "authors.%s %s and canonical_author.ca_status=1" % (field, sql_value)
                        dbases = [tableInfo('titles'), tableInfo('authors'), tableInfo('canonical_author',['USE INDEX(authors)'])]
                        joins = ['authors.author_id=canonical_author.author_id', 'titles.title_id=canonical_author.title_id']
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('canonical_author'), tableInfo('webpages')]
                        joins = ['canonical_author.title_id=titles.title_id','canonical_author.author_id=webpages.author_id']
                elif field == 'series':
                        clause = "series.series_title %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('series')]
                        joins = ['series.series_id=titles.series_id']
                elif field == 'reviewee':
                        clause = "titles.title_ttype='REVIEW' AND ca1.ca_status=3"
                        dbases = [tableInfo("titles"),tableInfo("canonical_author ca1"),
                                  tableInfo("(select author_id from authors where author_canonical %s) a1" % sql_value)]
                        joins = ['titles.title_id=ca1.title_id','ca1.author_id=a1.author_id']
                elif field == 'interviewee':
                        clause = "titles.title_ttype='INTERVIEW' AND ca2.ca_status=2"
                        dbases = [tableInfo("titles"),tableInfo("canonical_author ca2"),
                                  tableInfo("(select author_id from authors where author_canonical %s) a2" % sql_value)]
                        joins = ['titles.title_id=ca2.title_id','ca2.author_id=a2.author_id']
                elif field == 'title_note':
                        clause = "n1.note_note %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('notes n1')]
                        joins = ['n1.note_id=titles.note_id']
                elif field == 'title_synopsis':
                        clause = "n2.note_note %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('notes n2')]
                        joins = ['n2.note_id=titles.title_synopsis']
                elif field == 'title_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('webpages')]
                        joins = ['webpages.title_id=titles.title_id']
                elif field == 'title_language':
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('languages')]
                        joins = ['languages.lang_id=titles.title_language']
                elif field == 'tag':
                        clause = "tags.tag_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('tags'), tableInfo('tag_mapping')]
                        joins = ['tag_mapping.title_id=titles.title_id','tags.tag_id=tag_mapping.tag_id']
                # "exact" is used by "Show All Titles"  and "view all titles by this pseudonym"
                elif field == 'exact':
                        clause = "canonical_author.author_id=%d and canonical_author.ca_status=1" % int(value)
                        dbases = [tableInfo('titles'), tableInfo('canonical_author')]
                        joins = ['titles.title_id=canonical_author.title_id']
                else:
                        DisplayError("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

        def MakeAuthorSQLterm(self, field, value, sql_value):

                # Set up default values
                joins = []
                dbases = [tableInfo('authors')]

                if field == 'author_canonical':
                        clause = "authors.author_canonical %s" % sql_value
                elif field == 'author_trans_name':
                        clause = "trans_authors.trans_author_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('trans_authors')]
                        joins = ['trans_authors.author_id=authors.author_id']
                elif field == 'author_legalname':
                        clause = "authors.author_legalname %s" % sql_value
                elif field == 'author_trans_legalname':
                        clause = "trans_legal_names.trans_legal_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('trans_legal_names')]
                        joins = ['trans_legal_names.author_id=authors.author_id']
                elif field == 'author_lastname':
                        clause = "authors.author_lastname %s" % sql_value
                elif field == 'author_birthplace':
                        clause = "authors.author_birthplace %s" % sql_value
                elif field == 'author_birthdate':
                        clause = "authors.author_birthdate %s" % sql_value
                elif field == 'author_deathdate':
                        clause = "authors.author_deathdate %s" % sql_value
                elif field == 'author_language':
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('languages')]
                        joins = ['languages.lang_id=authors.author_language']
                elif field == 'author_pseudos':
                        clause = """authors.author_id in (SELECT pseudonyms.author_id from pseudonyms,
                                  authors a1 WHERE pseudonym = a1.author_id AND a1.author_canonical %s)""" % sql_value
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('webpages')]
                        joins = ['webpages.author_id=authors.author_id']
                elif field == 'author_email':
                        clause = "emails.email_address %s" % sql_value
                        dbases = [tableInfo('authors'), tableInfo('emails')]
                        joins = ['emails.author_id=authors.author_id']
                elif field == 'author_note':
                        clause = "authors.author_note %s" % sql_value
                else:
                        DisplayError("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

        def MakePubSQLterm(self, field, value, sql_value):

                # Set up default values
                joins = []
                dbases = [tableInfo('pubs')]

                if field == 'pub_title':
                        clause = "pubs.pub_title %s" % sql_value
                elif field == 'pub_trans_title':
                        clause = "trans_pubs.trans_pub_title %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_pubs')]
                        joins = ['trans_pubs.pub_id=pubs.pub_id']
                elif field == 'pub_tag':
                        clause = "pubs.pub_tag %s" % sql_value
                elif field == 'pub_year':
                        clause = "SUBSTRING(pubs.pub_year,1,4) %s" % sql_value
                elif field == 'pub_month':
                        clause = "SUBSTRING(pubs.pub_year,1,7) %s" % sql_value
                elif field == 'pub_publisher':
                        clause = "publishers.publisher_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('publishers')]
                        joins = ['pubs.publisher_id=publishers.publisher_id']
                elif field == 'trans_publisher':
                        clause = "trans_publisher.trans_publisher_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_publisher')]
                        joins = ['trans_publisher.publisher_id=pubs.publisher_id']
                elif field == 'pub_series':
                        clause = "pub_series.pub_series_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_series')]
                        joins = ['pubs.pub_series_id=pub_series.pub_series_id']
                elif field == 'trans_pub_series':
                        clause = "trans_pub_series.trans_pub_series_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_pub_series')]
                        joins = ['trans_pub_series.pub_series_id=pubs.pub_series_id']
                elif field == 'pub_isbn':
                        # ISBNs are a special case. The whole clause was pre-built in ProcessTerm
                        clause = sql_value
                elif field == 'pub_ptype':
                        clause = "pubs.pub_ptype %s" % sql_value
                elif field in ('author_canonical', 'author_birthplace', 'author_birthdate', 'author_deathdate'):
                        clause = "authors.%s %s" % (field, sql_value)
                        dbases = [tableInfo('pubs'), tableInfo('authors'), tableInfo('pub_authors',['USE INDEX(author_id)'])]
                        joins = ['authors.author_id=pub_authors.author_id', 'pubs.pub_id=pub_authors.pub_id']
                elif field == 'author_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_authors'), tableInfo('webpages')]
                        joins = ['pub_authors.pub_id=pubs.pub_id','pub_authors.author_id=webpages.author_id']
                elif field == 'pub_price':
                        clause = "pubs.pub_price %s" % sql_value
                elif field == 'pub_pages':
                        clause = "pubs.pub_pages %s" % sql_value
                elif field == 'pub_coverart':
                        clause = "titles.title_ttype='COVERART' and authors.author_canonical %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_content'), tableInfo('canonical_author'), tableInfo('titles'), tableInfo('authors')]
                        joins = ['pubs.pub_id=pub_content.pub_id', 'pub_content.title_id=canonical_author.title_id',
                                 'canonical_author.title_id=titles.title_id', 'canonical_author.author_id=authors.author_id']
                elif field == 'pub_note':
                        clause = "notes.note_note %s" % sql_value
                        # dbases = [tableInfo('pubs',['USE INDEX(note_id)']), tableInfo('notes',['IGNORE INDEX (PRIMARY)'])]
                        dbases = [tableInfo('pubs'), tableInfo('notes')]
                        joins = ['pubs.note_id = notes.note_id']
                elif field == 'pub_verifier':
                        clause = "mw_user.user_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('mw_user'), tableInfo('primary_verifications')]
                        joins = ['pubs.pub_id = primary_verifications.pub_id',
                                 'primary_verifications.user_id = mw_user.user_id']
                elif field == 'pub_frontimage':
                        clause = "pub_frontimage %s" % sql_value
                elif field == 'pub_ctype':
                        clause = "pubs.pub_ctype %s" % sql_value
                else:
                        DisplayError("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

class tableInfo:
	def __init__(self, tname='', hints=None):
		self.tname = tname
		if hints == None:
			self.hints = []
		else:
			self.hints = hints

	def __cmp__(self, ti):
		if (self.tname == ti.tname):
			return 0
		if (self.tname < ti.tiname):
			return -1
		return 1

	def __eq__(self, ti):
		return self.tname == ti.tname

        def mergeHints(self, other):
            for hint in other.hints:
                if not hint in self.hints:
                    self.hints.append(hint)
            return self

if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################

        search = advanced_search()
        search.parse_parameters()

	PrintHeader("Advanced %s Search" % search.search_type)
	PrintNavbar('adv_search_results', 0, 0, 0, 0)

        search.set_search_type()

        search.ProcessTerms()

        search.ProcessSort()

        search.print_merges()

        search.MakeTerms()

        search.executeQuery()

        search.PrintNextPage()

	PrintTrailer('adv_search_results', 0, 0)
