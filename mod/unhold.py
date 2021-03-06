#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2021   Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from isfdblib import *
from library import *
from common import *

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Remove Submission Hold')
        PrintNavBar()

	(reviewerid, username, usertoken) = GetUserData()

        #Check that the submission is new
	if SQLloadState(submission) != 'N':
		print '<div id="ErrorBox">'
		print '<h3>Submission %d not in NEW state</h3>' % (int(submission))
		print '</div>'

        else:
                hold_id = SQLGetSubmissionHoldId(submission)
                if not hold_id:
                        print '<h3>Submission is not on hold.</h3>'
                # Only holding moderators and bureaucrats can unhold submissions
                elif (int(hold_id) != int(reviewerid)) and not SQLisUserBureaucrat(reviewerid):
                        holding_user = SQLgetUserName(hold_id)
                        print '<h3>Submission is currently on hold by '
                        print '<a href=%s://%s/index.php/User:%s>%s</a> ' % (PROTOCOL, WIKILOC, holding_user, holding_user)
                        print '<a href=%s://%s/index.php/User_talk:%s>(Talk)</a></h3>' % (PROTOCOL, WIKILOC, holding_user)
                else:
                        update = "update submissions set sub_holdid=0 where sub_id=%d" % int(submission)
                        db.query(update)
                        print '<h3>Submission %d is no longer on hold.</h3>' % int(submission)

        print ISFDBLink('mod/list.cgi', 'N', 'Submission List', 1)
	PrintPostMod(0)
