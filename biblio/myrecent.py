#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2018   Al von Ruff, Ahasuerus and Dirk Stoecker
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
from login import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node

results_per_page=200


if __name__ == '__main__':

	try:
		start = int(sys.argv[1])
	except:
		start = 0

	try:
		type = sys.argv[2]
		if type not in ('I', 'N', 'R', 'P'):
			type = 'I'
	except:
		type = 'I'

	if type == 'I':
		PrintHeader("My Recent Edits")
	elif type == 'N':
		PrintHeader("My Pending Edits")
	elif type == 'R':
		PrintHeader("My Rejected Edits")
	elif type == 'P':
		PrintHeader("My Errored Out Edits")

	PrintNavbar('recent', 0, 0, 'recent.cgi', 0)

        if start:
                print '<p> [<a href="http:/%s/myrecent.cgi?%d+%s">NEWER</a>]<p>' % (HTFAKE, start-results_per_page, type)

	(myID, username, usertoken) = GetUserData()

        query = """select * from submissions where sub_state='%s'
                and sub_submitter='%d' order by sub_reviewed desc
                limit %d,%d""" % (db.escape_string(type), int(myID), start, results_per_page+1)
	db.query(query)
	result = db.store_result()
        numRows = result.num_rows()
	if numRows == 0:
		print '<h3>No submissions present</h3>'
		PrintTrailer('recent', 0, 0)
		sys.exit(0)
	elif type == 'N':
                queuesize = SQLQueueSize()
		wikipointer = """If your edits seem to be taking a long time to be approved,
                please check your <a href="http://%s/index.php/User_talk:%s">Talk page</a>
                for comments or questions.<br>The current number of pending edits by all editors is %d.""" % (WIKILOC, username, queuesize)
		print wikipointer
	elif type == 'R':
		wikipointer = """The moderator may have left additional comments on your 
		<a href="http://%s/index.php/User_talk:%s">Talk page</a>.<br>
		Please check your wiki Talk page frequently for comments or questions.""" % (WIKILOC, username)
		print wikipointer

        printSubmissionTable(type)
	color = 0
        for n in range(results_per_page):
                record = result.fetch_row()
                if not record:
                        break
		printSubmissionRecord(record, color, type)
		color = color ^ 1

	print "</table>"
        # Check if there is more since "results_per_page+1" was requested from the database
        if numRows > results_per_page:
                print '<p> [<a href="http:/%s/myrecent.cgi?%d+%s">OLDER</a>]' % (HTFAKE, start+results_per_page, type)
	PrintTrailer('recent', 0, 0)

