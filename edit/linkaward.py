#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
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
from isfdblib_help import *
from isfdblib_print import printfield, printtextarea
from awardClass import *


if __name__ == '__main__':

	try:
		award_id = int(sys.argv[1])
                award = awards(db)
                award.load(award_id)
                if not award.award_title:
                        raise
	except:
		PrintPreSearch("Link Award")
		PrintNavBar("edit/linkaward.cgi", 0)
		print '<h3>Non-existent award specified.</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Link Award")
	PrintNavBar("edit/linkaward.cgi", award_id)

        help = HelpGeneral()

	print '<div id="HelpBox">'
        print '<b>Help on linking awards: </b>'
        print '<a href="http://%s/index.php/Help:Screen:LinkAward">Help:Screen:LinkAward</a><p>' % (WIKILOC)
	print '</div>'

	print 'Linking the following award to a title:<p>'

        award.PrintAwardSummary()

	print 'Enter the record number of the title that this award refers to or 0 to break the link:'
	print '<p>'
	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitlinkaward.cgi">'
	print '<table border="0">'
        print '<tbody id="tagBody">'

	printfield("Title #", "title_id", help, award.title_id)

        printtextarea('Note to Moderator', 'mod_note', help, '')
        print '</tbody>'
        print '</table>'
	print "<p>"

	print '<input NAME="award_id" VALUE="%d" TYPE="HIDDEN">' % award_id
	print '<input TYPE="SUBMIT" VALUE="Link Award to Title" tabindex="1">'
	print '</form>'

	print '<p>'
	print '<hr>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)
