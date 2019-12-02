#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2019   Al von Ruff, Ahasuerus and Dirk Stoecker
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
from isfdblib import *
from common import *
from login import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node


if __name__ == '__main__':

	try:
		start = int(sys.argv[1])
		status = sys.argv[2]
	except:
		start = 0
		status = 'I'

	if status == 'I':
        	PrintPreMod('Recent Approvals')
                PrintNavBar()
	elif status == 'R':
        	PrintPreMod('Recent Rejections')
                PrintNavBar()
	elif status == 'N':
        	PrintPreMod('Recent Pending Submissions')
                PrintNavBar()
        elif status == 'P':
        	PrintPreMod('Errored Out and "In Progress" Submissions')
                PrintNavBar()
                print """<h3>Note: The status of each submission is temporarily changed from "New" to
                        "In Progress" during the approval process. Once a submission has been
                        successfully approved, its status is changed to "Approved". If, on the
                        other hand, the approval process errors out, then the submission remains
                        "In Progress" and is displayed on this page. If a new submission
                        appears on this list, check again in a few seconds to make sure that you
                        didn't catch it while it was in the process of being approved.</h3>"""
        else:
                PrintPreMod('Invalid Submissions Status Specified')
                PrintNavBar()
		print '<h3>Bad argument</h3>'
		PrintPostMod()
		sys.exit(0)

	if start:
		query = "select * from submissions use index (state_reviewed) where sub_state='%s' order by sub_reviewed desc limit %d,200;" % (status, start)
	else:
		query = "select * from submissions use index (state_reviewed) where sub_state='%s' order by sub_reviewed desc limit 200;" % (status)

	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>No submissions with the specified status present.</h3>'
		PrintPostMod()
		sys.exit(0)

        ISFDBprintSubmissionTable(result, status)

	print '<p> [<a href="http:/%s/mod/recent.cgi?%d+%s">MORE</a>]' % (HTFAKE, start+200, status)

	PrintPostMod()

