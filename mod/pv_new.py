#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2015   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.26 $
#     Date: $Date: 2015/01/17 23:02:09 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node
from viewers import DisplayNewPub


if __name__ == '__main__':

        PrintPreMod('Proposed New/Add Publication Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
                print '<div id="ErrorBox">'
                print '<h3>Error: Bad argument</h3>'
                print '</div>'
                PrintPostMod()
                sys.exit(0)

        submitter = DisplayNewPub(submission_id)
        print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
        print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('pa_new.cgi', submission_id)

        display_sources(submission_id)

	PrintPostMod()

