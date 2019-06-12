#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2019   Ahasuerus
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
from library import *
from SQLparsing import *
from viewers import DisplaySeriesDelete


if __name__ == '__main__':

        PrintPreMod('Proposed Series Deletion Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod(0)
		sys.exit(0)

	submitter = DisplaySeriesDelete(submission_id)


        print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('sa_delete.cgi', submission_id)
	PrintPostMod(0)

