#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2016/04/30 04:41:18 $


import sys
from awardtypeClass import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from login import *
from library import *
from isfdblib_print import printAwardName


def DoError(message):
        PrintPreSearch("Award Type Selector")
        PrintNavBar("edit/select_award_type.cgi", 0)
        print '<h3>%s.</h3>' % message
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':
        
        try:
                title_id = int(sys.argv[1])
        except:
                DoError('Missing or invalid Title ID')

        PrintPreSearch("Award Type Selector")
        PrintNavBar("edit/select_award_type.cgi", title_id)

        help = HelpAward(0)

	print '<div id="HelpBox">'
        print "<b>Help on adding an award: </b>"
        print '<a href="http://%s/index.php/Help:Screen:AddAward">Help:Screen:AddAward</a><p>' % (WIKILOC)
	print '</div>'

	print '<form method="POST" action="/cgi-bin/edit/addaward.cgi">'
        print "<table border=\"0\">"
        print '<tbody id="titleBody">'

        printAwardName("award_type_id", "Award Name", help)

	print '</tbody>'
	print '</table>'
	print '<p>'

	print '<input name="title_id" value="%d" type="HIDDEN">' % (title_id)
	print '<input type="SUBMIT" value="Proceed to the Next Page" tabindex="1">'
	print '</form>'

	PrintPostSearch(0, 0, 0, 0, 0)
