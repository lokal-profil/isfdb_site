#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2020   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import MySQLdb
import string
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from common import *
from library import *

debug = 0


def UpdateTitleColumn(doc, tag, column, id):
	value = GetElementValue(doc, tag)
	if TagPresent(doc, tag):
		value = XMLunescape(value)
		# For languages, get the language ID from its display name
		if tag == 'Language':
                        value = str(SQLGetLangByName(value))
		update = "update titles set %s='%s' where title_id=%d" % (db.escape_string(column), db.escape_string(value), int(id))
		print "<li> ", update
		if debug == 0:
        		db.query(update)

def UpdateSeries(ChildRecord, child_data, ParentRecord):
        update = "update titles set series_id=%d where title_id=%d" % (int(child_data[TITLE_SERIES]), int(ParentRecord))
        print "<li> ", update
        if debug == 0:
                db.query(update)
        DeleteSeries(ChildRecord)

def DeleteSeries(ChildRecord):
        #Clear the series name in the child title record
        update = "update titles set series_id=NULL where title_id=%d" % int(ChildRecord)
        print "<li> ", update
        if debug == 0:
                db.query(update)

def UpdateSeriesNum(ChildRecord, child_data, ParentRecord):
        if child_data[TITLE_SERIESNUM] is None:
                update = "update titles set title_seriesnum=NULL where title_id=%d" % int(ParentRecord)
        else:
                update = "update titles set title_seriesnum=%d where title_id=%d" % (int(child_data[TITLE_SERIESNUM]), int(ParentRecord))
        print "<li> ", update
        if debug == 0:
                db.query(update)

        if child_data[TITLE_SERIESNUM_2] is None:
                update = "update titles set title_seriesnum_2=NULL where title_id=%d" % int(ParentRecord)
        else:
                update = "update titles set title_seriesnum_2='%s' where title_id=%d" % (db.escape_string(child_data[TITLE_SERIESNUM_2]), int(ParentRecord))
        print "<li> ", update
        if debug == 0:
                db.query(update)
        DeleteSeriesNumber(ChildRecord)

def DeleteSeriesNumber(ChildRecord):
        #Clear the series number fields in the child title record
        update = "update titles set title_seriesnum=NULL where title_id=%d" % int(ChildRecord)
        print "<li> ", update
        if debug == 0:
                db.query(update)

        update = "update titles set title_seriesnum_2=NULL where title_id=%d" % int(ChildRecord)
        print "<li> ", update
        if debug == 0:
                db.query(update)

def UpdateTags(ChildRecord, ParentRecord):
        update = "update tag_mapping set title_id=%d where title_id=%d" % (int(ParentRecord), int(ChildRecord))
        print "<li> ", update
        if debug == 0:
                db.query(update)

