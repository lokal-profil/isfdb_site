#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2013   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2013/12/30 00:47:58 $


import string
import sys
import cgi
import MySQLdb
from isfdb import *
from common import *
from library import *
from SQLparsing import *


def ErrorBox(message):
        print '<div id="ErrorBox">'
        print "<h3>%s.</h3>" % (message)
        print '</div>'
        PrintTrailer('cancelsubmission', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	PrintHeader("Submission Cancellation")
	PrintNavbar('cancelsubmission', 0, 0, 'cancelsubmission.cgi', 0)

	try:
		submission = int(sys.argv[1])
	except:
                ErrorBox("Can't get submission ID")

        query = "select * from submissions where sub_id = '%d';" % (submission)
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
                ErrorBox("Submission ID %d is not present" % submission)

        record = result.fetch_row()
	if record[0][SUB_STATE] != 'N':
                ErrorBox("Submission %d is not in NEW state" % submission)

	(myID, username, usertoken) = GetUserData()

	if int(record[0][SUB_SUBMITTER]) != int(myID):
                ErrorBox("Submissions created by other users can't be cancelled!")

        print "<ul>"

	reason = 'Cancelled by the submitter'
	update = "update submissions set sub_state='R', sub_reason='%s', sub_reviewer='%d', sub_reviewed=NOW() where sub_id='%d';" % (db.escape_string(reason), int(myID), submission)
        print "<li> ", update
	db.query(update)

        print "</ul><p /><hr />"

	print "Record %d has been moved to the Rejected state.<br />" % submission
	print "<b>Reason:</b> ", reason

	print "<p />"
	print "<hr />"

	PrintTrailer('cancelsubmission', 0, 0)
