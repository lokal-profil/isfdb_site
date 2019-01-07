#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2019   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 302 $
#     Date: $Date: 2019-01-06 17:17:20 -0500 (Sun, 06 Jan 2019) $


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

	PrintHeader('Raw XML View')
        PrintNavbar('dumpxml', 0, 0, 0, 0)

	try:
		submission = int(sys.argv[1])
	except:
                print '<h2>Invalid submission specified</h2>'
		sys.exit(0)

        query = "select * from submissions where sub_id=%d" % submission
        db.query(query)
        result = db.store_result()
        if result.num_rows() == 0:
                print '<h2>Submission number %d not found in the submission queue</h2>' % submission
                sys.exit(0)
	
        record = result.fetch_row()[0]
	outstr = record[SUB_DATA]
        outstr = string.replace(outstr, '<', '&lt;')
        outstr = string.replace(outstr, '>', '&gt;')
        outstr = string.replace(outstr, '\n', '<br>')

        print outstr

        print '<p>'
        print '<a class="approval" href="http:/%s/view_submission.cgi?%s">Public View</a>' % (HTFAKE, submission)
	(userid, username, usertoken) = GetUserData()
	# If the user is a moderator
        if SQLisUserModerator(userid):
                subtype = record[SUB_TYPE]
                approval_script = SUBMAP[subtype][0]
                print ' <a class="approval" href="http:/%s/mod/%s.cgi?%s">Moderator View</a>' % (HTFAKE, approval_script, record[SUB_ID])

	PrintTrailer('dumpxml', 0, 0)
