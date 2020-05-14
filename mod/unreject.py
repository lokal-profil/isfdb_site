#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 528 $
#     Date: $Date: 2020-05-13 17:06:08 -0400 (Wed, 13 May 2020) $


import string
import sys
import cgi
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *

def DoError(message):
        print '<h3>%s.</h3>' % message
        PrintPostMod(0)
        sys.exit(0)

if __name__ == '__main__':

        PrintPreMod('UnReject Submission')
        PrintNavBar()

        try:
                sub_id = int(sys.argv[1])
        except:
                DoError('Invalid or unspecified submission ID')

        sub_data = SQLloadSubmission(sub_id)
	if not sub_data:
                DoError('Specified submission ID does not exist')

        if sub_data[SUB_STATE] != 'R':
                DoError('This submission is not in the Rejected state')

	update = """update submissions
                set sub_state='N', sub_reason=NULL, sub_reviewer=0, sub_reviewed=NULL, sub_holdid=0
                where sub_id=%d""" % int(sub_id)
	print '<ul>'
        print '<li> ', update
	db.query(update)
        print '</ul>'
	print '<p>'
	print ISFDBLink('view_submission.cgi', sub_id, 'View Submission')
	PrintPostMod(0)
