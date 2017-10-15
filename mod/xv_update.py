#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2014   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/01/15 18:21:03 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from viewers import DisplayPublisherChanges


if __name__ == '__main__':

	PrintPreMod('Proposed Publisher Update Submission')
	PrintNavBar()

	try:
		submission_id = int(sys.argv[1])
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	submitter = DisplayPublisherChanges(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('xa_update.cgi', submission_id)
	PrintPostMod()

