#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/04/19 01:38:19 $


import cgi
import sys
import MySQLdb
import string
from isfdb import *
from isfdblib import *
from SQLparsing import *
from common import *
from library import *

debug = 0

def DoError(text):
        print '<div id="ErrorBox">'
        print '<h3>%s</h3>' % text
        print '</div>'
        PrintPostMod()
        sys.exit(0)

def DoSubmission(db, submission):
        title_id =0
	award_id = 0
	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
	if doc.getElementsByTagName('LinkAward'):
		merge = doc.getElementsByTagName('LinkAward')

		print "<ul>"

		if TagPresent(merge, 'Title'):
			title_id = int(GetElementValue(merge, 'Title'))
		else:
                        DoError('No Title record specified')

		if TagPresent(merge, 'Award'):
			award_id = int(GetElementValue(merge, 'Award'))
			if award_id < 1:
                                raise
		else:
                        DoError('No valid award record specified')

		update = "delete from title_awards where award_id='%d';" % award_id
		print "<li> ", update
		if debug == 0:
			db.query(update)

		if int(title_id):
			update = "insert into title_awards(title_id, award_id) values(%d, %d);" % (title_id, award_id)
			print "<li> ", update
			if debug == 0:
				db.query(update)

		submitter = GetElementValue(merge, 'Submitter')
		if debug == 0:
			markIntegrated(db, submission)
		print "</ul>"
	return (title_id, award_id)


if __name__ == '__main__':

        PrintPreMod('Link Award - SQL Statements')
        PrintNavBar()

	try:
		submission = int(sys.argv[1])
	except:
                DoError('Error: Bad argument')

        if NotApprovable(submission):
                sys.exit(0)

	print '<h1>SQL Updates:</h1>'
	print '<hr>'

	(title_id, award_id) = DoSubmission(db, submission)

	print '<hr>'
	print '[<a href="http:/%s/mod/list.cgi?N">Submission List</a>]' % HTFAKE
	if title_id > 0:
		print '[<a href="http:/%s/title.cgi?%d">View Title record</a>]' % (HTFAKE, title_id)
	if award_id > 0:
		print '[<a href="http:/%s/award_details.cgi?%d">View Award record</a>]' % (HTFAKE, award_id)

	print "<p>"

	PrintPostMod()
	
