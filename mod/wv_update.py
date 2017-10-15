#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.13 $
#     Date: $Date: 2014/07/11 02:56:48 $


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from awardClass import *
from isfdblib import *
from library import *
from SQLparsing import *
from viewers import DisplayAwardEdit


if __name__ == '__main__':

	PrintPreMod('Proposed Award Update Submission')
	PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        submitter = DisplayAwardEdit(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('wa_update.cgi', submission_id)
	PrintPostMod()

