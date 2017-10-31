#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2013   Al von Ruff and Ahasuerus
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
from pubClass import *
from login import *
from SQLparsing import *

def displayError(value):
        print "<h3>%s.</h3>" % (value)
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Publication Delete Submission")

	try:
		record = int(sys.argv[1])
	except:
		PrintNavBar(0, 0)
		displayError("Integer publication number required")
	
	PrintNavBar("edit/deletepub.cgi", record)
	
	publication = SQLGetPubById(record)
	if not publication:
		displayError("Publication does not exist")

	print "<b>Request to Delete:</b> <i>%s</i>" % publication[PUB_TITLE]
	print "<p />"

        print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdelpub.cgi\">"
        print "<b>Deletion Reason</b><br />"
        print '<textarea name="reason" rows="4" cols="45"></textarea>'
        print '<p />'
        print '<input name="pub_id" value="%d" type="HIDDEN">' % (record)
        print '<input type="SUBMIT" value="Delete">'
        print "</form>"

	PrintPostSearch(0, 0, 0, 0, 0)
