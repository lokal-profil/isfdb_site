#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.12 $
#     Date: $Date: 2014/07/21 05:25:56 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from library import *
from SQLparsing import *
from viewers import DisplayTitleEdit


if __name__ == '__main__':

	PrintPreMod('Proposed Title Update Submission')
	PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	submitter = DisplayTitleEdit(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('ta_update.cgi', submission_id)
	PrintPostMod()
