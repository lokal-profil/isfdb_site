#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2021   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
from isfdb import *
from SQLparsing import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import printtextarea
from library import *
from titleClass import *

debug        = 0
MaxRecords   = 0
Records      = []

def Compare(value1, value2, fieldname):
	if value1 != value2:
		print '<tr align="left">'
		print '<td class="drop">'
		print "<b>" +fieldname+ " Conflict:</b><br>"
		print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="1" CHECKED>'
		print value1
		print "<br>"
		print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="2">'
		print value2
		print '</td>'
		print "</tr>"
	else:
		print '<tr align="left">'
		print '<td class="keep">'
		print "<b>Merged " +fieldname+ ": </b>", value1
		print '</td>'
		print "</tr>"

def Compare2(fieldname, values):

	checked_entry = 1

        # For Yes/No flags, check the first "Yes" box
	if fieldname in ('title_jvn', 'title_nvz', 'title_non_genre', 'title_graphic'):
                recno = 0
                while recno < MaxRecords:
                        if values[recno] == 'Yes':
                                checked_entry = recno + 1
                                break
                        recno += 1
        # For dates, check the box for the earliest date
	elif fieldname == 'title_year':
                recno = 0
                earliest_date = '9999-00-00'
                while recno < MaxRecords:
                        if values[recno] and Compare2Dates(values[recno], earliest_date):
                                earliest_date = values[recno]
                                checked_entry = recno + 1
                        recno += 1
        # For all other types of fields, check the first non-empty box
	else:
                recno = 0
                while recno < MaxRecords:
                        if values[recno]:
                                checked_entry = recno + 1
                                break
                        recno += 1

	recno = 1
	while recno < MaxRecords:
        	if values[0] != values[recno]:
			print '<tr align="left">'
			print '<td class="drop"><b>%s</b></td>' % fieldname
			print '<td class="drop"><b>Conflict</b></td>'
			print '<td class="drop">'
			index = 1
			for value in values:
				if index == checked_entry:
					print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="%s" checked="checked">' % (index)
				else:
					print '<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="%s">' % (index)
				index += 1
				print value
				print '<br>'
			print '</td>'
			print '</tr>'
			return
		recno += 1
	print '<tr align="left">'
	print '<td class="keep"><b>%s</b></td>' % fieldname
	print '<td class="keep">Merged</td>'
	print '<td class="keep">%s</td>' % values[0]
	print '</tr>'

def Merge2(fieldname, values):

	print '<tr align="left">'
	print '<td class="keep"><b>%s</b></td>' % fieldname
	print '<td class="keep">Merged</td>'
	print '<td class="keep">'
	for value in values:
		if value:
			print value
			print "<br>"
	print '</td>'
	print '</tr>'

def SelectionError():
        DisplayError('You need to select at least two records to merge')

def DisplayError(message):
	print '<h1>Error: %s.</h1>' % (message)
	print '</body>\n'
	print '</html>\n'
	PrintPostSearch(0, 0, 0, 0, 0)
	sys.exit(1)

def checkPubDups(title1, title2):
	pubs1 = SQLGetPubsByTitleNoParent(int(title1))
	pubs2 = SQLGetPubsByTitleNoParent(int(title2))
	for pub1 in pubs1:
		for pub2 in pubs2:
			if pub1[PUB_PUBID] == pub2[PUB_PUBID]:
				print '<div id="WarningBox">'
				print "<h3>WARNING: records %s and %s both appear in the publication <i>%s</i></h3>" % (title1, title2, pub1[PUB_TITLE])
				print "<p>Merging titles causes the title names to be commonized, AND causes"
				print "that new title to show up in the publications those titles point to."
				print "If you merge two titles that appear in the same publication, you will"
				print "cause that title to show up twice in that pub. This is probably not what you want."
				print "<p>If you are trying to remove a duplicate title from a publication, edit"
				print "that publication, and click on <b>Remove Titles From This Pub</b>."
				print "Then select the title you wish to remove."
				print '</div>'
				return

def checkTitleTypes(list):
        total = len(list)
        review_count = 0
        interview_count = 0
        reviewed_titles = []
        for rec in list:
                if rec.title_ttype == 'REVIEW':
                        review_count += 1
                        reviewed_title = SQLfindReviewedTitle(rec.title_id)
                        # Add the reviewed title ID to the list of reviewed titles
                        if reviewed_title and (reviewed_title not in reviewed_titles):
                                reviewed_titles.append(reviewed_title)
                elif rec.title_ttype == 'INTERVIEW':
                        interview_count += 1

        if len(reviewed_titles) > 1:
                DisplayError("All to-be-merged REVIEW records must be reviews of the same title")

        if review_count and (review_count < total):
                DisplayError("REVIEWS can't be merged with other title types")
        if interview_count and (interview_count < total):
        	DisplayError("INTERVIEWS can't be merged with other title types")


