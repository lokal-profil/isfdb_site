#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2014   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/04/16 21:25:16 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from awardClass import *
from login import *
from SQLparsing import *
	

if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Award Submission")

	try:
		record = int(sys.argv[1])
	except:
                PrintNavBar(0, 0)
                print "<h3>Missing or invalid argument</h3>"
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)
	
	PrintNavBar("edit/deleteaward.cgi", record)
	
	award = SQLloadAwards(record)
	if not award:
		print "<h3>Error: Award record does not exist</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	print "<b>Request to Delete:</b> <i>%s</i>" % award[0][AWARD_TITLE]
	print "<p />"

        print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdelaward.cgi\">"
        print "<b>Deletion Reason</b><br />"
        print '<textarea name="reason" rows="4" cols="45"></textarea>'
        print '<p />'
        print '<input name="award_id" value="%d" type="HIDDEN">' % record
        print '<input type="SUBMIT" value="Delete">'
        print "</form>"

	PrintPostSearch(0, 0, 0, 0, 0)
