#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.11 $
#     Date: $Date: 2014/07/16 03:14:55 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from viewers import DisplayMakeVariant


if __name__ == '__main__':

        PrintPreMod('Proposed Make Variant Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        submitter = DisplayMakeVariant(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('ka_new.cgi', submission_id)
	PrintPostMod()
