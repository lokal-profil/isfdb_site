#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2014/01/15 18:21:03 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import SQLloadXML
from library import *
from viewers import DisplayAwardTypeChanges


if __name__ == '__main__':

	PrintPreMod('Proposed Award Type Update Submission')
	PrintNavBar()

	try:
		submission_id = int(sys.argv[1])
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	submitter = DisplayAwardTypeChanges(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('award_type_update_file.cgi', submission_id)
	PrintPostMod()
