#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2021   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *

results_per_page=200


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)
        sub_type = SESSION.Parameter(1, 'str', 'I', ('I', 'N', 'R', 'P'))

	if sub_type == 'I':
		PrintHeader("My Recent Edits")
	elif sub_type == 'N':
		PrintHeader("My Pending Edits")
	elif sub_type == 'R':
		PrintHeader("My Rejected Edits")
	elif sub_type == 'P':
		PrintHeader("My Errored Out Edits")

	PrintNavbar('recent', 0, 0, 'recent.cgi', 0)

        if start:
                print '<p> [<a href="http:/%s/myrecent.cgi?%d+%s">NEWER</a>]<p>' % (HTFAKE, start-results_per_page, sub_type)

	(myID, username, usertoken) = GetUserData()

	if sub_type == 'N':
                queuesize = SQLQueueSize()
                print "The current number of pending edits by all editors (not held by a moderator) is %d." % queuesize

        query = """select * from submissions where sub_state='%s'
                and sub_submitter='%d' order by sub_reviewed desc
                limit %d,%d""" % (db.escape_string(sub_type), int(myID), start, results_per_page+1)
	db.query(query)
	result = db.store_result()
        numRows = result.num_rows()
	if numRows == 0:
		print '<h3>No submissions present</h3>'
		PrintTrailer('recent', 0, 0)
		sys.exit(0)
	elif sub_type == 'N':
		wikipointer = """<br>If your edits seem to be taking a long time to be approved,
                please check your <a href="http://%s/index.php/User_talk:%s">Talk page</a>
                for comments or questions.""" % (WIKILOC, username)
		print wikipointer
	elif sub_type == 'R':
		wikipointer = """The moderator may have left additional comments on your 
		<a href="http://%s/index.php/User_talk:%s">Talk page</a>.<br>
		Please check your wiki Talk page frequently for comments or questions.""" % (WIKILOC, username)
		print wikipointer

        ISFDBprintSubmissionTable(result, sub_type)
        
        # Check if there is more since "results_per_page+1" was requested from the database
        if numRows > results_per_page:
                print '<p> [<a href="http:/%s/myrecent.cgi?%d+%s">OLDER</a>]' % (HTFAKE, start+results_per_page, sub_type)
	PrintTrailer('recent', 0, 0)

