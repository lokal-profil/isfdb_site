#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 428 $
#     Date: $Date: 2019-06-12 17:06:29 -0400 (Wed, 12 Jun 2019) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import SQLloadSubmission
from library import WikiLink
import viewers


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission_data = SQLloadSubmission(submission_id)
        if not submission_data:
                SESSION.DisplayError('Specified Submission Does Not Exist')
        submission_type = submission_data[SUB_TYPE]
        submission_type_name = SUBMAP[submission_type][3]

	PrintPreMod('Proposed %s Submission' % submission_type_name)
	PrintNavBar()

        submission_filer = SUBMAP[submission_type][6]
        function_name = SUBMAP[submission_type][5]
        function_to_call = getattr(viewers, function_name)
        submitter = function_to_call(submission_id)
	print '<b>Submitted by:</b> %s' % WikiLink(submitter)

	ApproveOrReject('%s.cgi' % submission_filer, submission_id)
	if submission_filer in ('ca_new', 'pa_new'):
                display_sources(submission_id)
	PrintPostMod(0)
