#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2017   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2017/03/08 21:55:44 $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *


#################################################################################
# AUTHOR-RELATED CHANGES
#################################################################################
def printAuthorRecord(index, old, new, changed):

	if (index == AUTHOR_NOTE_ID) or (index == AUTHOR_COUNTER) or (index == AUTHOR_MARQUE):
		return

	print '<tr>'
	if index == AUTHOR_CANONICAL:
		print '<td class="label"><b>author_canonical</b></td>'
	elif index == AUTHOR_LEGALNAME:
		print '<td class="label"><b>author_legalname</b></td>'
	elif index == AUTHOR_LASTNAME:
		print '<td class="label"><b>author_lastname</b></td>'
	elif index == AUTHOR_BIRTHPLACE:
		print '<td class="label"><b>author_birthplace</b></td>'
	elif index == AUTHOR_BIRTHDATE:
		print '<td class="label"><b>author_birthdate</b></td>'
	elif index == AUTHOR_DEATHDATE:
		print '<td class="label"><b>author_deathdate</b></td>'
	elif index == AUTHOR_WIKI:
		print '<td class="label"><b>author_wiki</b></td>'
	elif index == AUTHOR_IMDB:
		print '<td class="label"><b>author_imdb</b></td>'
	elif index == AUTHOR_ANNUALVIEWS:
		print '<td class="label"><b>author_annualviews</b></td>'
	elif index == AUTHOR_LANGUAGE:
		print '<td class="label"><b>author_language</b></td>'
		if old and old != 'NULL':
                        old = LANGUAGES[int(old)]
                if new:
                        new = LANGUAGES[int(new)]
	elif index == AUTHOR_EMAILS:
		print '<td class="label"><b>author_emails</b></td>'
	elif index == AUTHOR_WEBPAGES:
		print '<td class="label"><b>author_webpages</b></td>'
	elif index == AUTHOR_IMAGE:
		print '<td class="label"><b>author_image</b></td>'
	else:
		print '<td class="label"><b>%d</b></td>' % index

	if changed:
		print '<td class="drop">%s</td>' % old
		print '<td class="keep">%s</td>' % new
	else:
		print '<td class="keep">%s</td>' % old
		print '<td class="drop">-</td>'

	print '</tr>'

def checkAuthorHistory(index, history):
	counter = 0
	while counter < len(history):
		if history[counter][4] == index:
			printAuthorRecord(index, history[counter][8], history[counter][9], 1)
			return 0
		counter += 1
	return 1


def doAuthorUpdate(record):
	
	aurec = record[0][3]
	history = []
	while record:
		history.append(record[0])
        	record = result.fetch_row()

	query = "select * from authors where author_id=%d" % aurec
	db.query(query)
	res2 = db.store_result()
        rec2 = res2.fetch_row()

        if not rec2:
                print '<h2>Author record %d is no longer on file and may have been deleted or merged</h2>' % (aurec)
                PrintTrailer('recent', 0, 0)
                sys.exit(0)

	index = 1
	while index < AUTHOR_MAX:
		if (index == AUTHOR_EMAILS):
			if checkAuthorHistory(index, history):
				emails = SQLloadEmails(int(aurec))
				tmp = ''
				for email in emails:
                                        if tmp == '':
                                                tmp = email
                                        else:
                                                tmp += ',' + email
				printAuthorRecord(index, tmp, '', 0)
		elif (index == AUTHOR_WEBPAGES):
			if checkAuthorHistory(index, history):
				webpages = SQLloadWebpages(int(aurec))
				tmp = ''
				for webpage in webpages:
                                        if tmp == '':
                                                tmp = webpage
                                        else:
                                                tmp += ',' + webpage
				printAuthorRecord(index, tmp, '', 0)
		else:
			if checkAuthorHistory(index, history):
				printAuthorRecord(index, rec2[0][index], '', 0)
		index += 1


#################################################################################

def doHeader(record):
	if record[2] == AUTHOR_UPDATE:
		print "<b>Type:</b> Author Record Update"
		print '<br><b>Author Record:</b> <a href="http:/%s/edit/editauth.cgi?%d">%d</a>' % (HTFAKE, record[3], record[3])
	print "<br><b>Modified:</b> ", record[1]
	submitter = SQLgetUserName(record[6])
	print '<br><b>Submitter:</b> <a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, submitter, submitter)
	reviewer = SQLgetUserName(record[7])
	print '<br><b>Reviewer:</b> <a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, reviewer, reviewer)

if __name__ == '__main__':

	PrintHeader("Recent Edit")
	PrintNavbar('recent', 0, 0, 'history.cgi', 0)

	try:
		submission = int(sys.argv[1])
	except:
		PrintTrailer('recent', 0, 0)
		sys.exit(0)

	query = "select * from history where history_submission='%d'" % (submission)
	db.query(query)
	result = db.store_result()
	if result.num_rows():
        	record = result.fetch_row()
		doHeader(record[0])

		print '<p /><table border="1" cellpadding=2 BGCOLOR="#FFFFFF">'
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>From</b></td>'
		print '<td class="label"><b>To</b></td>'
		print '</tr>'

		if record[0][2] == AUTHOR_UPDATE:
			doAuthorUpdate(record)

		print '</table>'
		print '<p />'
		print '<p />'
	else:
		print '<h2>No history records available for this submission.</h2>'


	PrintTrailer('recent', 0, 0)

