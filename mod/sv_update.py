#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from seriesClass import *
from SQLparsing import *
from library import *
from viewers import DisplaySeriesChanges


if __name__ == '__main__':

        PrintPreMod('Proposed Series Update Submission')
        PrintNavBar()

	try:
		submission_id = int(sys.argv[1])
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	submitter = DisplaySeriesChanges(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('sa_update.cgi', submission_id)
	PrintPostMod()

