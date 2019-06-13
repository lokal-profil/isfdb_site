#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2019   Al von Ruff and Ahasuerus
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
from common import *
from awardClass import *
from isfdblib import *
from SQLparsing import *
from library import *
from viewers import DisplayAwardDelete


if __name__ == '__main__':

        PrintPreMod('Proposed Award Deletion Submission')
        PrintNavBar()

	try:
		submission_id = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod(0)
		sys.exit(0)

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = DisplayAwardDelete(submission_id)
       
	print '<p><b>Submitted by:</b> <a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	print '<a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, submitter)

	ApproveOrReject('wa_delete.cgi', submission_id)
	PrintPostMod(0)

