#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from viewers import DisplayDeletePub


if __name__ == '__main__':

        PrintPreMod('Proposed Publication Deletion Submission')
        PrintNavBar()

	try:
		submission_id = int(sys.argv[1])
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        submitter = DisplayDeletePub(submission_id)
	print '<p><b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('pa_delete.cgi', submission_id)
	PrintPostMod()

