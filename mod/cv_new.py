#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2017   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
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
from xml.dom import minidom
from xml.dom import Node
from viewers import DisplayClonePublication


if __name__ == '__main__':

        PrintPreMod('Proposed Clone/Import/Export Publication Submission')
        PrintNavBar()

	try:
		submission_id = int(sys.argv[1])
	except:
                print '<div id="ErrorBox">'
                print '<h3>Error: Bad submission ID</h3>'
                print '</div>'
                PrintPostMod()
                sys.exit(0)

        submitter = DisplayClonePublication(submission_id)
        print '<b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
        print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('ca_new.cgi', submission_id)

        display_sources(submission_id)

	PrintPostMod()

