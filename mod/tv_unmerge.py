#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff and Ahasuerus
#	 ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.7 $
#     Date: $Date: 2014/07/15 21:36:51 $


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from titleClass import *
from library import *
from SQLparsing import *
from viewers import DisplayUnmergeTitle


if __name__ == '__main__':

	PrintPreMod('Proposed Title Unmerge Submission')
	PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        submitter = DisplayUnmergeTitle(submission_id)
	print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('ta_unmerge.cgi', submission_id)
	PrintPostMod()

