#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2011   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2011/03/28 05:48:52 $


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


def DoSubmission(db, submission):
        ParentRecord =0
	ChildRecord = 0
	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
	if doc.getElementsByTagName('LinkReview'):
		merge = doc.getElementsByTagName('LinkReview')

		print "<ul>"

		if TagPresent(merge, 'Parent'):
			ParentRecord = int(GetElementValue(merge, 'Parent'))
		else:
			print '<div id="ErrorBox">'
			print "<h3>: No Parent listed</h3>"
			print '</div>'
			PrintPostMod()
                	sys.exit(0)

		if TagPresent(merge, 'Record'):
			ChildRecord = int(GetElementValue(merge, 'Record'))
		else:
			print '<div id="ErrorBox">'
			print "<h3>: No Review record listed</h3>"
			print '</div>'
			PrintPostMod()
                	sys.exit(0)

		update = "delete from title_relationships where review_id='%d';" % (int(ChildRecord))
		print "<li> ", update
		if debug == 0:
			db.query(update)

		if int(ParentRecord):
			update = "insert into title_relationships(title_id, review_id) values(%d, %d);" % (int(ParentRecord), int(ChildRecord))
			print "<li> ", update
			if debug == 0:
				db.query(update)

		submitter = GetElementValue(merge, 'Submitter')
		if debug == 0:
			markIntegrated(db, submission)
		print "</ul>"
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

	print "<hr>"
	print '[<a href="http:/' +HTFAKE+ '/mod/list.cgi?N">Submission List</a>]'
	if ParentRecord > 0:
		print '[<a href="http:/' +HTFAKE+ '/title.cgi?%d">View Reviewed Title</a>]' % ParentRecord
	if ChildRecord > 0:
		print '[<a href="http:/' +HTFAKE+ '/title.cgi?%d">View Review Title</a>]' % ChildRecord

	print "<p>"

	PrintPostMod()
	
