#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2019   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 319 $
#     Date: $Date: 2019-01-13 20:23:22 -0500 (Sun, 13 Jan 2019) $

import cgi
import sys
import string
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import *

class AdvancedSearch:
        def __init__ (self, search_type, selector_id):
                self.search_type = search_type
                self.selector_id = selector_id
                self.max_term = 5
                self.selection = {}
                self.sort = {}
                self.message = {}

                self.selection['Award'] = (('award_year', 'Award Year'),
                                           ('award_level', 'Award Level'),
                                           ('title_title', 'Title (for title-based awards)'),
                                           ('title_ttype', 'Title Type'),
                                           ('award_cat_name', 'Award Category'),
                                           ('award_type_short_name', 'Award Type Short Name'),
                                           ('award_type_full_name', 'Award Type Full Name'),
                                           ('note', 'Notes')
                                           )
                self.sort['Award'] = (('award_year', 'Award Year'),
                                      ('award_level', 'Award Level')
                                      )

                self.selection['Award Category'] = (('award_cat_name', 'Award Category Name'),
                                           ('award_type_short_name', 'Parent Award Type Short Name'),
                                           ('award_type_full_name', 'Parent Award Type Full Name'),
                                           ('award_cat_order', 'Award Category Order'),
                                           ('note', 'Notes'),
                                           ('webpage', 'Webpage')
                                           )
                self.sort['Award Category'] = (('award_cat_name', 'Award Category Name'),
                                      ('award_cat_order', 'Award Category Order')
                                      )

                self.selection['Award Type'] = (('award_type_short_name', 'Award Type Name (Short)'),
                                           ('award_type_name', 'Award Type Name (Full)'),
                                           ('award_type_for', 'Awarded For'),
                                           ('award_type_by', 'Awarded By'),
                                           ('award_type_poll', 'Poll'),
                                           ('award_type_non_genre', 'Non-Genre'),
                                           ('note', 'Notes'),
                                           ('webpage', 'Webpage')
                                           )
                self.sort['Award Type'] = (('award_type_short_name', 'Short Award Type Name'),
                                      ('award_type_name', 'Full Award Type Name'),
                                      ('award_type_for', 'Awarded For'),
                                      ('award_type_by', 'Awarded By'),
                                      ('award_type_poll', 'Poll'),
                                      ('award_type_non_genre', 'Non-Genre')
                                      )

                self.selection['Publication Series'] = (('pub_series_name', 'Publication Series Name'),
                                           ('trans_pub_series_name', 'Transliterated Publication Series Name'),
                                           ('pub_series_note', 'Notes'),
                                           ('pub_series_webpage', 'Webpage')
                                           )
                self.sort['Publication Series'] = (('pub_series_name', 'Publication Series Name'),
                                      )

                self.selection['Publisher'] = (('publisher_name', 'Publisher Name'),
                                           ('trans_publisher_name', 'Transliterated Publisher Name'),
                                           ('publisher_note', 'Notes'),
                                           ('publisher_webpage', 'Webpage')
                                           )
                self.sort['Publisher'] = (('publisher_name', 'Publisher Name'),
                                      )

                self.selection['Series'] = (('series_title', 'Series Name'),
                                           ('trans_series_name', 'Transliterated Series Name'),
                                           ('parent_series_name', 'Parent Series Name'),
                                           ('parent_series_position', 'Position within Parent Series'),
                                           ('series_note', 'Notes'),
                                           ('series_webpage', 'Webpage')
                                           )
                self.sort['Series'] = (('series_title', 'Series Name'),
                                      )

                self.selection['Publication'] = (('pub_title', 'Title'),
                                           ('pub_trans_title', 'Transliterated Title'),
                                           ('pub_ctype', 'Publication Type'),
                                           ('author_canonical', 'Author\'s Name'),
                                           ('author_birthplace', 'Author\'s Birth Place'),
                                           ('author_birthdate', 'Author\'s Birthdate'),
                                           ('author_deathdate', 'Author\'s Deathdate'),
                                           ('author_webpage', 'Author\'s Webpage'),
                                           ('pub_year', 'Publication Year'),
                                           ('pub_month', 'Publication Month'),
                                           ('pub_publisher', 'Publisher'),
                                           ('trans_publisher', 'Transliterated Publisher'),
                                           ('pub_series', 'Publication Series'),
                                           ('trans_pub_series', 'Transliterated Publication Series'),
                                           ('title_language', 'Language of an Included Title (list)'),
                                           ('title_language_free', 'Language of an Included Title (free form)'),
                                           ('pub_isbn', 'ISBN'),
                                           ('pub_catalog', 'Catalog ID'),
                                           ('pub_price', 'Price'),
                                           ('pub_pages', 'Page Count'),
                                           ('pub_coverart', 'Cover Artist'),
                                           ('pub_ptype', 'Format'),
                                           ('pub_verifier', 'Primary Verifier'),
                                           ('pub_note', 'Notes'),
                                           ('pub_frontimage', 'Image URL')
                                           )
                self.sort['Publication'] = (('pub_title', 'Title'),
                                      ('pub_ctype', 'Publication Type'),
                                      ('pub_year', 'Date'),
                                      ('pub_isbn', 'ISBN'),
                                      ('pub_catalog', 'Catalog ID'),
                                      ('pub_price', 'Price'),
                                      ('pub_pages', 'Page Count'),
                                      ('pub_ptype', 'Format'),
                                      ('pub_frontimage', 'Image URL')
                                      )
                self.message['Publication'] = 'ISBN searches ignore dashes and search for both ISBN-10 and ISBN-13'

                self.selection['Title'] = (('title_title', 'Title'),
                                           ('title_trans_title', 'Transliterated Title'),
                                           ('author_canonical', 'Author\'s Name'),
                                           ('author_birthplace', 'Author\'s Birth Place'),
                                           ('author_birthdate', 'Author\'s Birthdate'),
                                           ('author_deathdate', 'Author\'s Deathdate'),
                                           ('author_webpage', 'Author\'s Webpage'),
                                           ('reviewee', 'Reviewed Author'),
                                           ('interviewee', 'Interviewed Author'),
                                           ('title_copyright', 'Title Year'),
                                           ('month', 'Title Month'),
                                           ('title_storylen', 'Length'),
                                           ('title_content', 'Content (omnibus only)'),
                                           ('title_ttype', 'Title Type'),
                                           ('title_note', 'Notes'),
                                           ('title_synopsis', 'Synopsis'),
                                           ('single_vote', 'Single User Vote'),
                                           ('series', 'Series'),
                                           ('title_language', 'Title Language (list)'),
                                           ('title_language_free', 'Title Language (free form)'),
                                           ('title_webpage', 'Title Webpage'),
                                           ('tag', 'Tag'),
                                           ('title_jvn', 'Juvenile'),
                                           ('title_nvz', 'Novelization'),
                                           ('title_non_genre', 'Non-Genre'),
                                           ('title_graphic', 'Graphic Format')
                                           )
                self.sort['Title'] = (('title_title', 'Title'),
                                      ('title_copyright', 'Date'),
                                      ('title_ttype', 'Title Type')
                                      )
                self.message['Title'] = 'When specifying multiple authors and/or multiple tags, OR is supported but AND is not'

                self.selection['Author'] = (('author_canonical', 'Canonical Name'),
                                           ('author_trans_name', 'Transliterated Name'),
                                           ('author_lastname', 'Directory Entry'),
                                           ('author_legalname', 'Legal Name'),
                                           ('author_trans_legalname', 'Transliterated Legal Name'),
                                           ('author_birthplace', 'Birth Place'),
                                           ('author_birthdate', 'Birthdate'),
                                           ('author_deathdate', 'Deathdate'),
                                           ('author_language', 'Working Language (list)'),
                                           ('author_language_free', 'Working Language (free form)'),
                                           ('author_webpage', 'Webpage'),
                                           ('author_email', 'E-mail'),
                                           ('author_pseudos', 'Alternate Name'),
                                           ('author_note', 'Note')
                                           )
                self.sort['Author'] = (('author_canonical', 'Canonical Name'),
                                      ('author_lastname', 'Directory Entry'),
                                      ('author_legalname', 'Legal Name'),
                                      ('author_birthplace', 'Birth Place'),
                                      ('author_birthdate', 'Birthdate'),
                                      ('author_deathdate', 'Deathdate')
                                      )

        def display_selection(self):
                PrintHeader('ISFDB Advanced %s Search' % self.search_type)
                script_name = 'adv_%s_search' % self.selector_id
                PrintNavbar(script_name, 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                self.print_full_header()
                self.print_search_table()
                PrintTrailer(script_name, 0, 0)

        def print_search_table(self):
                print '<h2>Selection Criteria</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                if self.search_type in self.message:
                        print '<ul>'
                        print '<li> %s' % self.message[self.search_type]
                        print '</ul>'
                for number in range(1, self.max_term + 1):
                        self.print_selectors(number)
                self.print_sort_by()
                self.print_submit_button(self.search_type)

        def print_invisible_drop_down_values(self):
                self.print_one_invisible_drop_down('Formats', FORMATS)
                self.print_one_invisible_drop_down('PubTypes', PUB_TYPES)
                self.print_one_invisible_drop_down('TitleTypes', ALL_TITLE_TYPES)
                self.print_one_invisible_drop_down('StoryLengths', STORYLEN_CODES)
                selectable_languages = sorted(list(LANGUAGES))
                if 'None' in selectable_languages:
                        selectable_languages.remove('None')
                self.print_one_invisible_drop_down('AllLanguages', selectable_languages)
                self.print_invisible_award_levels()

        def print_one_invisible_drop_down(self, name, values):
                print '<select NAME="%s" id="%s" class="nodisplay">' % (name, name)
                for value in values:
                        # Skip empty values, e.g. in STORYLEN_CODES
                        if value:
                                print '<option VALUE="%s">%s' % (value, value)
                print '</select>'

        def print_invisible_award_levels(self):
                from awardClass import awardShared
                print '<select NAME="AwardLevels" id="AwardLevels" class="nodisplay">'
                # First display regular award levels in the 1-70 range
                for award_level in range(1,71):
                        if award_level == 1:
                                displayed_value = '1 (Win)'
                        elif award_level == 9:
                                displayed_value = '9 (Nomination)'
                        else:
                                displayed_value = '%d' % award_level
                        print '<option VALUE="%s">%s</option>' % (displayed_value, displayed_value)
                # Next display special award levels in the 71-99 range
                special_levels = awardShared.SpecialAwards()
                for special_level in sorted(special_levels):
                        print '<option VALUE="%s (%s)">%s (%s)</option>' % (special_level, special_levels[special_level], special_level, special_levels[special_level])
                print '</select>'

        def print_full_header(self):
                print '<ul>'
                print '<li>A downloadable version of the ISFDB database is available <a href="http://%s/index.php/ISFDB_Downloads">here</a>' % WIKILOC
                print '<li>Supported wildcards: * and % match any number of characters, _ matches one character'
                print '</ul>'
                print '<hr>'

        def print_submit_button(self, record_type):
                print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="query">Get Results</button>'
                print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="count">Get Count</button>'
                print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
                print '<input NAME="TYPE" VALUE="%s" TYPE="HIDDEN">' % record_type
                print '</form>'

        def print_radio_selectors(self):
                print '<input TYPE="RADIO" NAME="C" VALUE="AND" CHECKED>AND'
                print '<input TYPE="RADIO" NAME="C" VALUE="OR">OR'

        def print_operators(self, record_type, number):
                print '<select NAME="O_%d" id="%s_operator_%d">' % (number, record_type, number)
                print '<option SELECTED VALUE="exact">is exactly'
                print '<option VALUE="notexact">is not exactly'
                print '<option VALUE="contains">contains'
                print '<option VALUE="notcontains">does not contain'
                print '<option VALUE="starts_with">starts with'
                print '<option VALUE="ends_with">ends with'
                print '</select>'

        def print_selectors(self, number):
                print '<p id="%s_selectors_%d">' % (self.selector_id, number)
                print '<select NAME="USE_%d" id="%s_%d">' % (number, self.selector_id, number)
                for value_display_pair in self.selection[self.search_type]:
                        print '<option VALUE="%s">%s' % (value_display_pair[0], value_display_pair[1])
                print '</select>'

                self.print_operators(self.selector_id, number)

                print '<input id="%sterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (self.selector_id, number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_sort_by(self):
                if self.search_type not in self.sort:
                        return
                # If there is only one way to sort the search results, hide the sort value
                if len(self.sort[self.search_type]) == 1:
                        print '<input NAME="ORDERBY" VALUE="%s" TYPE="HIDDEN">' % self.sort[self.search_type][0][0]
                        return

                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                for value_display_pair in self.sort[self.search_type]:
                        print '<option VALUE="%s">%s' % (value_display_pair[0], value_display_pair[1])
                print '</select>'


class AdvancedSearchResults:
        def __init__(self):
        	self.action = 'query'
        	self.conjunction = ''
        	self.dbases = []
                self.form = {}
                self.id_field = ''
        	self.join_list = []
        	self.max_term = 5
        	self.num = 0
        	self.operator_list = []
                self.order_by = ''
        	self.query = ''
        	self.records = []
                self.search_type = ''
                self.start = 0
        	self.term_list = []
        	self.terms = ''
        	self.wildcards = '%*_'

                user = User()
                user.load()
                user.load_moderator_flag()
                self.user = user

        def results(self):
                self.parse_parameters()
                PrintHeader("Advanced %s Search" % self.search_type)
                PrintNavbar('adv_search_results', 0, 0, 0, 0)
                self.set_search_type()
                self.process_terms()
                self.process_sort()
                self.print_merges()
                self.make_terms()
                self.execute_query()
                self.print_results()
                self.print_page_buttons()
                PrintTrailer('adv_search_results', 0, 0)

        def display_error(self, message, display_header = 0):
                if display_header:
                        PrintHeader('Advanced Search')
                        PrintNavbar('adv_search_results', 0, 0, 0, 0)
                self.display_message('Error: %s' % message)

        def display_message(self, message):
                print '<h2>%s</h2>' % message
                PrintTrailer('adv_search_results', 0, 0)
                sys.exit(0)

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
                        if self.start > 30000:
                                self.display_error('Advanced Search Is Currently Limited to 300 pages or 30,000 records', 1)
                        self.search_type = self.form['TYPE']
                        self.order_by = self.format_entry(self.form['ORDERBY'])
                        self.action = self.form.get('ACTION', 'query')
                        if self.action not in ('query', 'count'):
                                raise
                        self.conjunction = self.form.get('C', '')
                        # Legacy queries send CONJUNCTION_1 instead of C
                        if not self.conjunction:
                                self.conjunction = self.form.get('CONJUNCTION_1', '')
                        # "Exact" queries from "Show All Title" do not use a conjunction, so use a default value
                        if not self.conjunction:
                                self.conjunction = 'AND'
                        if self.conjunction not in ('AND', 'OR'):
                                raise
                except:
                        self.display_error('Invalid Advanced Search Parameters', 1)

        def set_search_type(self):
                if self.search_type == 'Author':
                        self.table = 'authors'
                        self.id_field = 'author_id'
                        self.SQLterm = self.make_author_SQL_term
                        self.print_results = self.print_author_results
                elif self.search_type == 'Title':
                        self.table = 'titles'
                        self.id_field = 'title_id'
                        self.SQLterm = self.make_titles_SQL_term
                        self.print_results = self.print_title_results
                elif self.search_type == 'Publication':
                        self.table = 'pubs'
                        self.id_field = 'pub_id'
                        self.SQLterm = self.make_pub_SQL_term
                        self.print_results = self.print_pub_results
                elif self.search_type == 'Publisher':
                        self.table = 'publishers'
                        self.id_field = 'publisher_id'
                        self.SQLterm = self.make_publisher_SQL_term
                        self.print_results = self.print_publisher_results
                elif self.search_type == 'Publication Series':
                        self.table = 'pub_series'
                        self.id_field = 'pub_series_id'
                        self.SQLterm = self.make_pub_series_SQL_term
                        self.print_results = self.print_pub_series_results
                elif self.search_type == 'Series':
                        self.table = 'series'
                        self.id_field = 'series_id'
                        self.SQLterm = self.make_series_SQL_term
                        self.print_results = self.print_series_results
                elif self.search_type == 'Award Type':
                        self.table = 'award_types'
                        self.id_field = 'award_type_id'
                        self.SQLterm = self.make_award_type_SQL_term
                        self.print_results = self.print_award_type_results
                elif self.search_type == 'Award Category':
                        self.table = 'award_cats'
                        self.id_field = 'award_cat_id'
                        self.SQLterm = self.make_award_cat_SQL_term
                        self.print_results = self.print_award_cat_results
                elif self.search_type == 'Award':
                        self.table = 'awards'
                        self.id_field = 'award_id'
                        self.SQLterm = self.make_award_SQL_term
                        self.print_results = self.print_award_results
                else:
                        self.display_error('Non-Existing Record Type')

        def process_sort(self):
                self.sort = self.format_entry(self.order_by)
                if self.search_type == 'Publication' and self.sort not in ('pub_title', 'pub_ctype',
                                                         'pub_year', 'pub_isbn', 'pub_catalog',
                                                         'pub_price', 'pub_pages', 'pub_ptype', 'pub_frontimage'):
                        self.unknown_sort()
                elif self.search_type == 'Author' and self.sort not in ('author_canonical',
                                                            'author_lastname',
                                                            'author_legalname',
                                                            'author_birthplace',
                                                            'author_birthdate',
                                                            'author_deathdate'):
                        self.unknown_sort()
                elif self.search_type == 'Title' and self.sort not in ('title_title',
                                                            'title_copyright',
                                                            'title_ttype'):
                        self.unknown_sort()
                elif self.search_type == 'Publisher' and self.sort != 'publisher_name':
                        self.unknown_sort()
                elif self.search_type == 'Publication Series' and self.sort != 'pub_series_name':
                        self.unknown_sort()
                elif self.search_type == 'Series' and self.sort != 'series_title':
                        self.unknown_sort()
                elif self.search_type == 'Award Type' and self.sort not in ('award_type_short_name',
                                                            'award_type_name',
                                                            'award_type_for',
                                                            'award_type_by',
                                                            'award_type_poll',
                                                            'award_type_non_genre'):
                        self.unknown_sort()
                elif self.search_type == 'Award Category' and self.sort not in ('award_cat_name',
                                                            'award_cat_order'):
                        self.unknown_sort()
                elif self.search_type == 'Award' and self.sort not in ('award_year',
                                                            'award_level'):
                        self.unknown_sort()
                if self.sort == 'pub_pages':
                        self.sort = 'CAST(pub_pages as SIGNED)'
                elif self.sort == 'pub_price':
                        self.sort = "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_price,' ',''),'$',''),'C',''),'A',''),'M',''),'D',''),CHAR(0xA3),''),'F',''),CHAR(0x80),''),'z&#322;',''),'NZ',''),'t',''),CHAR(0x83),'')*100"
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
                elif self.search_type == 'Award Type':
                        if self.sort != 'award_type_short_name':
                                self.sort += ', award_type_short_name'
                elif self.search_type == 'Award Category':
                        if self.sort != 'award_cat_name':
                                self.sort += ', award_cat_name'
                elif self.search_type == 'Award':
                        if self.sort == 'award_level':
                                self.sort = 'CAST(award_level as SIGNED)'
                        if self.sort != 'award_year':
                                self.sort += ', award_year'

        def unknown_sort(self):
                self.display_error("Unknown sort field: %s" % self.sort)

        def process_terms(self):
                # Special case for "Show All Titles"
                if (self.search_type == 'Title') and self.form.has_key('exact'):
                        self.process_term(self.form.get('exact'), 'exact', 'exact')

                for count in range(1, self.max_term + 1):
                        term = 'TERM_%d' % count
                        if self.form.has_key(term):
                                use = self.form.get('USE_%d' % count)
                                operator = self.form.get('O_%d' % count)
                                if not operator:
                                        operator = self.form.get('OPERATOR_%d' % count)
                                self.process_term(self.form.get(term), use, operator)

                if not self.term_list:
                        self.display_error("No search data entered")

        def process_term(self, term, use, operator):
                term = normalizeInput(term)
                if not term:
                        return
                raw_entry = term
                entry = self.format_entry(term)
                self.validate_term(use, entry)

                self.check_valid_operator(operator)
                self.operator_list.append(operator)

                if use == 'pub_isbn':
                        # Search for possible ISBN variations
                        isbn_values = isbnVariations(entry)
                        isbn_count = 0
                        sql_value = '('
                        for isbn_value in isbn_values:
                                padded_entry = self.pad_entry(operator, isbn_value)
                                if isbn_count:
                                        if operator in ('notexact', 'notcontains'):
                                                sql_value += ' and '
                                        else:
                                                sql_value += ' or '
                                sql_value += "pubs.pub_isbn %s" % padded_entry
                                isbn_count += 1
                        sql_value += ")"
                elif use == 'award_level':
                        try:
                                # Remove the trailing description of the award level
                                entry = entry.split(' ')[0]
                                entry = int(entry)
                        except:
                                self.display_error('Invalid Award Level')
                        sql_value = self.pad_entry(operator, entry)
                else:
                        sql_value = self.pad_entry(operator, entry)

                (new_term, new_dbases, new_joins) = self.SQLterm(use, entry, sql_value)
                self.term_list.append(new_term)
                self.merge_table_info_lists(self.dbases, new_dbases)

                for join in new_joins:
                        if join not in self.join_list:
                                self.join_list.append(join)

        def check_valid_operator(self, operator):
                operators = ('exact', 'notexact', 'contains', 'notcontains', 'starts_with', 'ends_with')
                if operator not in operators:
                        message = 'Valid operators are: '
                        for operator in operators:
                                message += operator
                                message += ', '
                        self.display_error(message[:-2])

        def pad_entry(self, operator, entry):
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
                        self.display_error('An unexpected error has occurred. Please post the URL of this Web page on the Moderator noticeboard.')
                return padded_entry

        def validate_empty_term(self, value):
                stripped = value
                for wildcard in self.wildcards:
                        stripped = stripped.replace(wildcard,'')
                        if not stripped:
                                self.display_error('Search values must contain at least one non-wildcard character')

        def validate_term(self, field, value):
                self.validate_empty_term(value)
                
                if field in ('month', 'pub_month'):
                        (year, month, error) = validateMonth(value)
                        if error:
                                self.display_error(error)
                elif field == 'title_ttype':
                        if value.upper() not in ALL_TITLE_TYPES:
                                self.display_error('Valid title types are: %s' % ', '.join(ALL_TITLE_TYPES))
                elif field in ('title_graphic', 'title_non_genre', 'title_jvn', 'title_nvz', 'award_type_poll', 'award_type_non_genre'):
                        if value.lower() not in ('yes', 'no'):
                                self.display_error('Yes/No value required')
                elif field == 'pub_ctype':
                        if value.upper() not in PUB_TYPES:
                                self.display_error('Valid title types are: %s' % ', '.join(PUB_TYPES))

        def merge_table_info_lists(self, dest, src):
                for sti in src:
                        found = 0
                        for dti in dest:
                                if dti == sti:
                                        found = 1
                                        dti.merge_hints(sti)
                                        break
                        if not found:
                                dest.append(sti)

        def format_entry(self, value):
                value = db.escape_string(value)
                # Change asterisks to % because * is also a supported wildcard character
                value = string.replace(value, '*', '%')
                return value

        def make_terms(self):
                # Concatenate terms using the conjunction. Wrap the result in parens
                # to avoid unintended interaction with the join clauses.
                self.terms = "("
                count = 1
                for term in self.term_list:
                        if count == 1:
                                self.terms += '%s ' % term
                        else:
                                self.terms += '%s %s ' % (self.conjunction, term)
                        count += 1
                self.terms += ")"

                # Add the join clauses to the end
                for join in self.join_list:
                        self.terms += " and " + join

        def execute_query(self):
                if self.action == 'query':
                        self.query = 'select distinct %s.* from ' % self.table
                elif self.action == 'count':
                        self.query = 'select count(distinct %s.%s) from ' % (self.table, self.id_field)
                self.make_table_query()
                self.search()
                if self.action == 'count':
                        self.display_message('Count of matching records: %d' % self.records[0])

        def print_pub_results(self):
                PrintPubsTable(self.records, 'adv_search', self.user, 100)

        def print_publisher_results(self):
                PrintPublisherTable(self.records, 1, 100, self.user)
                if self.user.moderator:
                        self.print_merge_button()

        def print_pub_series_results(self):
                PrintPubSeriesTable(self.records, 100)

        def print_series_results(self):
                PrintSeriesTable(self.records, 100)

        def print_award_type_results(self):
                PrintAwardResults(self.records, 100)

        def print_award_cat_results(self):
                PrintAwardCatResults(self.records, 100)

        def print_award_results(self):
                from awardClass import awards
                award = awards(db)
                award.PrintAwardTable(self.records, 1, 1, 100)

        def print_author_results(self):
                PrintAuthorTable(self.records, 1, 100, self.user)
                if self.user.moderator:
                        self.print_merge_button()

        def print_title_results(self):
                PrintTitleTable(self.records, 1, 100, self.user)
                self.print_merge_button()

        def search(self):
                db.query(self.query)
                result = db.store_result()
                self.num = result.num_rows()

                if not self.num:
                        self.display_message('No records found')

                record = result.fetch_row()
                while record:
                        self.records.append(record[0])
                        record = result.fetch_row()

        def make_table_query(self):
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
                if self.user.moderator:
                        if self.search_type == 'Author':
                                self.print_help_merge('authors', 'av_merge')
                if self.search_type == 'Title':
                        self.print_help_merge('titles', 'tv_merge')

        def print_help_merge(self, record_type, script):
                print '<div id="HelpBox">'
                print '<b>Help:How to merge %s: </b>' % record_type
                print '<a href="http://%s/index.php/Help:How_to_merge_%s">Help:How to merge %s</a><p>' % (WIKILOC, record_type, record_type)
                print '</div>'
                print '<form METHOD="POST" ACTION="/cgi-bin/edit/%s.cgi">' % script

        def print_page_buttons(self):
                print '<div class="button-container">'
                if self.start > 99:
                        self.print_page_button('Previous')
                if self.num > 100:
                        self.print_page_button('Next')
                print '</div>'

        def print_page_button(self, direction):
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % HTFAKE
                print '<div>'
                for key in self.form.keys():
                        if key == 'START':
                                if direction == 'Previous':
                                        key_value = self.start - 100
                                else:
                                        key_value = self.start + 100
                        else:
                                key_value = cgi.escape(self.form[key], True)
                        print '<input NAME="%s" value="%s" type="HIDDEN">' % (key, key_value)
                if direction == 'Previous':
                        start = self.start-99
                        end = self.start
                else:
                        start = self.start+101
                        end = self.start+200
                print '<input TYPE="SUBMIT" VALUE="%s page (%d - %d)">' % (direction, start, end)
                print '</div>'
                print '</form>'

        def print_merge_button(self):
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Merge Selected Records">'
                print '</form>'
                print '<hr>'

        def make_titles_SQL_term(self, field, value, sql_value):
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
                elif field == 'single_vote':
                        clause = "votes.rating %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('votes')]
                        joins = ['votes.title_id=titles.title_id']
                elif field == 'title_webpage':
                        clause = "webpages.url %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('webpages')]
                        joins = ['webpages.title_id=titles.title_id']
                elif field in ('title_language', 'title_language_free'):
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('languages')]
                        joins = ['languages.lang_id=titles.title_language']
                elif field == 'tag':
                        clause = "tags.tag_name %s" % sql_value
                        dbases = [tableInfo('titles'), tableInfo('tags'), tableInfo('tag_mapping')]
                        joins = ['tag_mapping.title_id=titles.title_id','tags.tag_id=tag_mapping.tag_id']
                # "exact" is used by "Show All Titles" and by "view all titles by this alternate name"
                elif field == 'exact':
                        clause = "canonical_author.author_id=%d and canonical_author.ca_status=1" % int(value)
                        dbases = [tableInfo('titles'), tableInfo('canonical_author')]
                        joins = ['titles.title_id=canonical_author.title_id']
                else:
                        self.display_error("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

        def make_author_SQL_term(self, field, value, sql_value):
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
                elif field in ('author_language', 'author_language_free'):
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
                        self.display_error("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

        def make_pub_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('pubs')]

                if field == 'pub_title':
                        clause = "pubs.pub_title %s" % sql_value
                elif field == 'pub_trans_title':
                        clause = "trans_pubs.trans_pub_title %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('trans_pubs')]
                        joins = ['trans_pubs.pub_id=pubs.pub_id']
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
                        # ISBNs are a special case. The whole clause was pre-built in process_term
                        clause = sql_value
                elif field == 'pub_catalog':
                        clause = "pubs.pub_catalog %s" % sql_value
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
                        joins = ['pubs.pub_id=pub_content.pub_id',
                                 'pub_content.title_id=canonical_author.title_id',
                                 'canonical_author.title_id=titles.title_id',
                                 'canonical_author.author_id=authors.author_id']
                elif field in ('title_language', 'title_language_free'):
                        clause = "languages.lang_name %s" % sql_value
                        dbases = [tableInfo('pubs'), tableInfo('pub_content'), tableInfo('titles'), tableInfo('languages')]
                        joins = ['pubs.pub_id=pub_content.pub_id',
                                 'pub_content.title_id=titles.title_id',
                                 'languages.lang_id=titles.title_language']
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
                        self.display_error("Unknown field: %s" % field)
                return ("(%s)" % clause, dbases, joins)

        def make_publisher_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('publishers')]
                if field == 'publisher_name':
                        clause = 'publishers.publisher_name %s' % sql_value
                elif field == 'trans_publisher_name':
                        clause = 'trans_publisher.trans_publisher_name %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('trans_publisher')]
                        joins = ['trans_publisher.publisher_id=publishers.publisher_id']
                elif field == 'publisher_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('notes')]
                        joins = ['publishers.note_id = notes.note_id']
                elif field == 'publisher_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('publishers'), tableInfo('webpages')]
                        joins = ['webpages.publisher_id=publishers.publisher_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

        def make_pub_series_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('pub_series')]
                if field == 'pub_series_name':
                        clause = 'pub_series.pub_series_name %s' % sql_value
                elif field == 'trans_pub_series_name':
                        clause = 'trans_pub_series.trans_pub_series_name %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('trans_pub_series')]
                        joins = ['trans_pub_series.pub_series_id=pub_series.pub_series_id']
                elif field == 'pub_series_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('notes')]
                        joins = ['pub_series.pub_series_note_id = notes.note_id']
                elif field == 'pub_series_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('pub_series'), tableInfo('webpages')]
                        joins = ['webpages.pub_series_id=pub_series.pub_series_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

        def make_award_type_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('award_types')]
                if field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                elif field == 'award_type_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                elif field == 'award_type_for':
                        clause = 'award_types.award_type_for %s' % sql_value
                elif field == 'award_type_by':
                        clause = 'award_types.award_type_by %s' % sql_value
                elif field == 'award_type_poll':
                        clause = 'award_types.award_type_poll %s' % sql_value
                elif field == 'award_type_non_genre':
                        clause = 'award_types.award_type_non_genre %s' % sql_value
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('award_types')]
                        joins = ['award_types.award_type_note_id = notes.note_id']
                elif field == 'webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('webpages')]
                        joins = ['webpages.award_type_id=award_types.award_type_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

        def make_award_cat_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('award_cats')]
                if field == 'award_cat_name':
                        clause = 'award_cats.award_cat_name %s' % sql_value
                elif field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats')]
                        joins = ['award_cats.award_cat_type_id = award_types.award_type_id']
                elif field == 'award_type_full_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats')]
                        joins = ['award_cats.award_cat_type_id = award_types.award_type_id']
                elif field == 'award_cat_order':
                        clause = 'award_cats.award_cat_order %s' % sql_value
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('award_cats')]
                        joins = ['award_cats.award_cat_note_id = notes.note_id']
                elif field == 'webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('award_cats'), tableInfo('webpages')]
                        joins = ['webpages.award_cat_id = award_cats.award_cat_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

        def make_award_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('awards')]
                if field == 'award_year':
                        clause = 'SUBSTRING(awards.award_year,1,4) %s' % sql_value
                elif field == 'award_level':
                        clause = 'awards.award_level %s' % sql_value
                elif field == 'title_title':
                        clause = 'titles.title_title %s' % sql_value
                        dbases = [tableInfo('awards'), tableInfo('titles'), tableInfo('title_awards')]
                        joins = ['awards.award_id = title_awards.award_id',
                                 'title_awards.title_id=titles.title_id']
                elif field == 'title_ttype':
                        clause = 'titles.title_ttype %s' % sql_value
                        dbases = [tableInfo('awards'), tableInfo('titles'), tableInfo('title_awards')]
                        joins = ['awards.award_id = title_awards.award_id',
                                 'title_awards.title_id=titles.title_id']
                elif field == 'award_cat_name':
                        clause = 'award_cats.award_cat_name %s' % sql_value
                        dbases = [tableInfo('award_cats'), tableInfo('awards')]
                        joins = ['award_cats.award_cat_id = awards.award_cat_id']
                elif field == 'award_type_short_name':
                        clause = 'award_types.award_type_short_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats'), tableInfo('awards')]
                        joins = ['awards.award_cat_id = award_cats.award_cat_id and award_cats.award_cat_type_id = award_types.award_type_id']
                elif field == 'award_type_full_name':
                        clause = 'award_types.award_type_name %s' % sql_value
                        dbases = [tableInfo('award_types'), tableInfo('award_cats'), tableInfo('awards')]
                        joins = ['awards.award_cat_id = award_cats.award_cat_id and award_cats.award_cat_type_id = award_types.award_type_id']
                elif field == 'note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('notes'), tableInfo('awards')]
                        joins = ['awards.award_note_id = notes.note_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

        def make_series_SQL_term(self, field, value, sql_value):
                # Set up default values
                joins = []
                dbases = [tableInfo('series')]
                if field == 'series_title':
                        clause = 'series.series_title %s' % sql_value
                elif field == 'trans_series_name':
                        clause = 'trans_series.trans_series_name %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('trans_series')]
                        joins = ['trans_series.series_id=series.series_id']
                elif field == 'parent_series_name':
                        clause = 's2.series_title %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('series s2')]
                        joins = ['s2.series_id = series.series_parent']
                elif field == 'parent_series_position':
                        clause = 'series.series_parent_position %s' % sql_value
                elif field == 'series_note':
                        clause = 'notes.note_note %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('notes')]
                        joins = ['series.series_note_id = notes.note_id']
                elif field == 'series_webpage':
                        clause = 'webpages.url %s' % sql_value
                        dbases = [tableInfo('series'), tableInfo('webpages')]
                        joins = ['webpages.series_id=series.series_id']
                else:
                        self.display_error('Unknown field: %s' % field)
                return ('(%s)' % clause, dbases, joins)

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

        def merge_hints(self, other):
            for hint in other.hints:
                if not hint in self.hints:
                    self.hints.append(hint)
            return self
