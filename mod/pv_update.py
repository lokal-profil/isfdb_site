#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2019   Al von Ruff, Bill Longley and Ahasuerus
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
from viewers import DisplayEditPub


if __name__ == '__main__':

        PrintPreMod('Proposed Publication Update Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
                print '<div id="ErrorBox">'
                print '<h3>Error: %s</h3>' % label
                print '</div>'
                PrintPostMod(0)
                sys.exit(0)

        submitter = DisplayEditPub(submission_id)
	
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('pa_update.cgi', submission_id)
	PrintPostMod(0)


