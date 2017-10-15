#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2017   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.16 $
#     Date: $Date: 2017/01/16 23:16:12 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
from viewers import DisplayMergeTitles

records = []
MaxRecords = 0

def DoColumn(column, tag):
	if form.has_key(column):
		value = form[column].value
		index = int(value)-1
		retval = "    <%s>%d</%s>\n" % (tag, int(records[index]), tag)
		return retval
	else:
		return ""

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Title Merge Results'
        submission.cgi_script = 'tv_merge'
        submission.type = MOD_TITLE_MERGE
        submission.viewer = DisplayMergeTitles

	if not submission.user.id:
                submission.error()

	form = cgi.FieldStorage()

	# Retrieve all submitted IDs starting with "record" and sort them by number
	keys = []
	for key in form.keys():
                if key[0:6] != 'record':
                        continue
                key_number = int(key[6:])
                keys.append(key_number)

        # Retrieve the values of all submitted "record" IDs and put them into the "records" list
	targetID = 1000000000
        for key in keys:
		target = "record%d" % (key)
		records.append(int(form[target].value))
		if records[MaxRecords] < targetID:
			targetID = records[MaxRecords]
		MaxRecords += 1

	merge_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	merge_string += "<IsfdbSubmission>\n"
	merge_string += "  <TitleMerge>\n"

	if MaxRecords == 0:
		submission.error()

	index = 0
	while index < MaxRecords:
		if records[index] == targetID:
			merge_string += "    <KeepId>%d</KeepId>\n" % (records[index])
		else:
			merge_string += "    <DropId>%d</DropId>\n" % (records[index])
		index += 1

	titlename = SQLgetTitle(targetID)
	submitter = getSubmitter()
	merge_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submitter)))
	merge_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(titlename)))


	merge_string += DoColumn('title_title',     'Title')
	merge_string += DoColumn('title_author',    'Author')
	merge_string += DoColumn('title_year',      'Year')
	merge_string += DoColumn('title_series',    'Series')
	merge_string += DoColumn('title_seriesnum', 'Seriesnum')
	merge_string += DoColumn('title_storylen',  'Storylen')
	merge_string += DoColumn('title_content',   'ContentIndicator')
	merge_string += DoColumn('title_jvn',       'Juvenile')
	merge_string += DoColumn('title_nvz',       'Novelization')
	merge_string += DoColumn('title_non_genre', 'NonGenre')
	merge_string += DoColumn('title_graphic',   'Graphic')
	merge_string += DoColumn('title_language',  'Language')
	merge_string += DoColumn('title_ttype',     'TitleType')
	merge_string += DoColumn('title_synop',     'Synopsis')
	merge_string += DoColumn('title_note',      'Note')
	merge_string += DoColumn('title_parent',    'Parent')

	if form.has_key('mod_note'):
		merge_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))

	merge_string += "  </TitleMerge>\n"
	merge_string +=  "</IsfdbSubmission>\n"

	submission.file(merge_string)
