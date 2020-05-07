#
#     (C) COPYRIGHT 2004-2020   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import sys
import MySQLdb
import string
import traceback
from isfdb import *
from time import *

################################################################
# This section is executed when the file is imported by another
# file. The try section below is executed. If a successful
# connection to the database is made, the query count is updated
# via a call to SQLUpdateQueries(). If an exception occurs, html
# error code is emitted, and the application exits.
################################################################

def StandardQuery(query):
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def OneField(query):
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0][0])
		record = result.fetch_row()
	return results

def SQLUpdateQueries():
	query = "select metadata_counter from metadata"
	db.query(query)
	result = db.store_result()
	retvalue = result.fetch_row()[0][0]
	newvalue = retvalue + 1
	update = "update metadata set metadata_counter='%d'" % (newvalue)
	db.query(update)
	return retvalue

try:
	db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
	db.select_db(DBASE)
	SQLUpdateQueries()
except:
        PrintHTMLHeaders('Database Connection Error')
        print '</div>'
        print '<div id="nav">'
       	print '<a href="http:/%s/index.cgi">' % HTFAKE
	print '<img src="http://%s/isfdb.gif" width="90%%" alt="ISFDB logo">' % HTMLLOC
        print '</a>'
        print '</div>'
        print '<div id="main2">'
        print '<div id="ErrorBox">'
	print 'Cannot connect to the ISFDB database'
	print '</div>'
	print '</div>'
	print '</div>'
        print '</body>'
        print '</html>'
	sys.exit(0)


def SQLgetDatabaseStatus():
	query = "select metadata_dbstatus from metadata"
	db.query(query)
	result = db.store_result()
	version = result.fetch_row()[0][0]
	return version

def SQLgetEditingStatus():
	query = "select metadata_editstatus from metadata"
	db.query(query)
	result = db.store_result()
	version = result.fetch_row()[0][0]
	return version

def SQLgetSchemaVersion():
	query = "select metadata_schemaversion from metadata"
	db.query(query)
	result = db.store_result()
	version = result.fetch_row()[0][0]
	return version

def todaysDate():
	date = gmtime()
	month = date[1]
	day = date[2]
	year  = str(date[0])
	ISFDBdate = '%s-%02d-%02d' % (year, int(month), int(day))
	return ISFDBdate

def SQLMultipleAuthors(author):
	query = "select * from authors where author_canonical like '%s (%%'" % db.escape_string(author)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return 0

def SQLgetAuthorData(author):
	query = "select * from authors where author_canonical='%s'" % db.escape_string(author)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return 0