def DoSubmission(db, submission):
        ParentRecord = 0
        ChildRecord = 0
	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
	if doc.getElementsByTagName('MakeVariant'):
		merge = doc.getElementsByTagName('MakeVariant')
		ChildRecord = GetElementValue(merge, 'Record')
                child_data = SQLloadTitle(ChildRecord)

		print "<ul>"
		if TagPresent(merge, 'Parent'):
			ParentRecord = int(GetElementValue(merge, 'Parent'))
			parent_data = SQLloadTitle(ParentRecord)
                        
                        if parent_data:
                                if child_data[TITLE_SERIES]:
                                        # If the parent title is already in a Series, DELETE 
                                        # the child's series AND the child's series number
                                        if parent_data[TITLE_SERIES]:
                                                DeleteSeries(ChildRecord)
                                                DeleteSeriesNumber(ChildRecord)
                                        # If the parent title is not in a Series, then MOVE the Series name
                                        # AND the Series number from the child record to the parent record
                                        else:
                                                UpdateSeries(ChildRecord, child_data, ParentRecord)
                                                UpdateSeriesNum(ChildRecord, child_data, ParentRecord)
			# Move any Tags to Parent, if parent exists
			if ParentRecord > 0:
				UpdateTags(ChildRecord, ParentRecord)
		else:
			##########################################################
			# TITLE
			##########################################################
			query = "insert into titles(title_title) values('xxx');"
			print "<li> ", query
			if debug == 0:
				db.query(query)
			ParentRecord = db.insert_id()
			UpdateTitleColumn(merge, 'Title',     'title_title',     ParentRecord)
			
                        value = GetElementValue(merge, 'TransTitles')
                        if value:
                                trans_titles = doc.getElementsByTagName('TransTitle')
                                for trans_title in trans_titles:
                                        title_value = XMLunescape(trans_title.firstChild.data.encode('iso-8859-1'))
                                        update = """insert into trans_titles(title_id, trans_title_title)
                                                    values(%d, '%s')""" % (int(ParentRecord), db.escape_string(title_value))
                                        print "<li> ", update
                                        if debug == 0:
                                                db.query(update)
			UpdateTitleColumn(merge, 'Year',      'title_copyright', ParentRecord)
			UpdateTitleColumn(merge, 'TitleType', 'title_ttype',     ParentRecord)
			UpdateTitleColumn(merge, 'Language',  'title_language',  ParentRecord)

			#Copy the "storylen" value from the child record to the new parent record
                        storylen = child_data[TITLE_STORYLEN]
                        if storylen:
                                update = "update titles set title_storylen='%s' where title_id=%d" % (db.escape_string(storylen), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)

			#Copy the "content" value from the child record to the new parent record
                        content = child_data[TITLE_CONTENT]
                        if content:
                                update = "update titles set title_content='%s' where title_id=%d" % (db.escape_string(content), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)

			#Copy the "juvenile" value from the child record to the new parent record
                        juvenile = child_data[TITLE_JVN]
                        if juvenile:
                                update = "update titles set title_jvn='%s' where title_id=%d" % (db.escape_string(juvenile), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)

			#Copy the "novelization" value from the child record to the new parent record
                        novelization = child_data[TITLE_NVZ]
                        if novelization:
                                update = "update titles set title_nvz='%s' where title_id=%d" % (db.escape_string(novelization), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)

			#Copy the "Non-Genre" value from the child record to the new parent record
                        nongenre = child_data[TITLE_NON_GENRE]
                        if nongenre:
                                update = "update titles set title_non_genre='%s' where title_id=%d" % (db.escape_string(nongenre), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)
                        
			#Copy the "Graphic" value from the child record to the new parent record
                        graphic = child_data[TITLE_GRAPHIC]
                        if graphic:
                                update = "update titles set title_graphic='%s' where title_id=%d" % (db.escape_string(graphic), int(ParentRecord))
                                print "<li> ", update
                                if debug == 0:
                                        db.query(update)

                        #Move the Series name from the child record to the new parent record
                        if child_data[TITLE_SERIES]:
                                UpdateSeries(ChildRecord, child_data, ParentRecord)
                        
                        #Move the Series number from the child record to the new parent record
                        if child_data[TITLE_SERIESNUM] is not None:
                                UpdateSeriesNum(ChildRecord, child_data, ParentRecord)

			# Move any Tags to Parent
			UpdateTags(ChildRecord, ParentRecord)

			##########################################################
			# TITLE AUTHORS
			##########################################################
			value = GetElementValue(merge, 'Authors')
			if value:
				authors = doc.getElementsByTagName('Author')
				for author in authors:
					data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
					addTitleAuthor(data, ParentRecord, 'CANONICAL')

		update = "update titles set title_parent=%d where title_id=%d" % (int(ParentRecord), int(ChildRecord))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		########################################################## 	 
		#  REVIEWED TITLE AUTHORS AND INTERVIEWEES 	 
		########################################################## 	 
		value = GetElementValue(merge, 'TitleType')
		if value == 'REVIEW':
			insert = "insert into canonical_author (title_id, author_id, ca_status) \
                                select %d, author_id, 3 from canonical_author where title_id = %d \
                                and ca_status = 3" % (int(ParentRecord), int(ChildRecord))
			print "<li> ", insert
			if debug == 0:
				db.query(insert)
		elif value == 'INTERVIEW':
			insert = "insert into canonical_author (title_id, author_id, ca_status) \
                                select %d, author_id, 2 from canonical_author where title_id = %d \
                                and ca_status = 2" % (int(ParentRecord), int(ChildRecord))
			print "<li> ", insert
			if debug == 0:
				db.query(insert)

		###################################################################
		# Relink any grandchildren variants from the child to the parent
		###################################################################
		query = "select title_id from titles where title_parent=%d" % (int(ChildRecord))
        	db.query(query)
        	res2 = db.store_result()
        	rec2 = res2.fetch_row()
		while rec2:
			grandchild_id = int(rec2[0][0])
			update = "update titles set title_parent=%d where title_id=%d" % (int(ParentRecord), grandchild_id)
			print "<li> ", update
			if debug == 0:
				db.query(update)
        		rec2 = res2.fetch_row()

		submitter = GetElementValue(merge, 'Submitter')
		if debug == 0:
			markIntegrated(db, submission, ChildRecord)
	return (ParentRecord, ChildRecord)


if __name__ == '__main__':

        PrintPreMod('Make Variant - SQL Statements')
        PrintNavBar()

	try:
		submission = int(sys.argv[1])
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

	(ParentRecord, ChildRecord) = DoSubmission(db, submission)

	if ParentRecord:
		print '[<a href="http:/%s/edit/edittitle.cgi?%d">Edit Parent Title</a>]' % (HTFAKE, int(ParentRecord))
		print '[<a href="http:/%s/title.cgi?%d">View Parent Title</a>]' % (HTFAKE, int(ParentRecord))
                print '[<a href="http:/%s/edit/find_title_dups.cgi?%s">Check Parent Title for Duplicates</a>]' % (HTFAKE, int(ParentRecord))
	if ChildRecord:
		print '[<a href="http:/%s/edit/edittitle.cgi?%d">Edit Variant Title</a>]' % (HTFAKE, int(ChildRecord))
		print '[<a href="http:/%s/title.cgi?%d">View Variant Title</a>]' % (HTFAKE, int(ChildRecord))
	print '<p>'

	PrintPostMod(0)
