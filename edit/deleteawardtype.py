#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
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
from awardtypeClass import *
from login import *
from SQLparsing import *
	
if __name__ == '__main__':

        (userid, username, usertoken) = GetUserData()
        if SQLisUserModerator(userid) == 0:
		PrintPreSearch("Delete Award Type - Limited to Moderators")
		PrintNavBar("edit/deleteawardtype.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Award Type")

	try:
		record = int(sys.argv[1])
	except:
		PrintNavBar(0, 0)
		print "<h3>Missing or invalid award type ID</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	PrintNavBar("edit/deleteawardtype.cgi", record)


	awardType = award_type()
	awardType.award_type_id = record
	awardType.load()
	if not awardType.award_type_name:
		print "<h3>Specified award type does not exist</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	# Find if there are any award records for this award type
	awards = SQLGetAwardYears(awardType.award_type_id)
	award_cats = SQLGetAwardCategories(awardType.award_type_id)
        if awards or award_cats:
                if awards:
                        print "<h2>Error: Award records for %d years still on file for this award type</h2>" % (len(awards))
                if award_cats:
                        print "<h2>Error: %d award categories still on file for this award type</h2>" % (len(award_cats))
                print "<h2>*** Cannot delete this award type</h2>"
        else:
		print "<b>Request to Delete:</b> <i>%s</i>" % awardType.award_type_name
		print "<p />"

		print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdeleteawardtype.cgi\">"
		print "<b>Deletion Reason</b><br />"
		print '<textarea name="reason" rows="4" cols="45"></textarea>'
		print '<p>'
		print '<input name="award_type_id" value="%d" type="HIDDEN">' % awardType.award_type_id
		print '<input type="SUBMIT" value="Delete">'
		print "</form>"
	
	PrintPostSearch(0, 0, 0, 0, 0)
