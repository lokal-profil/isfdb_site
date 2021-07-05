#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2021   Al von Ruff and Ahasuerus
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

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Place Submission on Hold')
        PrintNavBar()

	(reviewerid, username, usertoken) = GetUserData()

	hold_id = SQLGetSubmissionHoldId(submission)

	if SQLloadState(submission) != 'N':
		print '<div id="ErrorBox">'
		print "<h3>Submission %d not in NEW state</h3>" % (int(submission))
		print '</div>'

        else:
                if int(hold_id) == int(reviewerid):
                        print "<h3>Submission is already on hold by you.</h3>"
                elif hold_id:
                        holding_user = SQLgetUserName(hold_id)
                        print '<h3>Submission is already on hold by '
                        print '<a href=http://%s/index.php/User:%s>%s</a> ' % (WIKILOC, holding_user, holding_user)
                        print '<a href=http://%s/index.php/User_talk:%s>(Talk)</a></h3>' % (WIKILOC, holding_user)
                else:
                        update = "update submissions set sub_holdid=%d where sub_id='%d';" % (int(reviewerid), int(submission))
                        db.query(update)
                        print "<h3>Submission %d has been put on hold.</h3>" % int(submission)

        print ISFDBLink('mod/list.cgi', 'N', 'Submission List', 1)

	PrintPostMod(0)
