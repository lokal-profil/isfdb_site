#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node

debug = 0

def dropCanonicalAuthors(db, DropId):

        ##############################################
        # STEP 1 - Get the list of current authors
        ##############################################
	query = "select author_id from canonical_author where title_id='%d'" % (int(DropId))
	db.query(query)
        result = db.store_result()
        author = result.fetch_row()
        author_list = []
        while author:
                author_list.append(author[0][0])
                author = result.fetch_row()

        ##############################################
        # STEP 2 - Delete the author/title mapping
        ##############################################
	delete = "delete from canonical_author where title_id='%d'" % (int(DropId))
	print "<li> ", delete
	if debug == 0:
		db.query(delete)

        ##############################################
        # STEP 2 - Delete the author/title mapping
        ##############################################
	for author_id in author_list:
		found = 0
        	for i in ['canonical_author', 'pub_authors']:
			query = 'select COUNT(author_id) from %s where author_id=%d' % (i, author_id)
			print "<li> ", query
			db.query(query)
			res = db.store_result()
			record = res.fetch_row()
			if record[0][0]:
				found = 1

		if found == 0:
			deleteFromAuthorTable(author_id)


def dropPubTitles(db, KeepId, DropId):
	update = "update pub_content set title_id=%d where title_id=%d" % (int(KeepId), int(DropId))
	print "<li> ", update
	if debug == 0:
		db.query(update)

def deleteTitle(db, id):
	delete = "delete from titles where title_id='%d'" % (int(id))
	print "<li> ", delete
	if debug == 0:
		db.query(delete)

def moveSeriesNumber(db, keep, drop):
	query = "select title_seriesnum from titles where title_id='%d'" % (int(drop))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	value = record[0][0]
	if value is not None:
                update = "update titles set title_seriesnum='%s' where title_id='%d'" % (db.escape_string(str(value)), int(keep))
	else:
                update = "update titles set title_seriesnum=NULL where title_id='%d'" % (int(keep))
	print "<li> ", update
	if debug == 0:
		db.query(update)
	query = "select title_seriesnum_2 from titles where title_id='%d'" % (int(drop))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	value = record[0][0]
	if value is not None:
                update = "update titles set title_seriesnum_2='%s' where title_id='%d'" % (db.escape_string(str(value)), int(keep))
	else:
                update = "update titles set title_seriesnum_2=NULL where title_id='%d'" % (int(keep))
	print "<li> ", update
	if debug == 0:
		db.query(update)

def moveTitleColumn(db, column, keep, drop):
	query = "select %s from titles where title_id='%d'" % (column, int(drop))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	value = record[0][0]
	if value is not None:
                update = "update titles set %s='%s' where title_id='%d'" % (column, db.escape_string(str(value)), int(keep))
	else:
                update = "update titles set %s=NULL where title_id='%d'" % (column, int(keep))
	print "<li> ", update
	if debug == 0:
		db.query(update)

def moveCanonicalAuthors(db, To, From):
	dropCanonicalAuthors(db, To)
	update = "update canonical_author set title_id=%d where title_id='%d'" % (int(To), int(From))
	print "<li> ", update
	if debug == 0:
		db.query(update)

def doColumn(db, KeepId, merge, label, column):
	id = GetElementValue(merge, label)
	if id and id != KeepId:
		moveTitleColumn(db, column, KeepId, id)

def retrieveNoteIds(field_name, KeepId, DropIds):
        from copy import deepcopy
        note_ids = []
        # Use deep copy to avoid modifying DropIds
        drop_ids = deepcopy(DropIds)
        # Add the Keep ID value to the list of Drop IDs
        drop_ids.append(int(KeepId))
        # Convert the list of IDs to a tuple and then to a MySQL-compatible IN clause
        drop_ids_string = str(tuple(drop_ids))
        query = "select %s from titles where title_id in %s" % (field_name, db.escape_string(drop_ids_string))
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                # Only append this Notes ID to the list if it is not NULL
                if record[0][0] and (record[0][0] not in note_ids):
                        note_ids.append(record[0][0])
                record = result.fetch_row()
        return note_ids

