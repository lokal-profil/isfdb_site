#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *
from common import *

if __name__ == '__main__':

        PrintPreMod('Remove Submission Hold')
        PrintNavBar()

	try:
		submission = sys.argv[1]
	except:
		sys.exit(0)

	(reviewerid, username, usertoken) = GetUserData()

	hold_id = SQLGetSubmissionHoldId(submission)

        #Check that the submission is not approved/rejected
	if SQLloadState(submission) != 'N':
		print '<div id="ErrorBox">'
		print "<h3>Submission %d not in NEW state</h3>" % (int(submission))
		print '</div>'

        else:
                #Only submissions held by the currently signed in moderator can be removed from hold
                if not hold_id:
                        print "<h3>Submission is not on hold.</h3>"
                elif int(hold_id) != int(reviewerid):
                        holding_user = SQLgetUserName(hold_id)
                        print '<h3>Submission is currently on hold by '
                        print '<a href=http://%s/index.php/User:%s>%s</a> ' % (WIKILOC, holding_user, holding_user)
                        print '<a href=http://%s/index.php/User_talk:%s>(Talk)</a></h3>' % (WIKILOC, holding_user)
                else:
                        update = "update submissions set sub_holdid=0 where sub_id='%d';" % (int(submission))
                        db.query(update)
                        print "<h3>Submission %d is no longer on hold.</h3>" % int(submission)

        print ISFDBLink('mod/list.cgi', 'N', 'Submission List', 1)

	PrintPostMod(0)