if __name__ == '__main__':
	PrintPreSearch("Title Merge Results")
	PrintNavBar(0, 0)

	##################################################################
	# Gather the form input
	##################################################################
	sys.stderr = sys.stdout
	form = cgi.FieldStorage()
	if form.has_key('merge'):
                RecordNumber = form.getlist('merge')
                MaxRecords = len(RecordNumber)
		rec = 0
		print "<h2>Merging Records: "
		while rec < MaxRecords:
			print RecordNumber[rec]
			rec += 1
		print "</h2>"
		print "<hr>"
	else:
		SelectionError()

        help = HelpGeneral()

	if MaxRecords < 2:
		SelectionError()


	##################################################
	# Load in all of the data records
	##################################################
	recno = 0
	while recno < MaxRecords:
        	Records.append(titles(db))
        	Records[recno].load(int(RecordNumber[recno]))
		recno += 1

	##################################################
	# Check for Review/Interview mismatches
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
                list.append(Records[recno])
		recno += 1
	checkTitleTypes(list)

	##################################################
	# Check to see if the titles are ever in the
	# same publications 
	##################################################
	target = 0
	while target < MaxRecords:
		check = target+1
		while check < MaxRecords:
			checkPubDups(RecordNumber[target], RecordNumber[check])
			check += 1
		target += 1

	print '<form METHOD="POST" ACTION="/cgi-bin/edit/ts_merge.cgi">'
	print '<table class="generic_table">'

	##################################################
	# title_title
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_title)
		recno += 1
	Compare2("title_title", list)

	##################################################
	# title_trans_titles 	 
	################################################## 	 
	trans_titles_list = [] 	 
	recno = 0 	 
	while recno < MaxRecords:
                for trans_title in Records[recno].title_trans_titles:
                        if trans_title not in trans_titles_list:
                                trans_titles_list.append(trans_title)
		recno += 1 	 
	Merge2("title_trans_titles", trans_titles_list)

	##################################################
	# title_author
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].authors())
		recno += 1
	Compare2("title_author", list)

	##################################################
	# title_xlate
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_xlate)
		recno += 1
	Compare2("title_xlate", list)

	##################################################
	# title_synop
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_synop)
		recno += 1
	Compare2("title_synop", list)

	##################################################
	# title_series
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_series)
		recno += 1
	Compare2("title_series", list)

	##################################################
	# title_seriesnum
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_seriesnum)
		recno += 1
	Compare2("title_seriesnum", list)

	##################################################
	# title_year
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_year)
		recno += 1
	Compare2("title_year", list)

	##################################################
	# title_storylen
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_storylen)
		recno += 1
	Compare2("title_storylen", list)

	##################################################
	# title_content
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_content)
		recno += 1
	Compare2("title_content", list)

	##################################################
	# title_jvn
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_jvn)
		recno += 1
	Compare2("title_jvn", list)

	##################################################
	# title_nvz
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_nvz)
		recno += 1
	Compare2("title_nvz", list)

	##################################################
	# title_nongenre
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_non_genre)
		recno += 1
	Compare2("title_non_genre", list)

	##################################################
	# title_graphic
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_graphic)
		recno += 1
	Compare2("title_graphic", list)

	##################################################
	# title_language
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_language)
		recno += 1
	Compare2("title_language", list)

	##################################################
	# title_ttype
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_ttype)
		recno += 1
	Compare2("title_ttype", list)

	##################################################
	# title_parent
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_parent)
		recno += 1
	Compare2("title_parent", list)

	##################################################
	# title_webpages 	 
	################################################## 	 
	list = [] 	 
	recno = 0 	 
	while recno < MaxRecords:
                for webpage in Records[recno].title_webpages:
                        if webpage not in list:
                                list.append(webpage)
		recno += 1 	 
	Merge2("title_webpages", list)

	##################################################
	# title_note
	##################################################
	list = []
	recno = 0
	while recno < MaxRecords:
		list.append(Records[recno].title_note)
		recno += 1
	Compare2("title_note", list)

	print '</table>'
	print '<p>'

        # Display cover images for COVERART records
        recno = 0
        images_found = 0
	while recno < MaxRecords:
                if Records[recno].title_ttype == 'COVERART':
                        if not images_found:
                                print '<table border="1">'
                                images_found = 1
                        print '<tr>'
                        print '<td>Images for record %s:</td>' % ISFDBLinkNoName('title.cgi', Records[recno].title_id, Records[recno].title_id)
                        cover_pubs = SQLGetCoverPubsByTitle(int(Records[recno].title_id))
                        print '<td>'
                        for cover_pub in cover_pubs:
                                if cover_pub[PUB_IMAGE]:
                                        print '<br>'
                                        print ISFDBLinkNoName('pl.cgi', cover_pub[PUB_PUBID], FormatImage(cover_pub[PUB_IMAGE]))
                                        print '<br>'
                        print '</td>'
                        print '</tr>'
                recno += 1

        if images_found:
                print '</table>'
        
        print '<hr>'
        print '<table border="0">'
        print '<tbody id="tagBody">'
        printtextarea('Note to Moderator', 'mod_note', help, '')
        print '</tbody>'
        print '</table>'
        print '<p>'

	recno = 0
	while recno < MaxRecords:
		print '<input NAME="record%s" VALUE="%s" TYPE="HIDDEN">' % ((recno+1), RecordNumber[recno])
		recno += 1

	print '<input TYPE="SUBMIT" VALUE="Complete Merge">'
	print '</form>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)
