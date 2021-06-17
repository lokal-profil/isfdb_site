#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission_body = SQLloadSubmission(submission_id)
        if not submission_body:
                SESSION.DisplayError('Submission number %d not found in the submission queue</h2>' % submission_id)

	PrintHeader('Raw XML View')
        PrintNavbar('dumpxml', 0, 0, 0, 0)

	outstr = submission_body[SUB_DATA]
        outstr = string.replace(outstr, '<', '&lt;')
        outstr = string.replace(outstr, '>', '&gt;')
        outstr = string.replace(outstr, '\n', '<br>')

        print outstr

        print '<p>'
        print '<a class="approval" href="http:/%s/view_submission.cgi?%s">Public View</a>' % (HTFAKE, submission_id)
	(userid, username, usertoken) = GetUserData()
	# If the user is a moderator
        if SQLisUserModerator(userid):
                subtype = submission_body[SUB_TYPE]
                approval_script = SUBMAP[subtype][0]
                print ' <a class="approval" href="http:/%s/mod/%s.cgi?%s">Moderator View</a>' % (HTFAKE, approval_script, submission_id)

	PrintTrailer('dumpxml', 0, 0)