def SQLloadAuthorData(author_id):
	query = "select * from authors where author_id=%d" % int(author_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return 0

def SQLauthorIsPseudo(au_id):
	query = "select pseudo_id from pseudonyms where pseudonym=%d" % int(au_id)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		return 1
	else:
		return 0

def SQLauthorHasPseudo(au_id):
	query = "select pseudo_id from pseudonyms where author_id=%d" % int(au_id)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		return 1
	else:
		return 0

def SQLgetBriefActualFromPseudo(au_id):
	query = """select a.author_id, a.author_canonical
                   from authors a, pseudonyms p
                   where p.pseudonym = %d
                   and p.author_id = a.author_id
                   order by a.author_lastname, a.author_canonical""" % int(au_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	authors = [] 
	while record:
		authors.append(list(record[0]))
		record = result.fetch_row()
	return authors

def SQLGetSimilarRecords(record_id, name, table, id_field, name_field):
        # Drop everything to the right of the first " ("
        name = name.split(' (')[0]
        name = name.strip()
        exact_name = db.escape_string(name.replace('_','\_'))
        table = db.escape_string(table)
        id_field = db.escape_string(id_field)
        name_field = db.escape_string(name_field)
        query = """select * from %s where (%s = '%s'
                   or %s like '%s (%%') and %s != %d
                   order by %s
                   """ % (table, name_field, exact_name, name_field, exact_name, id_field, int(record_id), name_field)
        return StandardQuery(query)

def SQLgetActualFromPseudo(au_id):
	query = "select authors.author_canonical from authors,pseudonyms where pseudonyms.pseudonym=%d and pseudonyms.author_id=authors.author_id;" % int(au_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	authors = [] 
	while record:
		authors.append(list(record[0]))
		record = result.fetch_row()
	return authors

def SQLgetBriefPseudoFromActual(au_id):
	query = """select a.author_id, a.author_canonical
                   from authors a, pseudonyms p
                   where p.author_id = %d
                   and p.pseudonym = a.author_id
                   order by a.author_lastname""" % int(au_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	authors = [] 
	while record:
		authors.append(list(record[0]))
		record = result.fetch_row()
	return authors

def SQLgetPseudoFromActual(au_id):
	query = "select authors.author_canonical from authors,pseudonyms where pseudonyms.author_id=%d and pseudonyms.pseudonym=authors.author_id;" % int(au_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	authors = [] 
	while record:
		authors.append(list(record[0]))
		record = result.fetch_row()
	return authors

def SQLupdateViews(author_id):
	query = "select author_views, author_annualviews from authors where author_id=%d" % author_id
        db.query(query)
        result = db.store_result()
        view_data = result.fetch_row()
        total_views = view_data[0][0]
        annual_views = view_data[0][1]
        update = """update authors set author_views = %d, author_annualviews = %d
                    where author_id=%d""" % (total_views+1, annual_views+1, author_id)
        db.query(update)
	return

def SQLupdateTitleViews(title_id):
	total_views = 0
	query = "select title_views from titles where title_id=%d" % title_id
	try:
		db.query(query)
		result = db.store_result()
		total_views = views = result.fetch_row()[0][0]
		update = "update titles set title_views='%d' where title_id='%d'" % (views+1, title_id)
		db.query(update)
	except:
		return 0
	query = "select title_annualviews from titles where title_id=%d" % title_id
	try:
		db.query(query)
		result = db.store_result()
		views = result.fetch_row()[0][0]
		update = "update titles set title_annualviews='%d' where title_id='%d'" % (views+1, title_id)
		db.query(update)
	except:
		return 0
	return total_views

def SQLgetSeriesData(author_id):
	query = """select distinct series.* from series, titles, canonical_author
                where titles.series_id=series.series_id
                and titles.title_id=canonical_author.title_id
                and canonical_author.author_id=%d
                order by series.series_title""" % int(author_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(list(record[0]))
		record = result.fetch_row()
	return records

def SQLget1Series(seriesrec):
	query = "select * from series where series_id='%d'" % (int(seriesrec))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return 0

def SQLgetNotes(note_id):
        if not note_id:
                return ''
	query = "select * from notes where note_id='%d'" % int(note_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	return record[0][1]

def SQLloadAllAuthorTitles(aurec, page_type, languages_all, languages):
	if page_type == 'Summary':
		query = """select t.*, IF(t.title_seriesnum IS NULL, 1, 0) AS isnull
                from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by isnull, t.title_seriesnum, t.title_seriesnum_2,
                IF(t.title_copyright = '0000-00-00', 1, 0),
                t.title_copyright, t.title_title""" % aurec
	elif page_type == 'Chronological':
		query = """select t.* from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by IF(t.title_copyright = '0000-00-00', 1, 0),
                t.title_copyright, t.title_title""" % aurec
	else:
		query = """select t.* from titles t, canonical_author ca
                where (ca.author_id=%d and ca.title_id=t.title_id and ca.ca_status=1)
                and t.title_parent=0
                order by t.title_title, t.title_copyright""" % aurec
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = []
	# For alphabetical and award biblios, also build a comma-separated list to use in a SQL IN clause later
	in_clause = ''
	while record:
		records.append(list(record[0]))
		if page_type in ('Alphabetical', 'Award'):
                        title_id = str(record[0][0])
                        if not in_clause:
                                in_clause = title_id
                        else:
                                in_clause += ",%s" % title_id
		record = result.fetch_row()
	# For alphabetical and award biblios, also retrieve the VTs of canonical titles
	if page_type in ('Alphabetical', 'Award') and in_clause:
                query = "select titles.* from titles where title_parent in (%s)" % in_clause
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        # Only select this VT if it meets the current user's language pereferences
                        if ((languages_all == 'All') or
                            not record[0][TITLE_LANGUAGE] or
                            ((languages_all == 'Selected') and
                             (record[0][TITLE_LANGUAGE] in languages))):
                                records.append(list(record[0]))
                        record = result.fetch_row()
                # Re-sort the list by title
                records.sort(key=lambda tup:tup[1])
	return records


def SQLloadAnyTitles(aurec):
	query = "select titles.* from titles,canonical_author where (canonical_author.author_id = %d and canonical_author.title_id = titles.title_id and canonical_author.ca_status = 1);" % (aurec)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(list(record[0]))
		record = result.fetch_row()
	return records

def SQLloadTitlesXBT(recno):
	query = "select titles.* from titles,pub_content where pub_content.pub_id='%d' and pub_content.title_id = titles.title_id order by titles.title_title;" % int(recno)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(record[0])
		record = result.fetch_row()
	return records

def SQLloadIntervieweeXBA(author):
	query = "select * from titles where title_ttype='INTERVIEW' and title_subject_author like '%%%s%%';" % db.escape_string(author)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(record[0])
		record = result.fetch_row()
	return records

def SQLloadTitleFromAward(award_id):
	query = "select titles.* from titles,title_awards where titles.title_id=title_awards.title_id and title_awards.award_id='%d';" % int(award_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	return record

def SQLloadAwardsXBA(author, titles, pseudonyms):
        # Load all awards for one author
        #
        # Step 1: Create a list of author/pseudonym names for this person
        names = []
        names.append(author)
        for pseudonym in pseudonyms:
                names.append(pseudonym[1])
	# Step 2: Build an SQL IN clause for titles
	in_clause = ''
	for title in titles:
                title_id = str(title[TITLE_PUBID])
                if not in_clause:
                        in_clause = title_id
                else:
                        in_clause += ",%s" % title_id
        # Step 3: Create a query to retrieve awards whose author name matches the canonical author name
        # or one of his pseudonyms AND all awards associated with this author's titles and VTs
        first = 1
        query = "select * from awards where "
        for name in names:
                value = db.escape_string(name)
                if not first:
                        query += "or "
                query += "(award_author = '%s') or " % value
                query += "(award_author like '%s+%%') or " % value
                query += "(award_author like '%%+%s') or " % value
                query += "(award_author like '%%+%s+%%') " % value
                first = 0
        if in_clause:
                query += "UNION select a.* from awards as a, title_awards as t where a.award_id=t.award_id and t.title_id in (%s) " % in_clause
        query += "order by award_year"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(record[0])
		record = result.fetch_row()
	return records

def SQLloadAwardsForYearType(award_type_id, year):
	query = """select a.*, c.award_cat_name
                   from awards a, award_cats c
                   where a.award_type_id=%d
                   and YEAR(a.award_year)=%d
                   and a.award_cat_id=c.award_cat_id
                   order by ISNULL(c.award_cat_order), c.award_cat_order,
                   c.award_cat_name, ABS(a.award_level),
                   a.award_title""" % (int(award_type_id), int(year))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(record[0])
		record = result.fetch_row()
	return records

def SQLloadAwardsForCat(award_cat_id, win_nom):
	query = "select a.*,c.award_cat_name from awards a, award_cats c where a.award_cat_id=%d " % int(award_cat_id)
	# If the requested award list is limited to wins, then add another limiting clause to the query
	if not win_nom:
                query += "and a.award_level = '1'"
        query += "and a.award_cat_id=c.award_cat_id order by a.award_year, ABS(a.award_level), a.award_title"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = {}
	while record:
                year = record[0][AWARD_YEAR]
                if year not in records:
                        records[year] = []
                records[year].append(record[0])
		record = result.fetch_row()
	return records

def SQLloadAwardsForCatYear(award_cat_id, award_year):
	query = """select a.* from awards a, award_cats c
                where a.award_cat_id = %d
                and a.award_cat_id = c.award_cat_id
                and YEAR(a.award_year) = %d
                order by ABS(a.award_level), a.award_title""" % (int(award_cat_id), int(award_year))
	return StandardQuery(query)

def SQLloadTitlesXBS(series):
	query = "select * from titles where series_id = '%d';" % (series)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	records = [] 
	while record:
		records.append(record[0])
		record = result.fetch_row()
	return records


###########################################
#
# Function: SQLGetForthcoming
# Arg1:     Target Month
# Arg2:     Target Year
#
# Description: This function creates a 
# python list of publications to be 
# published in a specific month/year. 
#
###########################################
def SQLGetForthcoming(month, year, day, all):
	if month == 12:
		end    = "%d-01-00" % (int(year)+1)
	else:
		end    = "%s-%02d-00" % (year, month+1)
	target = "%s-%02d-%02d" % (year, month, int(day))
	if all:
		query = "select * from pubs where pub_year>='%s' and pub_year<'%s' order by pub_year,pub_title" % (db.escape_string(target), db.escape_string(end))
	else:
		query = "select * from pubs where pub_year>='%s' and pub_year<'%s' and pub_frontimage is not NULL order by pub_year,pub_title" % (db.escape_string(target), db.escape_string(end))
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	results = []
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results
	
def SQLGetTodaysPubs(month, year, day, limit):
	target = "%s-%02d-%02d" % (year, month, int(day))
	if limit:
		query = "select * from pubs where pub_year='%s' order by pub_title limit 25" % (db.escape_string(target))
	else:
		query = "select * from pubs where pub_year='%s' order by pub_title" % (db.escape_string(target))
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	results = []
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results
	
def SQLGetPubByTag(tag):
	query = "select * from pubs where pub_tag = '%s'" % (db.escape_string(tag))
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		pub = result.fetch_row()
		return pub[0]
	else:
		return 0

def SQLGetPubById(id):
	query = "select * from pubs where pub_id = '%d'" % (int(id))
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		pub = result.fetch_row()
		return pub[0]
	else:
		return 0

def SQLGetCoverAuthorsForPubs(pub_list):
        pub_string = ", ".join(pub_list)
	query = """select pc.pub_id, a.author_id, a.author_canonical
                from titles t, pub_content pc, canonical_author ca, authors a
                where pc.pub_id in (%s)
                and t.title_ttype = 'COVERART'
                and t.title_ttype = 'COVERART'
                and pc.title_id = t.title_id
		and ca.title_id = pc.title_id
		and ca.author_id = a.author_id""" % db.escape_string(pub_string)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = {}
	while row:
                pub_id = row[0][0]
                author_id = row[0][1]
                author_name = row[0][2]
                if pub_id not in results:
                        results[pub_id] = []
                results[pub_id].append((author_id, author_name))
                row = result.fetch_row()
	return results

def SQLGetCoverPubsByTitle(titlerec):
	query = "select title_id from titles where title_id=%d and title_ttype='COVERART' \
                UNION select title_id from titles where title_parent=%d \
                and title_ttype='COVERART'" % (titlerec, titlerec)
        results = retrievePubsQuery(query)
        return results

def SQLGetPubsByTitle(titlerec):
	query = "select title_id from titles where title_id=%d or title_parent=%d" % (titlerec, titlerec)
        results = retrievePubsQuery(query)
        return results

def SQLGetPubsByTitleNoParent(titlerec):
	query = "select title_id from titles where title_id=%d" % (titlerec)
        results = retrievePubsQuery(query)
        return results

def SQLGetPubsByTitleNoTranslations(titlerec):
	query = """select %d
                   UNION
                   select variant.title_id
                   from titles variant, titles parent
                   where variant.title_parent=%d
                   and parent.title_id = %d
                   and variant.title_language = parent.title_language
                """ % (int(titlerec), int(titlerec), int(titlerec))
        results = retrievePubsQuery(query)
        return results

def SQLGetPubsForChildTitles(titlerec):
	query = "select title_id from titles where title_parent=%d" % (titlerec)
        results = retrievePubsQuery(query)
        return results

def retrievePubsQuery(query):
        # Internal function, NOT TO BE CALLED DIRECTLY
        # Currently called by SQLGetPubsByTitle, SQLGetPubsByTitleNoParent,
        # SQLGetCoverPubsByTitle and SQLGetPubsForChildTitles
        #
	############################################################
	# STEP 1 - Get the list of titles
	############################################################
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	titles = []
	while title:
		titles.append(title[0])
		title = result.fetch_row()
	# If no titles were found, which may happen if the title has been deleted, return the empty list
	if not titles:
                return titles

	############################################################
	# STEP 2 - Form a query using those titles
	############################################################
       	query = "select distinct pubs.* from pubs,pub_content where pub_content.pub_id=pubs.pub_id "
	counter = 0
	for title in titles:
		if counter:
			query += "or pub_content.title_id=%d " % title
		else:
			query += "and (pub_content.title_id=%d " % title
		counter += 1
	# Display 0000 years last
	query += ") order by IF(pubs.pub_year = '0000-00-00', 1, 0), pubs.pub_year"

	results = []
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results


def SQLGetPubsByPublisherYear(publisher_id, year):
	query = """select * from pubs
                   where publisher_id=%d and YEAR(pub_year)=%d
                   order by pub_year""" % (int(publisher_id), int(year))
	results = []
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results


def SQLGetPubsByAuthor(aurec):
	query = "select pubs.* from pubs,pub_authors where pub_authors.author_id=%d and pubs.pub_id=pub_authors.pub_id;" % aurec
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	results = []
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results

def SQLGetPubContentByAuthor(aurec):
	query = "select pub_content.* from pub_content,canonical_author where canonical_author.author_id=%d and pub_content.title_id=canonical_author.title_id;" % aurec
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	results = []
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results

def SQLloadTitle(titlerec):
	query = "select * from titles where title_id = %d" % int(titlerec)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	if title:
		return list(title[0])
	else:
		return []

def SQLloadTitleList(title_ids):
        from library import list_to_in_clause
        if not title_ids:
                return {}
        in_clause = list_to_in_clause(title_ids)
	query = "select * from titles where title_id in (%s)" % in_clause
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                title_id = record[0][0]
                results[title_id] = record[0]
		record = result.fetch_row()
	return results

def SQLGetPublisher(pubrec):
        if not pubrec:
                return []
	query = "select * from publishers where publisher_id = '%d'" % (int(pubrec))
	db.query(query)
	result = db.store_result()
	publisher = result.fetch_row()
	if publisher:
		return list(publisher[0])
	else:
		return []

def SQLGetPublisherList(publisher_list):
        from library import list_to_in_clause
        if not publisher_list:
                return {}
        publisher_string = list_to_in_clause(publisher_list)
	query = "select * from publishers where publisher_id in (%s)" % publisher_string
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                publisher_id = record[0][0]
                publisher_name = record[0][1]
                results[publisher_id] = publisher_name
		record = result.fetch_row()
	return results

def SQLGetPublisherDirectory():
        query = """select publisher_name from publishers
                UNION
                select trans_publisher_name from trans_publisher"""
        return ASCIIDirectory(query)

def ASCIIDirectory(query):
        import unicodedata
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        records_map = {}
        while record:
                two_latin1_letters = record[0][0]
                first_latin_letter = two_latin1_letters[0]
                first_unicode_letter = first_latin_letter.decode('iso-8859-1')
                first_normalized_letter = unicodedata.normalize('NFKD', first_unicode_letter).encode('ascii', 'ignore').decode('ascii', 'strict').lower()
                second_normalized_letter = ' '
                if len(two_latin1_letters) > 1:
                        second_latin_letter = two_latin1_letters[1]
                        second_unicode_letter = second_latin_letter.decode('iso-8859-1')
                        second_normalized_letter = unicodedata.normalize('NFKD', second_unicode_letter).encode('ascii', 'ignore').decode('ascii', 'strict').lower()
                two_normalized_letters = first_normalized_letter + second_normalized_letter
                records_map[two_normalized_letters] = ''
                record = result.fetch_row()
        return records_map

def SQLGetMagazineDirectory():
        query = """select s.series_title
        from series s, titles t
        where t.series_id = s.series_id
        and t.title_ttype = 'EDITOR'
        UNION
        select t.title_title
        from titles t
        where t.title_ttype='EDITOR'
        UNION
        select tt.trans_title_title
        from trans_titles tt, titles t
        where t.title_ttype = 'EDITOR'
        and t.title_id = tt.title_id"""
        return ASCIIDirectory(query)

def SQLGetAuthorDirectory():
        query = """select lower(substring(author_lastname,1,2)) as xx, count(*)
        from authors group by xx"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        records_map = {}
        while record:
                records_map[record[0][0]] = record[0][1]
                record = result.fetch_row()
        return records_map

def SQLGetPubSeries(pub_series_id):
	query = "select * from pub_series where pub_series_id = %d" % int(pub_series_id)
	db.query(query)
	result = db.store_result()
	pub_series = result.fetch_row()
	if pub_series:
		return list(pub_series[0])
	else:
		return []

def SQLGetPubSeriesByName(pub_series_name):
	query = "select * from pub_series where pub_series_name = '%s'" % db.escape_string(pub_series_name)
	db.query(query)
	result = db.store_result()
	pub_series = result.fetch_row()
	if pub_series:
		return list(pub_series[0])
	else:
		return []

def SQLGetPubSeriesList(pub_series_list):
        from library import list_to_in_clause
        if not pub_series_list:
                return {}
        pub_series_string = list_to_in_clause(pub_series_list)
	query = "select * from pub_series where pub_series_id in (%s)" % pub_series_string
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                pub_series_id = record[0][0]
                pub_series_name = record[0][1]
                results[pub_series_id] = pub_series_name
		record = result.fetch_row()
	return results

def SQLLoadPubSeries(pub_series_ids):
	query = "select * from pub_series where pub_series_id in (%s) order by pub_series_name" % (db.escape_string(pub_series_ids))
	db.query(query)
	result = db.store_result()
	pub_series = result.fetch_row()
       	results = []
        while pub_series:
                results.append(pub_series[0])
                pub_series = result.fetch_row()
        return results

def SQLGetPubSeriesPubs(pub_series_id, display_order):
        # Supported display_order values:
        #  0: Show earliest year first
        #  1: Show last year first
        #  2: Sort by series number
	results = []
	query = "select * from pubs where pub_series_id=%d order by " % int(pub_series_id)
	if display_order == 0:
                query += "IF(pub_year = '0000-00-00', 1, 0), pub_year, cast(pub_series_num as UNSIGNED), pub_series_num"
	elif display_order == 1:
                query += "IF(pub_year = '0000-00-00', 1, 0), pub_year desc, cast(pub_series_num as UNSIGNED), pub_series_num"
	elif display_order == 2:
                query += "IF(pub_series_num IS NULL, 1, 0), cast(pub_series_num as UNSIGNED), pub_series_num, pub_year"
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results

def SQLCountPubsNotInPubSeries(publisher_id):
        query = """select count(*) from pubs where publisher_id=%d
                   and pub_series_id is null""" % int(publisher_id)
	db.query(query)
	result = db.store_result()
	pubs = result.fetch_row()
	return pubs[0][0]

def SQLGetPubsNotInSeries(publisher_id):
	results = []
	query = """select * from pubs where publisher_id=%d
                   and pub_series_id is NULL
                   order by IF(pub_year = '0000-00-00', 1, 0), pub_year""" % int(publisher_id)
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results

##################################################################
# FIND ROUTINES
##################################################################

def SQLFindAuthors(target, mode = 'contains'):
        from string import maketrans
        if mode == 'exact':
                query = "select distinct * from authors where author_canonical = '%s'""" % db.escape_string(target)
        elif mode == 'contains':
                target = db.escape_string('%'+target+'%')
                query = """select distinct a.* from authors a
                             where a.author_canonical like '%s'
                           union select distinct a.* from authors a, trans_authors at
                                where at.trans_author_name like '%s' and at.author_id = a.author_id
                           order by author_canonical""" % (target, target)
        elif mode == 'approximate':
                punctuation = """'",.()"""
                target = target.translate(maketrans("",""), punctuation)
                prefix = ''
                for character in punctuation:
                        prefix += 'REPLACE('
                suffix = ''
                for character in punctuation:
                        if character == "'":
                                suffix += ""","%s",'')""" % character
                        else:
                                suffix += ",'%s','')" % character
                name1 = '%s%s%s' % (prefix, 'a.author_canonical', suffix)
                name2 = '%s%s%s' % (prefix, 'at.trans_author_name', suffix)
                target = db.escape_string('%'+target+'%')
                query = """select distinct a.* from authors a
                           where %s like '%s'
                           union select distinct a.* from authors a, trans_authors at
                           where %s like '%s' and at.author_id = a.author_id
                           order by author_canonical""" % (name1, target, name2, target)
        return StandardQuery(query)

def SQLFindTitles(target):
        target = db.escape_string('%'+target+'%')
	query = """select distinct t.* from titles t
                        where t.title_title like '%s'
                union select distinct t.* from titles t, trans_titles tt
                        where tt.trans_title_title like '%s' and tt.title_id = t.title_id
                order by title_title""" % (target, target)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLFindExactTitles(target):
        query = "select * from titles where title_title = '%s' order by title_title" % db.escape_string(target)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLFindFictionTitles(target):
	target = db.escape_string('%'+target+'%')
	query = """select distinct t.* from titles t
                        where t.title_title like '%s'
                        and t.title_ttype in ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','POEM','SERIAL','SHORTFICTION','CHAPBOOK')
                union
                        select distinct t.* from titles t, trans_titles tt
                        where tt.trans_title_title like '%s' and tt.title_id = t.title_id
                        and t.title_ttype in ('ANTHOLOGY','COLLECTION','EDITOR','NOVEL','OMNIBUS','POEM','SERIAL','SHORTFICTION','CHAPBOOK')
                order by title_title""" % (target, target)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLFindYear(target):
	results = []
	try:
		year = int(target)
	except:
		return results

	query = "select * from titles where YEAR(title_copyright) = '%d' order by title_ttype,title_title" % (year)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLFindPublisher(target, mode = 'contains'):
        if mode == 'exact':
                query = "select distinct * from publishers where publisher_name = '%s'" % db.escape_string(target)
        else:
                target = db.escape_string('%'+target+'%')
                query = """select distinct p.* from publishers p
                           where p.publisher_name like '%s'
                           union
                           select distinct p.* from publishers p, trans_publisher tp
                           where tp.trans_publisher_name like '%s' and
                           tp.publisher_id = p.publisher_id
                           order by publisher_name""" % (target, target)
        return StandardQuery(query)

def SQLGetPublisherYears(publisher_id):
	results = []
	query = "select distinct YEAR(pub_year) from pubs where publisher_id='%d' order by pub_year" % int(publisher_id)
	db.query(query)
	result = db.store_result()
	year = result.fetch_row()
	while year:
		results.append(year[0][0])
		year = result.fetch_row()
	return results

def SQLFindPubSeries(target, mode = 'contains'):
        if mode == 'exact':
                query = "select * from pub_series where pub_series_name = '%s'" % db.escape_string(target)
        else:
                target = db.escape_string('%'+target+'%')
                query = """select distinct ps.* from pub_series ps
                           where ps.pub_series_name like '%s'
                           union
                           select distinct ps.* from pub_series ps, trans_pub_series tps
                           where tps.trans_pub_series_name like '%s'
                           and tps.pub_series_id = ps.pub_series_id
                           order by pub_series_name""" % (target, target)
        return StandardQuery(query)

def SQLFindMagazine(arg, directory = 0):
        if directory:
                target = db.escape_string(arg)
        else:
                target = db.escape_string('%'+arg+'%')
        # First retrieve matching series names
	query = """select distinct s.series_id, s.series_title, s.series_parent
                from series s, titles t
                where t.series_id = s.series_id
                and t.title_ttype = 'EDITOR'
                and s.series_title like '%s'
                UNION
                select distinct s.series_id, s.series_title, s.series_parent
                from series s, titles t, trans_series ts
                where t.series_id = s.series_id
                and t.title_ttype = 'EDITOR'
                and s.series_id = ts.series_id
                and ts.trans_series_name like '%s'
                """ % (target, target)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	series = {}
	while record:
                series_id = record[0][0]
                title = record[0][1]
                series_parent = record[0][2]
                if title not in series:
                        series[title] = {}
                series[title][series_id] = (series_parent, title)
		record = result.fetch_row()

        # Next find magazine titles that match the search string, but whose
        # series titles don't match it
        query="""select distinct t.title_title, s.series_id, s.series_title,
                s.series_parent from series s, titles t
                where t.title_title like '%s'
                and t.title_ttype = 'EDITOR'
                and t.series_id=s.series_id
                and s.series_title not like '%s'
                UNION
                select distinct t.title_title, s.series_id, s.series_title,
                s.series_parent from series s, titles t, trans_titles tt
                where tt.trans_title_title like '%s'
                and tt.title_id=t.title_id
                and t.title_ttype = 'EDITOR'
                and t.series_id=s.series_id
                and s.series_title not like '%s'
                """ % (target, target, target, target)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
                title = record[0][0]
                separator = title.rfind(" - ")
                if separator != -1:
                        title = title[:separator]
                series_id = record[0][1]
                series_title = record[0][2]
                series_parent = record[0][3]
                if title not in series:
                        series[title] = {}
                series[title][series_id] = (series_parent, series_title)
		record = result.fetch_row()

        count = 0
        for title in series:
                for series_id in series[title]:
                        count += 1
	return (series, count)

def SQLFindSeries(target, mode = 'contains'):
        if mode == 'exact':
                query = "select distinct * from series where series_title = '%s'" % db.escape_string(target)
        else:
                target = db.escape_string('%'+target+'%')
                query = """select distinct s.* from series s
                           where s.series_title like '%s'
                           union
                           select distinct s.* from series s, trans_series ts
                           where ts.trans_series_name like '%s'
                           and ts.series_id = s.series_id
                           order by series_title""" % (target, target)
        return StandardQuery(query)

def SQLFindSeriesChildren(id):
	query = "select series_id,IF(series.series_parent_position IS NULL or series.series_parent_position='', 1, 0) AS isnull from series where series_parent=%d ORDER BY isnull,series_parent_position" % (id)
	db.query(query)
	result = db.store_result()
	series = result.fetch_row()
	results = []
	while series:
		results.append(series[0][0])
		series = result.fetch_row()
	return results

def SQLgetSeriesName(id):
	query = "select series_title from series where series_id=%d" % int(id)
	db.query(query)
	result = db.store_result()
	series = result.fetch_row()
	return series[0][0]

def SQLFindSeriesId(target):
	target = db.escape_string(target)
	query = "select series_id from series where series_title='%s'" % (target)
	db.query(query)
	result = db.store_result()
	id = result.fetch_row()
	if result.num_rows() > 0:
                return id[0][0]
        else:
                return ''

def SQLFindSeriesName(target):
	query = "select series_title from series where series_id='%d'" % int(target)
	db.query(query)
	result = db.store_result()
	id = result.fetch_row()
	return id[0][0]

def SQLFindSeriesParent(target):
	query = "select series_parent from series where series_id='%d'" % int(target)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		id = result.fetch_row()
		return id[0][0]
	else:
		return ''

def SQLFindSeriesParentPosition(target):
	query = "select series_parent_position from series where series_id='%d'" % int(target)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		id = result.fetch_row()
		return id[0][0]
	else:
		return ''

def SQLFindSeriesTitles(target):
	results = []
	target = db.escape_string(target)
	query = "select titles.*,IF(titles.title_seriesnum IS NULL, 1, 0) AS isnull from titles,series where series.series_id=titles.series_id and series.series_title='%s' order by isnull,titles.title_seriesnum,titles.title_seriesnum_2,titles.title_copyright" % (target)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLLoadSeriesFromList(series_ids):
        from library import list_to_in_clause
        if not series_ids:
                return {}
        series_id_list = list_to_in_clause(series_ids)
	query = "select * from series where series_id in (%s)" % series_id_list
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                series_id = record[0][0]
		results[series_id] = record[0]
		record = result.fetch_row()
	return results
        

def SQLLoadSeriesListTitles(series_list):
	series_list = db.escape_string(series_list)
	query = """select titles.*,IF(titles.title_seriesnum IS NULL, 1, 0) AS isnull
                from titles where series_id in (%s) order by series_id,
                isnull, titles.title_seriesnum, titles.title_seriesnum_2,
                titles.title_copyright""" % (series_list)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results_dict = {}
	results_list = []
	while title:
                results_list.append(title[0])
                series_id = title[0][TITLE_SERIES]
                if series_id not in results_dict:
                        results_dict[series_id] = []
                results_dict[series_id].append(title[0])
		title = result.fetch_row()
	return (results_dict, results_list)

def SQLFindPubsByIsbn(targets, excluded_pub_id = 0):
	results = []
	if len(targets) > 0:
		first = 1
		query = "select * from pubs where (pub_isbn like '"
		for target in targets:
			if not first:
				query += "' or pub_isbn like '"
			query += db.escape_string(target)
			first = 0
		query += "')"
		if excluded_pub_id:
                        query += " and pub_id != %d" % int(excluded_pub_id)
		query += " order by pub_isbn limit 300"
		db.query(query)
		result = db.store_result()
		pub = result.fetch_row()
		while pub:
			results.append(pub[0])
			pub = result.fetch_row()
	return results

def SQLFindPubsByCatalogId(value):
        query = "select * from pubs where pub_catalog ='%s'" % db.escape_string(value)
	return StandardQuery(query)

def SQLFindPubSeriesForPublisher(publisher_id):
        results = []
        query = "select distinct pub_series_id from pubs where publisher_id = '%d' and pub_series_id IS NOT NULL" % int(publisher_id)
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	while pub:
		results.append(pub[0])
		pub = result.fetch_row()
	return results

def SQLgetPublisherName(id):
	query = "select publisher_name from publishers where publisher_id=%d" % (int(id))
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		publisher = result.fetch_row()
		return publisher[0][0]
	else:
		return ''

def SQLReviewedAuthors(title_id):
	query = """select authors.author_id, authors.author_canonical
                   from authors, canonical_author
                   where canonical_author.title_id = %d
                   and canonical_author.author_id = authors.author_id
                   and canonical_author.ca_status = 3""" % int(title_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLIntervieweeAuthors(title_id, author_id = 0):
	query = """select authors.author_id, authors.author_canonical
                   from authors, canonical_author
                   where canonical_author.title_id = %d
                   and canonical_author.author_id <> %d
                   and canonical_author.author_id = authors.author_id
                   and canonical_author.ca_status = 2""" % (int(title_id), int(author_id))
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLTitleBriefAuthorRecords(title_id):
	query = """select a.author_id, a.author_canonical
                 from authors a, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.ca_status = 1
                 and ca.title_id=%d
                 order by a.author_lastname, a.author_canonical""" % int(title_id)
	return StandardQuery(query)

def SQLTitleListBriefAuthorRecords(title_list, author_id = 0):
        if not title_list:
                return {}
        # Load author IDs and author names for a list of titles;
        # if a non-0 author ID was explicitly passed in, then skip it
	query = """select ca.title_id, a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and a.author_id <> %d
                and ca.ca_status = 1
                and ca.title_id in (%s)
                order by a.author_lastname, a.author_canonical""" % (int(author_id), db.escape_string(title_list))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                title_id = record[0][0]
                if title_id not in results:
                        results[title_id] = []
		results[title_id].append((record[0][1], record[0][2]))
		record = result.fetch_row()
	return results

def SQLTitleAuthors(title_id):
	query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and ca.ca_status=1
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0][0])
		title = result.fetch_row()
	return results

def SQLInterviewBriefAuthorRecords(title_id):
	query = """select a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=2
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
	return StandardQuery(query)

def SQLInterviewAuthors(title_id):
	query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id = ca.author_id
                and ca.ca_status=2
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0][0])
		title = result.fetch_row()
	return results

def SQLReviewBriefAuthorRecords(title_id):
	query = """select a.author_id, a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=3
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
	return StandardQuery(query)

def SQLReviewAuthors(title_id):
	query = """select a.author_canonical
                from authors a, canonical_author ca
                where a.author_id=ca.author_id
                and ca.ca_status=3
                and ca.title_id=%d
                order by a.author_lastname, a.author_canonical""" % int(title_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0][0])
		title = result.fetch_row()
	return results

def SQLPubBriefAuthorRecords(pub_id):
	query = """select a.author_id, a.author_canonical
                from authors a, pub_authors pa
                where a.author_id = pa.author_id
                and pa.pub_id = %d
                order by a.author_lastname, a.author_canonical""" % int(pub_id)
	return StandardQuery(query)

def SQLPubListBriefAuthorRecords(pub_list):
        from library import list_to_in_clause
        pub_string = list_to_in_clause(pub_list)
	query = """select pa.pub_id, a.author_id, a.author_canonical, a.author_lastname
                from authors a, pub_authors pa
                where a.author_id = pa.author_id
                and pa.pub_id in (%s)
                order by a.author_lastname, a.author_canonical""" % pub_string
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                pub_id = record[0][0]
                author_id = record[0][1]
                canonical_name = record[0][2]
                last_name = record[0][3]
                if pub_id not in results:
                        results[pub_id] = []
                results[pub_id].append((author_id, canonical_name, last_name))
		record = result.fetch_row()
	return results

def SQLPubAuthors(pub_id):
	query = """select a.author_canonical
                from authors a, pub_authors pa
                where a.author_id=pa.author_id
                and pa.pub_id=%d
                order by a.author_lastname, a.author_canonical""" % int(pub_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0][0])
		title = result.fetch_row()
	return results

def SQLMarqueAuthors(pub_id):
	query = "select authors.author_marque from authors,pub_authors where authors.author_id=pub_authors.author_id and pub_authors.pub_id='%d';" % int(pub_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		# If any of the authors are marque authors, return true
		if record[0][0]:
			return 1
		record = result.fetch_row()
	# Otherwise return false
	return 0

def SQLTitleAwards(title_id):
        ############################################################
        # Get variant titles including canonical one
        # as a string suitable for SQL's IN (...) clause
        ############################################################
        if not title_id:
                return ([])
        query = "select DISTINCT title_id from titles where title_id=%d or title_parent=%d" % (int(title_id), int(title_id))
        db.query(query)
        result0 = db.store_result()
        title = result0.fetch_row()
        if not title:
                return([])
        title_set = ""
        counter = 0
        while title:
                if counter:
                        title_set += ", "
                title_set += str(title[0][0])
                title = result0.fetch_row()
                counter += 1

        query = """select distinct awards.*
                from title_awards, awards
                where title_awards.title_id in (%s)
                and title_awards.award_id=awards.award_id
                order by awards.award_year, awards.award_level""" % (db.escape_string(title_set))
        return StandardQuery(query)

def SQLloadAwards(award_id):
	query = "select * from awards where award_id='%d'" % (award_id)
	db.query(query)
	result = db.store_result()
	award = result.fetch_row()
	results = []
	while award:
		results.append(award[0])
		award = result.fetch_row()
	return results

def SQLloadEmails(author_id):
	query = "select email_address from emails where author_id='%d'" % (author_id)
	db.query(query)
	result = db.store_result()
	email = result.fetch_row()
	results = []
	while email:
		results.append(email[0][0])
		email = result.fetch_row()
	return results

def SQLgetTitleReferral(pub_id, pub_ctype, include_editors=0):
	query = "select c.title_id,t.title_ttype from pub_content c, titles t where c.pub_id=%d and c.title_id=t.title_id" % int(pub_id)
	db.query(query)
	result = db.store_result()
	if result.num_rows() < 1:
		return 0
	title_data = result.fetch_row()
	while title_data:
		title_id = title_data[0][0]
		title_ttype = title_data[0][1]
		if title_ttype == pub_ctype:
			return title_id
		# If "include_editors" was set to 1 and this pub is a magazine or fanzine, then return the first found EDITOR title
                elif (include_editors == 1) and ((pub_ctype == 'MAGAZINE') or (pub_ctype == 'FANZINE')) and (title_ttype == 'EDITOR'):
                        return title_id
		title_data = result.fetch_row()
	return 0

def SQLgetTitleReferralList(pubs, include_editors=0):
        from library import list_to_in_clause
        pub_ids = []
        pub_types = {}
        for pub in pubs:
                pub_id = pub[PUB_PUBID]
                pub_ids.append(pub_id)
                pub_type = pub[PUB_CTYPE]
                pub_types[pub_id] = pub_type

        referral_titles = {}
        if not pub_ids:
                return referral_titles
        pub_ids_string = list_to_in_clause(pub_ids)
	query = """select pc.pub_id, t.*
                   from pub_content pc, titles t
                   where pc.pub_id in (%s)
                   and pc.title_id = t.title_id""" % pub_ids_string
	db.query(query)
	result = db.store_result()
	if result.num_rows() < 1:
		return 0
	combined_data = result.fetch_row()
	while combined_data:
		pub_id = combined_data[0][0]
		title_data = combined_data[0][1:]
		title_ttype = title_data[TITLE_TTYPE]
		if pub_id not in referral_titles:
                        pub_type = pub_types[pub_id]
                        if title_ttype == pub_type:
                                referral_titles[pub_id] = title_data
                        # If "include_editors" was set to 1 and this pub is
                        # a magazine or fanzine, then return the first found EDITOR title
                        elif (include_editors == 1) and (pub_type in ('MAGAZINE', 'FANZINE')) and (title_ttype == 'EDITOR'):
                                referral_titles[pub_id] = title_data
		combined_data = result.fetch_row()
	return referral_titles

def SQLloadTransLegalNames(author_id):
	query = "select trans_legal_name from trans_legal_names where author_id='%d'" % int(author_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLloadWebpages(author_id):
	query = "select url from webpages where author_id='%d'" % (author_id)
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLloadPublisherWebpages(publisher_id):
	query = "select url from webpages where publisher_id='%d'" % (publisher_id)
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLloadTransPubSeriesNames(pub_series_id):
	query = "select trans_pub_series_name from trans_pub_series where pub_series_id=%d" % int(pub_series_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLLoadTransPubSeriesList(pub_series_ids):
        from library import list_to_in_clause
        if not pub_series_ids:
                return {}
        pub_series_ids_string = list_to_in_clause(pub_series_ids)
        query = """select p.pub_series_id, tps.trans_pub_series_name
                  from pub_series p, trans_pub_series tps
                  where p.pub_series_id = tps.pub_series_id
                  and p.pub_series_id in (%s)""" % pub_series_ids_string
        db.query(query)
        result = db.store_result()
        results = {}
        record = result.fetch_row()
        while record:
                  pub_series_id = record[0][0]
                  trans_pub_series_name = record[0][1]
                  if pub_series_id not in results:
                          results[pub_series_id] = []
                  results[pub_series_id].append(trans_pub_series_name)
                  record = result.fetch_row()
        return results

def SQLloadTransPublisherNames(publisher_id):
	query = "select trans_publisher_name from trans_publisher where publisher_id=%d" % int(publisher_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLLoadTransPublisherList(publisher_ids):
        from library import list_to_in_clause
        if not publisher_ids:
                return {}
        publisher_ids_string = list_to_in_clause(publisher_ids)
        query = """select p.publisher_id, tp.trans_publisher_name
                  from publishers p, trans_publisher tp
                  where p.publisher_id = tp.publisher_id
                  and p.publisher_id in (%s)""" % publisher_ids_string
        db.query(query)
        result = db.store_result()
        results = {}
        record = result.fetch_row()
        while record:
                  publisher_id = record[0][0]
                  trans_publisher_name = record[0][1]
                  if publisher_id not in results:
                          results[publisher_id] = []
                  results[publisher_id].append(trans_publisher_name)
                  record = result.fetch_row()
        return results

def SQLloadTransSeriesNames(series_id):
	query = "select trans_series_name from trans_series where series_id=%d" % int(series_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLloadTransTitles(title_id):
	query = "select trans_title_title from trans_titles where title_id=%d" % int(title_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLLoadTransTitlesList(title_ids):
        from library import list_to_in_clause
        if not title_ids:
                return {}
        title_ids_string = list_to_in_clause(title_ids)
        query = """select t.title_id, tt.trans_title_title
                  from titles t, trans_titles tt
                  where t.title_id = tt.title_id
                  and t.title_id in (%s)""" % title_ids_string
        db.query(query)
        result = db.store_result()
        results = {}
        record = result.fetch_row()
        while record:
                  title_id = record[0][0]
                  trans_title_title = record[0][1]
                  if title_id not in results:
                          results[title_id] = []
                  results[title_id].append(trans_title_title)
                  record = result.fetch_row()
        return results

def SQLloadTransAuthorNames(author_id):
	query = "select trans_author_name from trans_authors where author_id=%d" % int(author_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLLoadTransAuthorNamesList(author_ids):
        from library import list_to_in_clause
        if not author_ids:
                return {}
        author_ids_string = list_to_in_clause(author_ids)
        query = """select a.author_id, at.trans_author_name
                  from authors a, trans_authors at
                  where a.author_id = at.author_id
                  and a.author_id in (%s)""" % author_ids_string
        db.query(query)
        result = db.store_result()
        results = {}
        record = result.fetch_row()
        while record:
                  author_id = record[0][0]
                  trans_author_name = record[0][1]
                  if author_id not in results:
                          results[author_id] = []
                  results[author_id].append(trans_author_name)
                  record = result.fetch_row()
        return results

def SQLloadTransPubTitles(pub_id):
	query = "select trans_pub_title from trans_pubs where pub_id=%d" % int(pub_id)
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	results = []
	while row:
		results.append(row[0][0])
		row = result.fetch_row()
	return results

def SQLLoadTransPubTitlesList(pub_ids):
        from library import list_to_in_clause
        if not pub_ids:
                return {}
        pub_ids_string = list_to_in_clause(pub_ids)
        query = """select p.pub_id, tp.trans_pub_title
                  from pubs p, trans_pubs tp
                  where p.pub_id = tp.pub_id
                  and p.pub_id in (%s)""" % pub_ids_string
        db.query(query)
        result = db.store_result()
        results = {}
        record = result.fetch_row()
        while record:
                  pub_id = record[0][0]
                  trans_pub_title = record[0][1]
                  if pub_id not in results:
                          results[pub_id] = []
                  results[pub_id].append(trans_pub_title)
                  record = result.fetch_row()
        return results

def SQLloadPubSeriesWebpages(publisher_id):
	query = "select url from webpages where pub_series_id='%d'" % (publisher_id)
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLloadTitleWebpages(title_id):
	query = "select url from webpages where title_id=%d" % int(title_id)
	return OneField(query)

def SQLloadPubWebpages(pub_id):
	query = "select url from webpages where pub_id=%d" % int(pub_id)
	return OneField(query)

def SQLloadAwardTypeWebpages(award_type_id):
	query = "select url from webpages where award_type_id='%d'" % (int(award_type_id))
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLloadAwardCatWebpages(award_cat_id):
	query = "select url from webpages where award_cat_id='%d'" % (int(award_cat_id))
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLloadSeriesWebpages(series_id):
	query = "select url from webpages where series_id='%d'" % (int(series_id))
	db.query(query)
	result = db.store_result()
	webpage = result.fetch_row()
	results = []
	while webpage:
		results.append(webpage[0][0])
		webpage = result.fetch_row()
	return results

def SQLAuthorsBorn(date):
	query = """select * from authors
                where MONTH(author_birthdate)=MONTH('%s')
                and DAYOFMONTH(author_birthdate)=DAYOFMONTH('%s')
                order by author_birthdate""" % (date, date)
	return StandardQuery(query)

def SQLAuthorsDied(date):
	query = """select * from authors
                where MONTH(author_deathdate)=MONTH('%s')
                and DAYOFMONTH(author_deathdate)=DAYOFMONTH('%s')
                order by author_birthdate""" % (date, date)
	return StandardQuery(query)

def SQLgetUserName(userId):
	query = "select user_name from mw_user where user_id=%d" % int(userId)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		user = result.fetch_row()
		return user[0][0]
	else:
		return "UNKNOWN"

def SQLgetUserNameAndToken(userId):
	query = "select user_name, user_token from mw_user where user_id=%d" % int(userId)
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		user = result.fetch_row()
		return (user[0][0], user[0][1])
	else:
		return ('', '')

def SQLhasNewTalk(userId):
	query = "select 1 from dual where exists (select * from mw_user_newtalk where user_id=%d)" % int(userId)
	count = 0
	# The mw_user_newtalk table does not exist unless MediaWiki is installed,
	# so we trap the exception and treat it as no new messages.
	try:
		db.query(query)
		result = db.store_result()
		if result.num_rows() > 0:
			count = 1
	except:
		pass
	return count

def SQLgetTitle(titleId):
	query = "select title_title from titles where title_id=%d" % int(titleId)
	db.query(query)
	result = db.store_result()
	if result.num_rows():
		record = result.fetch_row()
		return(record[0][0])
	else:
		return ('')

def SQLgetPubTitle(pubId):
	query = "select pub_title from pubs where pub_id=%d" % int(pubId)
	db.query(query)
	result = db.store_result()
	if result.num_rows():
		record = result.fetch_row()
		return(record[0][0])
	else:
		return ('')

def SQLTitlesWithPubs(title_list):
        if not title_list:
                return []
        query = "select title_id from pub_content where title_id in (%s)" % title_list
        db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0][0])
		title = result.fetch_row()
	return results

def SQLisUserModerator(userId):
        query = "select * from mw_user_groups where ug_user='%d' and ug_group='sysop'" % (int(userId))
        db.query(query)
        result = db.store_result()
	if result.num_rows():
		return 1
	else:
		return 0

def SQLisUserBureaucrat(userId):
        query = "select * from mw_user_groups where ug_user='%d' and ug_group='bureaucrat'" % (int(userId))
        db.query(query)
        result = db.store_result()
	if result.num_rows():
		return 1
	else:
		return 0

def SQLisUserBot(userId):
        query = "select ug_group from mw_user_groups where ug_user=%d and ug_group='bot'" % int(userId)
        db.query(query)
        result = db.store_result()
	if result.num_rows():
		return 1
	else:
		return 0

def SQLWikiEditCount(submitter):
        # Retrieve the count of Wiki edits by the current submitter
       	query = "select user_editcount from mw_user where user_name='%s'" % (db.escape_string(submitter))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		editcount = record[0][0]
	else:
		editcount = 0
	return editcount

def SQLgetTitleVariants(title_id):
	query = "select * from titles where title_parent='%d' order by titles.title_copyright, titles.title_title" % (title_id)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	results = []
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLloadVTsForAuthor(author_id):
	query = """select t.* from titles t, canonical_author ca
                   where t.title_parent = ca.title_id
                   and ca.author_id = %d
                   and ca.ca_status = 1
                   order by t.title_copyright, t.title_title""" % int(author_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLloadVTsForTitleList(title_list):
	query = """select variant.* from titles variant, titles parent
                   where variant.title_parent = parent.title_id
                   and parent.title_id in (%s)
                   order by variant.title_copyright, variant.title_title""" % db.escape_string(title_list)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetSubmitterID(submitter, case_sensitive = 1):
        if case_sensitive:
                query = "select user_id from mw_user where user_name='%s'" % db.escape_string(submitter)
        else:
                # We have to use LOWER because user_name in mw_user collates using latin1_bin
                query = "select user_id from mw_user where LOWER(user_name)='%s'" % db.escape_string(submitter.lower())
        db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		userid =  record[0][0]
	else:
		userid =  0
	return(int(userid))

def SQLmarkInProgress(submission):
        update = "update submissions set sub_state='P' where sub_id=%d" %  int(submission)
        db.query(update)

def SQLGetPubContentList(pub_id):
        query = "select * from pub_content where pub_id=%d" % int(pub_id)
##	query = """select pc.* from pub_content pc, titles t
##                where pc.pub_id = %d
##                and pc.title_id = t.title_id
##                order by t.title_title""" % int(pub_id)
	return StandardQuery(query)

def SQLGetRefDetails():
	query = "select * from reference order by reference_id"
	return StandardQuery(query)

def SQLVerificationStatus(pub_id):
        if SQLPrimaryVerifiers(pub_id):
                return 1
	secondary_verifications = SQLSecondaryVerifications(pub_id)
	for verification in secondary_verifications:
		if verification[VERIF_STATUS] == 1:
                        return 2
	return 0

def SQLSecondaryVerifications(pub_id):
	query = "select * from verification where pub_id=%d" % int(pub_id)
	return StandardQuery(query)

def SQLActiveSecondaryVerifications(pub_id):
	query = """select v.user_id, v.ver_time, r.reference_label, r.reference_url
                   from verification v, reference r
                   where v.pub_id=%d
                   and v.ver_status = 1
                   and v.reference_id = r.reference_id
                   order by r.reference_id""" % int(pub_id)
	return StandardQuery(query)

def SQLPrimaryVerifiers(pub_id):
	query = """select u.user_id, u.user_name, pv.ver_time, pv.ver_transient
                from primary_verifications pv, mw_user u
                where pv.pub_id = %d and pv.user_id = u.user_id
                order by pv.ver_time""" % int(pub_id)
	return StandardQuery(query)

def SQLPrimaryVerStatus(pub_id, user_id):
        # Returns None if this user hasn't verified this publication;
        # returns 'permanent' or 'transient' otherwise
	query = """select ver_transient
                from primary_verifications pv
                where pub_id = %d and user_id = %d""" % (int(pub_id), int(user_id))
	results = StandardQuery(query)
	if not results:
                return None
        elif not results[0][0]:
                return 'permanent'
        else:
                return 'transient'

def SQLInsertPrimaryVerification(pub_id, transient, userid):
        if transient:
                insert = """insert into primary_verifications(pub_id, user_id, ver_time, ver_transient)
                            values(%d, %d, NOW(), %d)""" % (int(pub_id), int(userid), int(transient))
        else:
                insert = """insert into primary_verifications(pub_id, user_id, ver_time)
                            values(%d, %d, NOW())""" % (int(pub_id), int(userid))
	db.query(insert)
	return insert

def SQLGetInterviews(author_id, page_type):
	query = """select titles.* from titles, canonical_author
                 where titles.title_ttype='INTERVIEW'
                 and titles.title_id=canonical_author.title_id
                 and canonical_author.ca_status=2
                 and canonical_author.author_id=%d
                 and titles.title_parent=0 """ % int(author_id)
	if page_type == 'Alphabetical':
                query += 'order by titles.title_title'
        else:
                query += 'order by titles.title_copyright'
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLloadXML(recno):
	query = "select sub_data from submissions where sub_id=%d;" % (int(recno))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	xml = record[0][0]
	return(xml)

def SQLloadState(recno):
	query = "select sub_state from submissions where sub_id=%d" % int(recno)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	try:
                state = record[0][0]
        except:
                state = None
	return state

def SQLloadSubmission(sub_id):
	query = "select * from submissions where sub_id=%d" % int(sub_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	try:
                return record[0]
        except:
                return None

def SQLloadNextSubmission(sub_id, reviewer_id):
	query = """select * from submissions s
                where s.sub_state = 'N'
                and s.sub_holdid = 0
                and s.sub_id > %d
                and not exists (
                        select 1 from mw_user u, mw_user_groups groups
                        where s.sub_submitter != %d
                        and s.sub_submitter = u.user_id
                        and u.user_id = groups.ug_user
                        and groups.ug_group = 'sysop'
                        )
                order by s.sub_reviewed
                limit 1""" % (int(sub_id), int(reviewer_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	try:
                return record[0]
        except:
                return None

def SQLwikiLinkExists(namespace, title):
	if namespace == 'Author':
		num = 100
	elif namespace == 'Bio':
		num = 102
	elif namespace == 'Fanzine':
		num = 104
	elif namespace == 'Magazine':
		num = 106
	elif namespace == 'Publication':
		num = 108
	elif namespace == 'Publisher':
		num = 110
	elif namespace == 'Series':
		num = 112
	else:
		num = 0

	newlink = string.replace(title, ' ', '_')
	query = "select page_id from mw_page where page_title='%s' and page_namespace='%d';" % (db.escape_string(newlink), num)
	# Use try/except in case this ISFDB instance has no Wiki tables
	try:
                db.query(query)
        except:
                return 0

	result = db.store_result()
	if result.num_rows() > 0:
		return 1
	else:
		return 0

def SQLgetTitleTags(title_id):
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id) as xx from tag_mapping,tags where tags.tag_id=tag_mapping.tag_id and tag_mapping.title_id=%d group by tag_mapping.tag_id order by xx desc" % int(title_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetTagsByTitleForTitleList(title_ids, user_id):
        from library import list_to_in_clause
        if not title_ids:
                return {}
        title_list = list_to_in_clause(title_ids)
        query = """select distinct tm.title_id, t.*
                from tag_mapping tm, tags t
                where t.tag_id = tm.tag_id
                and tm.title_id in (%s)
                and (t.tag_status = 0 or tm.user_id = %d)
                """ % (title_list, int(user_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = {}
	while record:
                title_id = record[0][0]
                if title_id not in results:
                        results[title_id] = []
                results[title_id].append(record[0][1:])
		record = result.fetch_row()
	return results

def SQLgetTitleListTags(title_list, user_id):
        query = """select distinct tm.tag_id, tags.tag_name, count(tm.tag_id) as xx
                from tag_mapping tm, tags
                where tags.tag_id=tm.tag_id and tm.title_id in (%s)
                and (tags.tag_status=0 or tm.user_id=%d)
                group by tm.tag_id order by xx desc""" % (db.escape_string(title_list), int(user_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetUsersForTag(tag_id):
	query = "select distinct tag_mapping.user_id, count(tag_mapping.user_id) as xx, user_name from"
	query += " tag_mapping, mw_user where tag_id=%d and mw_user.user_id=tag_mapping.user_id" % (int(tag_id))
	query += " group by tag_mapping.user_id order by xx desc;"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetTitlesForAuthorAndTag(tag_id, author_id):
	query = "select distinct titles.title_copyright, titles.title_title, tag_mapping.title_id"
	query += " from tag_mapping, titles, authors, canonical_author where tag_mapping.tag_id='%d' and titles.title_id=tag_mapping.title_id" % int(tag_id)
	query += " and authors.author_id=canonical_author.author_id and canonical_author.title_id=tag_mapping.title_id and canonical_author.ca_status=1"
	query += " and canonical_author.author_id=%d order by YEAR(titles.title_copyright) desc, titles.title_title" % int(author_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetTitlesForTag(tag_id, start):
	query = """select distinct t.* from tag_mapping tm, titles t
                 where tm.tag_id=%d and t.title_id=tm.title_id
                 order by YEAR(t.title_copyright) desc, t.title_title
                 limit %d, 101
                 """ % (int(tag_id), int(start))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetTitlesForTagForUser(tag_id, user_id, start):
	query = """select t.* from tag_mapping tm, titles t
                 where tm.tag_id=%d and tm.user_id=%d and t.title_id=tm.title_id
                 order by YEAR(t.title_copyright) desc, t.title_title
                 limit %d, 101
                 """ % (int(tag_id), int(user_id), int(start))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetAllTitleTags(title_id, parent_id, user_id):
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id)"
        query += " as xx from tag_mapping,tags where tags.tag_id=tag_mapping.tag_id and"
        query += " (tag_mapping.title_id=%d or tag_mapping.title_id=%d)" % (int(title_id), int(parent_id))
        query += " and (tags.tag_status=0 or tag_mapping.user_id=%d)" % user_id
        query += " group by tag_mapping.tag_id order by xx desc"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetTitleTagsByUser(title_id):
        query = """select tm.tag_id, t.tag_name, tm.user_id, tm.tagmap_id
                from tag_mapping tm, tags t
                where t.tag_id = tm.tag_id
                and tm.title_id = %d
                order by t.tag_name""" % int(title_id)
        return StandardQuery(query)

def SQLgetTitleByTagId(tagmap_id):
        query = """select title_id from tag_mapping where tagmap_id = %d""" % int(tagmap_id)
        return OneField(query)

def SQLgetUserTags(title_id, user_id):
        query = "select tags.tag_name from tags,tag_mapping where tag_mapping.title_id='%d' and tag_mapping.user_id='%d' and tag_mapping.tag_id=tags.tag_id;" % (int(title_id), int(user_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0][0])
		record = result.fetch_row()
	return results

def SQLGetTagById(tag_id):
	query = "select * from tags where tag_id = '%d'" % (int(tag_id))
	db.query(query)
	result = db.store_result()
	if result.num_rows() > 0:
		tag = result.fetch_row()
		return tag[0]
	else:
		return 0

def SQLgetPopularTags():
	query = "select distinct tags.tag_id,tags.tag_name from tags,tag_mapping where tag_mapping.title_id='%d' and tag_mapping.tag_id=tags.tag_id;" % int(title_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLgetAuthorTags(author_id, user_id):
        query = "select distinct tag_mapping.tag_id,tags.tag_name,count(tag_mapping.tag_id) as xx"
        query += " from tag_mapping,tags,canonical_author where canonical_author.author_id=%d and" % int(author_id)
        query += " canonical_author.title_id=tag_mapping.title_id and tags.tag_id=tag_mapping.tag_id"
        query += " and (tags.tag_status=0 or tag_mapping.user_id=%d)" % user_id
        query += " group by tag_mapping.tag_id order by xx desc"
        db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLsearchTags(tag):
	query = "select * from tags where tag_name like '%%%s%%' order by tag_name" % (db.escape_string(tag))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLaddTagToTitle(tag, title_id, user_id):
        print_string = []
        query = "select tag_id from tags where tag_name='%s'" % (db.escape_string(tag))
        db.query(query)
        result = db.store_result()
        if result.num_rows() < 1:
                update = "insert into tags(tag_name) values('%s')" % (db.escape_string(tag))
                print_string.append(update)
                db.query(update)
                tag_id = db.insert_id()
        else:
                record = result.fetch_row()
                tag_id = int(record[0][0])

        update = 'insert into tag_mapping(tag_id, title_id, user_id) values(%d,%d,%d)' % (int(tag_id), int(title_id), int(user_id))
        print_string.append(update)
        db.query(update)
        return print_string

def SQLDeleteDuplicateTags(title_id):
        query = "select tag_id, title_id, user_id, count(*) as xx from tag_mapping where title_id=%d group by tag_id,title_id,user_id having xx >1" % (int(title_id))
        db.query(query)
        result = db.store_result()
	record = result.fetch_row()
        tags = []
        while record:
		tags.append(record[0])
		record = result.fetch_row()
	for tag in tags:
                tag_id = tag[0]
                title_id = tag[1]
                user_id = tag[2]
                update = "delete from tag_mapping where tag_id=%d and title_id=%d and user_id=%d" % (int(tag_id), int(title_id), int(user_id))
                db.query(update)
                update = "insert into tag_mapping(tag_id, title_id, user_id) values(%d, %d, %d)" % (int(tag_id), int(title_id), int(user_id))
                db.query(update)

def SQLDeleteTagMapping(tagmap_id):
        update = "delete from tag_mapping where tagmap_id = %d" % int(tagmap_id)
	db.query(update)
	SQLDeteleOrphanTags()
        
def SQLDeteleOrphanTags():
	update = 'delete from tags where NOT EXISTS (select 1 from tag_mapping where tags.tag_id = tag_mapping.tag_id)'
        db.query(update)

def SQLFindReviewParent(title, author):
	# Attempt to find Book-Length Works first:
	query =  "select titles.* "
	query += "from titles,canonical_author,authors "
	query += "where titles.title_ttype IN ('ANTHOLOGY','COLLECTION','NOVEL','NONFICTION','OMNIBUS') "
	query += "and titles.title_title='%s' "  % (db.escape_string(title))
	query += "and canonical_author.title_id=titles.title_id "
	query += "and canonical_author.author_id=authors.author_id "
	query += "and authors.author_canonical='%s'" % (db.escape_string(author))
	db.query(query)
	result = db.store_result()
	title2 = result.fetch_row()
	results = []
	if title2:
		return(title2[0][0])
	else:
		# Attempt to find Shortfiction second
		query =  "select titles.* "
		query += "from titles,canonical_author,authors "
		query += "where titles.title_ttype = 'SHORTFICTION' "
		query += "and titles.title_title='%s' "  % (db.escape_string(title))
		query += "and canonical_author.title_id=titles.title_id "
		query += "and canonical_author.author_id=authors.author_id "
		query += "and authors.author_canonical='%s'" % (db.escape_string(author))
		db.query(query)
		result = db.store_result()
		title2 = result.fetch_row()
		results = []
		if title2:
			return(title2[0][0])
		else:
			return(0)

def SQLloadTitleReviews(title_id):
	# 0 has special meaning as value of the title_parent field
	if title_id==0:
		return([])

	############################################################
	# Get variant titles including canonical one
	# as a string suitable for SQL's IN (...) clause
	############################################################
	query = "select title_id from titles where title_id='%d' or title_parent='%d'" % (title_id, title_id)
	db.query(query)
	result0 = db.store_result()
	title = result0.fetch_row()
	if not title:
		return([])
	title_set = ""
	counter = 0
	while title:
		if counter:
			title_set += ", "
		title_set += str(title[0][0])
		title = result0.fetch_row()
		counter += 1

	############################################################
	# Get the list of review titles for this set
	############################################################
	query = "select distinct review_id from title_relationships where title_id in (%s)" % (db.escape_string(title_set))
	db.query(query)
	result = db.store_result()
	review_id = result.fetch_row()
	results = []
	while review_id:
		query = "select * from titles where title_id='%d'" % (review_id[0])
		db.query(query)
		res2 = db.store_result()
		review = res2.fetch_row()
		results.append(review[0])
		review_id = result.fetch_row()
	return results

def SQLfindReviewedTitle(review_id):
	query = "select title_id from title_relationships where review_id='%d'" % (review_id)
	db.query(query)
	result = db.store_result()
	title_id = result.fetch_row()
	if title_id:
		return(title_id[0][0])
	else:
		return(0)

def SQLGetPseudIdByAuthorAndPseud(parent,pseudonym):
        query = "select pseudo_id from pseudonyms where author_id = %d and pseudonym = %d order by pseudo_id desc limit 1" % (int(parent), int(pseudonym))
	db.query(query)
	result = db.store_result()
	pub = result.fetch_row()
	if pub:
		return pub[0][0]
	else:
                return []

def LoadWebSites(isbn, user_id = None, format = None):
        from urlparse import urlparse
        from library import toISBN10, toISBN13
        from isbn import convertISBN
        newisbn = string.replace(isbn, '-', '')
        newisbn = string.replace(newisbn, ' ', '')
        isbn13 = toISBN13(newisbn)
        isbn10 = toISBN10(newisbn)

        if user_id:
                query = """select w.site_url, w.site_name, w.site_isbn13
                         from websites w
                         where exists(select 1 from user_sites u
                          where u.user_id = %d
                          and u.site_id = w.site_id
                          and u.user_choice = 1)
                         or not exists(select 1 from user_sites u
                          where u.user_id = %d
                          and u.site_id = w.site_id)
                          order by w.site_name""" % (int(user_id), int(user_id))
        else:
                query = "select site_url, site_name, site_isbn13 from websites order by site_name"

	db.query(query)
	result = db.store_result()
	site = result.fetch_row()
        results = []
        while site:
                site_url = site[0][0]
                site_name = site[0][1]
                site_isbn13 = site[0][2]
                # For Amazon ebook links and 979 ISBN-13s, link to the Amazon search
                # page because direct links using ISBN-10s do not work
                if site_name[0:6] == 'Amazon' and (format == 'ebook' or (len(newisbn) == 13 and isbn13[:3] == '979')):
                        parsed_url = urlparse(site_url)
                        scheme = parsed_url[0]
                        # Extract the "domain:port" part of the URL
                        netloc = parsed_url[1]
                        url_string = '%s://%s/s?search-alias=stripbooks&field-isbn=%s' % (scheme, netloc, isbn13)
                        if site_name == 'Amazon US':
                                url_string += '&tag=isfdb-20'
                        elif site_name == 'Amazon UK':
                                url_string += '&tag=isfdb-21'
                # European Library requires ISBNs in search strings to be exact, i.e. ISBN-10s for
                # pre-2008 books and ISBN-13s for post-2008 books. Also, some of their records
                # include dashes and some don't, so we need to search for both forms of the ISBN.
                elif 'European Library' in site_name:
                        url_string = string.replace(site_url, "%s", newisbn + '+or+' + convertISBN(newisbn))
                # Some sites like Open Library and BnF require ISBNs in search strings
                # to be exact, i.e. ISBN-10s for pre-2008 books and ISBN-13s for post-2008 books.
                elif site_isbn13 == 2:
                        url_string = string.replace(site_url, "%s", newisbn)
                elif site_isbn13 == 1:
                        url_string = string.replace(site_url,"%s",isbn13)
                else:
                        url_string = string.replace(site_url,"%s",isbn10)
                url_string = string.replace(url_string, '&', '&amp;')
                results.append((site_name, url_string),)
		site = result.fetch_row()

	return results 

def SQLGetSubmissionHoldId(submission):
	query = "select sub_holdid from submissions where sub_id='%d';" % (int(submission))
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
        hold_id = record[0][0]
        return hold_id

def SQLGetSubmitterId(submission):
	query = "select sub_submitter from submissions where sub_id='%d';" % (int(submission))
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
        submitter_id = record[0][0]
        return submitter_id

def SQLLoadUserPreferences(user_id):
	# Get the currently defined preferences for the logged-in user
	query = """select concise_disp, default_language, display_all_languages,
                covers_display, suppress_translation_warnings, suppress_bibliographic_warnings,
                cover_links_display, keep_spaces_in_searches, suppress_help_bubbles,
                suppress_awards, suppress_reviews, display_post_submission
                from user_preferences where user_id=%d""" % (int(user_id))
	db.query(query)
	result = db.store_result()
	# Set the default values to 0; set the default language to 17, i.e. "English"
	preferences = (0, 17, 'All', 0, 0, 0, 0, 0, 0, 0, 0, 0)
	if result.num_rows() > 0:
        	row = result.fetch_row()
        	# Temporarily convert the tuple returned by the query to a list
        	preferences = list(row[0])
                if not preferences[1]:
                        preferences[1] = 17
                # Convert the list back to a tuple
                preferences = tuple(preferences)
        return preferences

def SQLLoadUserLanguages(user_id):
        query = "select lang_id from user_languages where user_id = %d;" % int(user_id)
        db.query(query)
        result = db.store_result()
        languages = []
        record = result.fetch_row()
        while record:
                languages.append(record[0][0])
                record = result.fetch_row()
        return languages

def SQLGetLangIdByName(lang_name):
        query = "select lang_id from languages where lang_name ='%s'" % (db.escape_string(lang_name))
        db.query(query)
        res = db.store_result()
        lang_id = 0
        if res.num_rows():
                record = res.fetch_row()
                lang_id = record[0][0]
        return lang_id

def SQLGetLangByName(lang_name):
        query = "select lang_id from languages where lang_name ='%s'" % (db.escape_string(lang_name))
        db.query(query)
        res = db.store_result()
        lang_id = 0
        if res.num_rows():
                record = res.fetch_row()
                lang_id = record[0][0]
        return lang_id

def SQLUserPreferencesId(user_id):
        query = "select user_pref_id from user_preferences where user_id='%d'" % (int(user_id))
        db.query(query)
        result = db.store_result()
        if result.num_rows() < 1:
                return 0
        record = result.fetch_row()
        user_pref_id = int(record[0][0])
        return user_pref_id

def SQLUpdate_last_viewed_verified_pubs_DTS(user_id):
        # Update the "last viewed changed primary verified pubs report" DTS
        # and return the previous DTS
        query = "select last_viewed_ver_pubs from user_status where user_id=%d" % (int(user_id))
        db.query(query)
        result = db.store_result()
        if result.num_rows() < 1:
                previous_last_viewed = None
                update = """insert into user_status(user_id, last_viewed_ver_pubs)
                          values(%d, NOW())""" % int(user_id)
        else:
                previous_last_viewed = result.fetch_row()[0][0]
                update = """update user_status set last_viewed_ver_pubs = 
                          NOW() where user_id = %d""" % int(user_id)
        db.query(update)
        return previous_last_viewed

def SQLUpdate_last_changed_verified_pubs_DTS(user_id):
        query = "select user_id from user_status where user_id=%d" % (int(user_id))
        db.query(query)
        result = db.store_result()
        if result.num_rows() < 1:
                update = """insert into user_status(user_id, last_changed_ver_pubs)
                          values(%d, NOW())""" % int(user_id)
        else:
                update = """update user_status set last_changed_ver_pubs = 
                          NOW() where user_id = %d""" % int(user_id)
        db.query(update)

def SQLListAwardTypes():
        query = "select * from award_types order by award_type_name"
        db.query(query)
        result = db.store_result()
	results = []
	record = result.fetch_row()
	while record:
		results.append(record[0])
		record = result.fetch_row()
        return results

def SQLGetAwardTypeByCode(award_type_code):
        query = "select * from award_types where award_type_code='%s'" % (db.escape_string(award_type_code))
        db.query(query)
        result = db.store_result()
        award_type = []
        if result.num_rows() > 0:
                record = result.fetch_row()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeByName(award_type_name):
        query = "select * from award_types where award_type_name='%s'" % (db.escape_string(award_type_name))
        db.query(query)
        result = db.store_result()
        award_type = []
        if result.num_rows() > 0:
                record = result.fetch_row()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeByShortName(award_type_short_name):
        query = "select * from award_types where award_type_short_name='%s'" % (db.escape_string(award_type_short_name))
        db.query(query)
        result = db.store_result()
        award_type = []
        if result.num_rows() > 0:
                record = result.fetch_row()
                award_type = record[0]
        return award_type

def SQLGetAwardTypeById(award_type_id):
        query = "select * from award_types where award_type_id='%d'" % (int(award_type_id))
        db.query(query)
        result = db.store_result()
        award_type = []
        if result.num_rows() > 0:
                record = result.fetch_row()
                award_type = record[0]
        return award_type

def SQLGetSeriesByName(series_name):
        query = "select * from series where series_title='%s'" % (db.escape_string(series_name))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return 0

def SQLGetAwardYears(award_type_id):
        query = "select distinct award_year from awards where award_type_id=%d order by award_year" % (int(award_type_id))
	db.query(query)
        result = db.store_result()
	results = []
	record = result.fetch_row()
	while record:
		results.append(record[0][0])
		record = result.fetch_row()
        return results

def SQLGetAwardCategories(award_type_id):
        query = "select * from award_cats where award_cat_type_id=%d order by award_cat_name" % int(award_type_id)
	db.query(query)
        result = db.store_result()
	results = []
	record = result.fetch_row()
	while record:
		results.append(record[0])
		record = result.fetch_row()
        return results

def SQLGetAwardCatById(award_cat_id):
        query = "select * from award_cats where award_cat_id=%d" % int(award_cat_id)
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return ()

def SQLGetAwardCatByName(award_cat_name, award_cat_type_id):
        query = "select * from award_cats where award_cat_name='%s' and award_cat_type_id=%d" % (db.escape_string(award_cat_name), int(award_cat_type_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record:
		return record[0]
	else:
		return ()

def SQLSearchAwards(award):
	query = "select * from award_types where award_type_name like '%%%s%%' or award_type_short_name like '%%%s%%' order by award_type_short_name" % (db.escape_string(award), db.escape_string(award))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	results = []
	while record:
		results.append(record[0])
		record = result.fetch_row()
	return results

def SQLGetAwardCatBreakdown(award_type_id):
        query = """select c.award_cat_name, a.award_cat_id, c.award_cat_order,
                   sum(if(a.award_level='1',1,0)), count(a.award_id),
                   IF(c.award_cat_order IS NULL, 1, 0) AS isnull
                   from awards a, award_cats c
                   where a.award_cat_id = c.award_cat_id
                   and a.award_type_id = %d
                   group by a.award_cat_id
                   order by isnull, c.award_cat_order, c.award_cat_name
                   """  % int(award_type_id)
	db.query(query)
        result = db.store_result()
	results = []
	record = result.fetch_row()
	while record:
		results.append(record[0])
		record = result.fetch_row()
        return results

def SQLGetEmptyAwardCategories(award_type_id):
        query = """select *, IF(award_cat_order IS NULL, 1, 0) AS isnull from award_cats
                   where award_cat_type_id=%d
                   and NOT EXISTS
                     (select award_id from awards
                      where award_cat_id = award_cats.award_cat_id)
                   order by isnull, award_cat_order, award_cat_name
                   """ % int(award_type_id)
	db.query(query)
        result = db.store_result()
	results = []
	record = result.fetch_row()
	while record:
		results.append(record[0])
		record = result.fetch_row()
        return results
        
def SQLGetPageNumber(title_id, pub_id):
	query = 'select pubc_page from pub_content where title_id=%d and pub_id=%d' % (int(title_id), int(pub_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	try:
		return record[0][0]
	except:
		return 0

def SQLtransLegalNames(author_ids):
        from library import list_to_in_clause
        if not author_ids:
                return {}
        author_ids_string = list_to_in_clause(author_ids)
        query = """select a.author_id, t.trans_legal_name
                from authors a, trans_legal_names t
                where a.author_id = t.author_id
                and a.author_id in (%s)""" % author_ids_string
	db.query(query)
        result = db.store_result()
	results = {}
	record = result.fetch_row()
	while record:
                author_id = record[0][0]
                trans_legal_name = record[0][1]
                if author_id not in results:
                        results[author_id] = []
                results[author_id].append(trans_legal_name)
		record = result.fetch_row()
        return results

def SQLPubArtists(pubid):
        titles = SQLloadTitlesXBT(pubid)
        results = []
        for title in titles:
                if title[TITLE_TTYPE] == 'COVERART':
        		authors = SQLTitleAuthors(title[TITLE_PUBID])
        		for author in authors:
                		results.append(author)
	return results

def SQLPubCovers(pubid):
	query = """select t.* from titles t, pub_content pc
                   where pc.pub_id=%d and pc.title_id = t.title_id
                   and t.title_ttype='COVERART'""" % int(pubid)
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	titles = []
	while title:
		titles.append(title[0])
		title = result.fetch_row()
	return titles

def SQLFindMonth(target):
	results = []
        query = "select * from titles where title_copyright like '%s%%' order by title_title" % (db.escape_string(target))
	db.query(query)
	result = db.store_result()
	title = result.fetch_row()
	while title:
		results.append(title[0])
		title = result.fetch_row()
	return results

def SQLChangedVerifications(user_id):
        import time
        # Returns 1 if one the logged-in user's primary verified publications has been changed by
        # another user since the logged-in user last looked at the report of changed verified pubs

        # Retrieve the "last viewed" and the "last changed" date/time stamps
        query = """select last_changed_ver_pubs, last_viewed_ver_pubs
                    from user_status where user_id = %d""" % int(user_id)
	db.query(query)
	result = db.store_result()
        # If the logged-in user has never checked this report and there are no changed verified pubs, return 0
        if not result.num_rows():
                return 0

        value = result.fetch_row()
        last_viewed = value[0][1]
        last_changed = value[0][0]
        # If none of the logged-in user's primary verified pubs have been changed, return 0
        if not last_changed:
                return 0
        # If some verified pubs have been changed but the user hasn't displayed the report yet,
        # return 1
        if not last_viewed:
                return 1
        # If a verified pub has been changed since the logged in user last checked the report,
        # return 1
        if last_changed > last_viewed:
                # If the logged-in user last checked the report before the last change, return 1
                return 1
        return 0

def SQLLastUserActivity(user_id):
        from datetime import datetime
        from calendar import timegm
        query = """select ver_time from primary_verifications
                where user_id = %d order by ver_time desc limit 1""" % int(user_id)
        results = StandardQuery(query)
        if results:
                primary_ver = results[0][0]
        else:
                primary_ver = ''

        query = """select ver_time from verification
                where user_id = %d order by ver_time desc limit 1""" % int(user_id)
        results = StandardQuery(query)
        if results:
                sec_ver = results[0][0]
        else:
                sec_ver = ''
        
        query = """select sub_time from submissions
                   where sub_submitter = %d and sub_state = 'I'
                   order by sub_reviewed desc limit 1""" % int(user_id)
        results = StandardQuery(query)
        if results:
                last_submission = results[0][0]
        else:
                last_submission = ''

	# The mw_revision table does not exist unless MediaWiki is installed,
	# so we trap the exception and treat it as no Wiki messages.
        last_wiki = ''
	try:
                query = "select max(rev_timestamp) from mw_revision where rev_user = %d" % int(user_id)
                results = StandardQuery(query)
                if results:
                        timestamp = results[0][0]
                        if timestamp:
                                year = timestamp[:4]
                                month = timestamp[4:6]
                                day = timestamp[6:8]
                                hours = timestamp[8:10]
                                minutes = timestamp[10:12]
                                seconds = timestamp[12:14]
                                wiki_utc = datetime.strptime('%s-%s-%s %s:%s:%s' % (year, month, day, hours, minutes, seconds), '%Y-%m-%d %H:%M:%S')
                                timestamp = timegm(wiki_utc.timetuple())
                                last_wiki = datetime.fromtimestamp(timestamp)
	except:
		pass

        last_activity = primary_ver
        if sec_ver:
                if not last_activity:
                        last_activity = sec_ver
                elif sec_ver > last_activity:
                        last_activity = sec_ver
        if last_submission:
                if not last_activity:
                        last_activity = last_submission
                elif last_submission > last_activity:
                        last_activity = last_submission
        if last_wiki:
                if not last_activity:
                        last_activity = last_wiki
                elif last_wiki > last_activity:
                        last_activity = last_wiki

        if not last_activity:
                return None
        else:
                return last_activity.date()

def SQLLoadIdentifierTypes():
        # Returns a dictionary of all supported external identifier types
        # The dictionary structure is:
        #       results[type_number] = (type_name, type_full_name)
        query = "select * from identifier_types"
        type_list = StandardQuery(query)
        results = {}
        for id_type in type_list:
                type_number = id_type[IDTYPE_ID]
                type_name = id_type[IDTYPE_NAME]
                type_full_name = id_type[IDTYPE_FULL_NAME]
                results[type_number] = (type_name, type_full_name)
        return results

def SQLLoadIdentifiers(pub_id):
        query = "select * from identifiers where pub_id = %d" % int(pub_id)
        return StandardQuery(query)

def SQLLoadIdentifierSites():
        query = "select * from identifier_sites order by site_position, site_name"
        return StandardQuery(query)

def SQLFindPubByExternalID(id_type, id_value):
        id_value = id_value.replace('*','%')
        query = """select p.* from pubs p, identifiers id
                   where p.pub_id = id.pub_id
                   and id.identifier_type_id = %d
                   and id.identifier_value like '%s'""" % (int(id_type), db.escape_string(id_value))
        return StandardQuery(query)

def SQLLoadVotes(title_id, variants, user_id):
        from library import list_to_in_clause
        vote_count = 0
        average_vote = 0
        user_vote = 0
        query = "select count(vote_id), ROUND(AVG(rating),2) from votes where title_id = %d" % int(title_id)
        results = StandardQuery(query)
        if results[0][0]:
                vote_count = int(results[0][0])
                average_vote = float(results[0][1])
                query = "select rating from votes where title_id = %d and user_id = %d" % (int(title_id), int(user_id))
                results = StandardQuery(query)
                if results:
                        user_vote = int(results[0][0])

        composite_vote_count = vote_count
        composite_average_vote = average_vote
        if variants:
                variant_ids = []
                variant_ids.append(title_id)
                for variant in variants:
                        variant_id = variant[TITLE_PUBID]
                        variant_ids.append(variant_id)
                variant_clause = list_to_in_clause(variant_ids)
                query = "select count(vote_id), ROUND(AVG(rating),2) from votes where title_id in (%s)" % variant_clause
                results = StandardQuery(query)
                if results[0][0]:
                        composite_vote_count = int(results[0][0])
                        composite_average_vote = float(results[0][1])

        return (vote_count, average_vote, composite_vote_count, composite_average_vote, user_vote)

def SQLQueueSize():
        query = """select count(s.sub_id)
        from submissions s
        where s.sub_state='N'
        and s.sub_submitter!=13571
        and s.sub_holdid=0
        and not exists
        (select 1 from mw_user_groups g where g.ug_user=s.sub_submitter and g.ug_group='sysop')"""
        return StandardQuery(query)[0][0]

def SQLCountPubsForTitle(title_id):
        # Retrieve the number of pubs that this title exists in
        query = "select count(*) from pub_content where title_id = %d" % int(title_id)
        db.query(query)
        result = db.store_result()
        result_record = result.fetch_row()
        if result_record and result_record[0][0] > 1:
                return 1
        return 0

def SQLGetLangIdByTitle(title_id):
        query = "select title_language from titles where title_id=%d" % int(title_id)
        db.query(query)
        res = db.store_result()
        lang_id = ''
        if res.num_rows():
                record = res.fetch_row()
                lang_id = record[0][0]
        if lang_id is None:
                lang_id = ''
        return lang_id

def SQLDeletedPub(pubid):
        query = "select 1 from submissions where sub_type = 6 and affected_record_id = %d" % pubid
        db.query(query)
        result = db.store_result()
	if result.num_rows() > 0:
		return 1
	else:
		return 0
