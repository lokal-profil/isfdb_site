#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2016   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2016/07/14 20:04:45 $


import string
import sys
import cgi
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

        PrintPreMod('Reject Submission')
        PrintNavBar()

        try:
                sub_id = int(sys.argv[1])
        except:
		print '<h3>Invalid or unspecified submission ID.</h3>'
		PrintPostMod()
		sys.exit(0)

        # Retrieve user information for the moderator tring to reject this submission
	(reviewerid, username, usertoken) = GetUserData()

        # Retrieve submission data
	query = "select * from submissions where sub_id=%d" % int(sub_id)
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>Specified submission ID does not exist</h3>'
		PrintPostMod()
		sys.exit(0)

        record = result.fetch_row()
        # If the submission is on hold, determine who the holding moderator is
        holder_id = record[0][SUB_HOLDID]
        if holder_id:
                # If the current user is neither the holding moderator nor a bureaucrat,
                # display a message explaining what needs to be done and abort
                if (int(holder_id) != int(reviewerid)) and (SQLisUserBureaucrat(reviewerid) == 0):
                        holder_name = SQLgetUserName(holder_id)
                        print '''<h3> This submission is currently held by <a href="http://%s/index.php/User:%s">%s</a>.
                        Please contact the holding moderator to discuss the submission. If the holding moderator is
                        inactive, please post on the Moderator Noticeboard and a bureaucrat will hard reject the
                        submission.''' % (WIKILOC, holder_name, holder_name)
                        PrintPostMod()
                        sys.exit(0)

        # If the submission was created by another moderator, do not allow rejection unless the current
        # user is a bureaucrat
        submitter_id = record[0][SUB_SUBMITTER]
        if ((int(submitter_id) != int(reviewerid))
            and (SQLisUserModerator(submitter_id) == 1)
            and not SQLisUserBureaucrat(reviewerid)):
                submitter_name = SQLgetUserName(submitter_id)
                print '''<h3> This submission was created by <a href="http://%s/index.php/User:%s">%s</a>, another moderator.
                Please contact the submitter to discuss the submission. If the submitting moderator is
                inactive, please post on the Moderator Noticeboard and a bureaucrat will hard reject the
                submission.''' % (WIKILOC, submitter_name, submitter_name)
                PrintPostMod()
                sys.exit(0)

	update = "update submissions set sub_state='R', sub_reason='%s', sub_reviewer='%d', sub_reviewed=NOW() where sub_id='%d';" % ("Forced", int(reviewerid), sub_id)
	print '<ul>'
        print '<li> ', update
	db.query(update)

        print '</ul>[<a href="http:/%s/mod/list.cgi?N">Submission List</a>]<hr />' % HTFAKE

	PrintPostMod()
