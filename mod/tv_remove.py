#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.9 $
#     Date: $Date: 2014/07/14 23:12:02 $


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from library import *
from titleClass import *
from SQLparsing import *
from viewers import DisplayRemoveTitle


if __name__ == '__main__':

        PrintPreMod('Proposed Title Removal Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        submitter = DisplayRemoveTitle(submission_id)

	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('ta_remove.cgi', submission_id)
	PrintPostMod()


