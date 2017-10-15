#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2014/06/14 23:24:24 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from awardcatClass import *
from login import *
from SQLparsing import *
	
if __name__ == '__main__':

        (userid, username, usertoken) = GetUserData()
        if SQLisUserModerator(userid) == 0:
		PrintPreSearch("Delete Award Category - Limited to Moderators")
		PrintNavBar("edit/deleteawardcat.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Award Category")

	try:
		record = int(sys.argv[1])
	except:
		PrintNavBar(0, 0)
		print "<h3>Missing or invalid award category ID</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	PrintNavBar("edit/deleteawardcat.cgi", record)


	awardCat = award_cat()
	awardCat.award_cat_id = record
	awardCat.load()
	if not awardCat.award_cat_name:
		print "<h3>Specified award category does not exist</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	# Find if there are any award records for this award category
	awards = SQLloadAwardsForCat(awardCat.award_cat_id, 1)
        if awards:
                print "<h2>Error: Award records for %d years still on file for this award category</h2>" % (len(awards))
                print "<h2>*** Cannot delete this award type</h2>"
        else:
		print "<b>Request to Delete:</b> <i>%s</i>" % awardCat.award_cat_name
		print "<p />"

		print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdeleteawardcat.cgi\">"
		print "<b>Deletion Reason</b><br />"
		print '<textarea name="reason" rows="4" cols="45"></textarea>'
		print '<p>'
		print '<input name="award_cat_id" value="%d" type="HIDDEN">' % awardCat.award_cat_id
		print '<input type="SUBMIT" value="Delete">'
		print "</form>"
	
	PrintPostSearch(0, 0, 0, 0, 0)