def dropNotes(db, KeepId, drop_ids, field_name):
        # If there are no IDs to delete from the Notes table, quit this function
        if not drop_ids:
                return
        # Retrieve the note/synopsis ID that is used by the kept title record post-merge
        query = "select %s from titles where title_id=%d" % (db.escape_string(field_name), int(KeepId))
        print "<li> ", query
        db.query(query)
        res = db.store_result()
        record = res.fetch_row()
        keep_note_id = record[0][0]

        # If the kept title record has a note/synopsis ID, then remove that ID
        # from the list of IDs that will be deleted from the notes table
        if keep_note_id and (keep_note_id in drop_ids):
                drop_ids.remove(keep_note_id)
        # If there are no IDs to delete from the Notes table, quit this function
        if not drop_ids:
                return
        # Build a MySQL-compatible IN clause
        in_clause = ''
        for drop_id in drop_ids:
                if not in_clause:
                        in_clause = str(drop_id)
                else:
                        in_clause += ",%s" % str(drop_id)
        update = "delete from notes where note_id in (%s)" % db.escape_string(in_clause)
        print "<li> ", update
        db.query(update)
        
########################################################################

RecordIds = []


def TitleMerge(db, doc):
	merge = doc.getElementsByTagName('TitleMerge')
	KeepId = GetElementValue(merge, 'KeepId')

	dropIds = doc.getElementsByTagName('DropId')
	for dropid in dropIds:
		RecordIds.append(int(dropid.firstChild.data))

        # Retrieve and save note IDs for the kept and all dropped titles
        note_ids = retrieveNoteIds('note_id', KeepId, RecordIds)

        # Retrieve and save synopsis IDs for the kept and all dropped titles
        synopsis_ids = retrieveNoteIds('title_synopsis', KeepId, RecordIds)
        
	doColumn(db, KeepId, merge, 'Title',      'title_title')
	doColumn(db, KeepId, merge, 'Translator', 'title_translator')
	doColumn(db, KeepId, merge, 'Synopsis',   'title_synopsis')
	doColumn(db, KeepId, merge, 'Note',       'note_id')
	doColumn(db, KeepId, merge, 'Series',     'series_id')
	doColumn(db, KeepId, merge, 'Year',       'title_copyright')
	doColumn(db, KeepId, merge, 'Storylen',   'title_storylen')
	doColumn(db, KeepId, merge, 'ContentIndicator', 'title_content')
	doColumn(db, KeepId, merge, 'Juvenile',   'title_jvn')
	doColumn(db, KeepId, merge, 'Novelization', 'title_nvz')
	doColumn(db, KeepId, merge, 'NonGenre',   'title_non_genre')
	doColumn(db, KeepId, merge, 'Graphic',    'title_graphic')
	doColumn(db, KeepId, merge, 'Language',   'title_language')
	doColumn(db, KeepId, merge, 'TitleType',  'title_ttype')
	doColumn(db, KeepId, merge, 'Parent',     'title_parent')

       	id = GetElementValue(merge, 'Seriesnum')
	if id and id != KeepId:
		moveSeriesNumber(db, KeepId, id)

	id = GetElementValue(merge, 'Author')
	if id and id != KeepId:
		moveCanonicalAuthors(db, KeepId, id)

        dropNotes(db, KeepId, note_ids, 'note_id')
        dropNotes(db, KeepId, synopsis_ids, 'title_synopsis')

        kept_title = SQLloadTitle(KeepId)
        if kept_title[TITLE_STORYLEN] and kept_title[TITLE_TTYPE] != 'SHORTFICTION':
                update = "update titles set title_storylen = NULL where title_id = %d" % int(KeepId)
                print "<li> ", update
	        db.query(update)

	for index in range(len(RecordIds)):
		dropCanonicalAuthors(db, RecordIds[index])
		dropPubTitles(db, KeepId, RecordIds[index])
		
		# Find webpages for dropped title
		query = "select webpage_id, url from webpages where title_id='%d'" % (int(RecordIds[index]))
	        db.query(query)
        	result = db.store_result()
       		record = result.fetch_row()
		while record:
			webpage_id = record[0][0]
			webpage_url = record[0][1]
			query2 = "select webpage_id from webpages where title_id='%d' and url='%s'" %  (int(KeepId), db.escape_string(webpage_url))
	        	db.query(query2)
        		result2 = db.store_result()
			if result2.num_rows() > 0:
				# Already exists, so delete the spare
				delete = "delete from webpages where webpage_id='%d'" % (int(webpage_id))
				print "<li> ", delete
				if debug == 0:
					db.query(delete)
			else:
				# Move webpage
				update = "update webpages set title_id='%d' where webpage_id='%d'" % (int(KeepId), int(webpage_id))
				print "<li> ", update
				if debug == 0:
					db.query(update)
			record = result.fetch_row()

		# Find transliterated titles for dropped title
		query = "select trans_title_id, trans_title_title from trans_titles where title_id=%d" % (int(RecordIds[index]))
	        db.query(query)
        	result = db.store_result()
       		record = result.fetch_row()
		while record:
			trans_title_id = record[0][0]
			trans_title_title = record[0][1]
			query2 = """select trans_title_id from trans_titles
                                  where title_id=%d and trans_title_title='%s'""" %  (int(KeepId), db.escape_string(trans_title_title))
	        	db.query(query2)
        		result2 = db.store_result()
			if result2.num_rows() > 0:
				# Already exists, so delete the spare
				delete = "delete from trans_titles where trans_title_id=%d" % int(trans_title_id)
				print "<li> ", delete
				if debug == 0:
					db.query(delete)
			else:
				# Move webpage
				update = "update trans_titles set title_id=%d where trans_title_id=%d" % (int(KeepId), int(trans_title_id))
				print "<li> ", update
				if debug == 0:
					db.query(update)
			record = result.fetch_row()

		deleteTitle(db, RecordIds[index])

		######################################################
		# Fixup any awards records to point to the new title
		######################################################
		update = "update title_awards set title_id=%d where title_id=%d" % (int(KeepId), int(RecordIds[index]))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		######################################################
		# Fixup any variant title records to point to the new title
		######################################################
		update = "update titles set title_parent=%d where title_parent=%d" % (int(KeepId), int(RecordIds[index]))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		######################################################
		# Fixup any vote records to point to the new title
		######################################################
		update = "update votes set title_id=%d where title_id=%d" % (int(KeepId), int(RecordIds[index]))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		######################################################
		# Fixup any tag records to point to the new title
		######################################################
		update = "update tag_mapping set title_id=%d where title_id=%d" % (int(KeepId), int(RecordIds[index]))
		print "<li> ", update
		if debug == 0:
			db.query(update)
		
		# Delete any duplicate tags that may have been created due to the merge
		SQLDeleteDuplicateTags(KeepId)

		######################################################
		# Fixup any review relationship records to point to the new title
		######################################################
		update = "update title_relationships set title_id=%d where title_id=%d" % (int(KeepId), int(RecordIds[index]))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		######################################################
		# When merging reviews, keep just one relationship record
		######################################################
		update = "delete from title_relationships where review_id=%d" % int(RecordIds[index])
		print "<li> ", update
		if debug == 0:
			db.query(update)

		######################################################
		# XXX - views
		######################################################

	return KeepId


if __name__ == '__main__':

	PrintPreMod('Title Merge - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
	if doc.getElementsByTagName('TitleMerge'):
		merge = doc.getElementsByTagName('TitleMerge')
		if merge:
			MergedTitle = TitleMerge(db, doc)
			submitter = GetElementValue(merge, 'Submitter')
			if debug == 0:
        			markIntegrated(db, submission, MergedTitle)

	print '[<a href="http:/' +HTFAKE+ '/edit/edittitle.cgi?%d">Edit This Title</a>]' % (int(MergedTitle))
	print '[<a href="http:/' +HTFAKE+ '/title.cgi?%d">View This Title</a>]' % (int(MergedTitle))

	print "<hr>"

	PrintPostMod(0)
