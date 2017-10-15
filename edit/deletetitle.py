#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2013   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.8 $
#     Date: $Date: 2013/12/31 20:29:25 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from login import *
from SQLparsing import *
	
if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Title Submission")

	try:
		record = int(sys.argv[1])
	except:
		PrintNavBar(0, 0)
		print "<h3>Missing or invalid title ID</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	PrintNavBar("edit/deletetitle.cgi", record)
	NoneFound  = 1

	titleRecord = SQLloadTitle(record)
	if titleRecord == []:
		print "<h3>Specified title does not exist</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	# Find pubs that refer to this title
	pubs = SQLGetPubsByTitle(record)
	if len(pubs) > 0:
		NoneFound = 0
		print "<h2>Error: %d publications still refer to this title:</h2>" % (len(pubs))
		print "<ul>"
		for pub in pubs:
			print "<li>"
			try:
				print '<a href="http:/%s/pl.cgi?%s">%s</a> (%s)' % (HTFAKE, pub[PUB_PUBID], pub[PUB_TITLE], convertYear(pub[PUB_YEAR][:4]))
                        except:
                                continue
		print "</ul>"

	# Find any variants that refer to this title
	titles = SQLgetTitleVariants(record)
        if len(titles) > 0:
		NoneFound = 0
		print "<h2>Error: %d variant titles still refer to this parent title:</h2>" % (len(titles))
		print "<ul>"
		for title in titles:
			print "<li>"
			try:
				print '<a href="http:/%s/title.cgi?%d">%d</a> (%s)' % (HTFAKE, title[TITLE_PUBID], title[TITLE_PUBID], title[TITLE_TITLE])
                        except:
                                continue
		print "</ul>"

	# Find any awards that refer to this title
	awards = SQLTitleAwards(record)
        if len(awards) > 0:
		NoneFound = 0
		print "<h2>Error: %d awards still refer to this title</h2>" % (len(awards))

	if NoneFound:
		titlename = SQLgetTitle(record)
		print "<b>Request to Delete:</b> <i>%s</i>" % titlename
		print "<p />"

		print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdeltitle.cgi\">"
		print "<b>Deletion Reason</b><br />"
		print '<textarea name="reason" rows="4" cols="45"></textarea>'
		print '<p />'
		print '<input name="title_id" value="%d" type="HIDDEN">' % record
		print '<input type="SUBMIT" value="Delete">'
		print "</form>"
	else:
		print "<h2>*** Cannot delete title</h2>"
	
	PrintPostSearch(0, 0, 0, 0, 0)
