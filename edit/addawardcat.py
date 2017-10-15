#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.5 $
#     Date: $Date: 2016/04/30 04:43:37 $


import sys
from awardtypeClass import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from login import *
from library import *
from isfdblib_print import printtextarea, printfield, printWebPages


if __name__ == '__main__':
        
        try:
                award_type_id = int(sys.argv[1])
                # If the passed in ID is not 0, i.e. this is a title-based award, load the associated title data
                if not award_type_id:
                        raise
                awardType = award_type()
                awardType.award_type_id = award_type_id
                awardType.load()
                if not awardType.award_type_name:
                        raise
        except:
                PrintPreSearch("New Award Category Error")
		PrintNavBar("edit/addawardcat.cgi", 0)
		print '<h3>Missing or invalid Award Type ID</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

        PrintPreSearch("New Award Category for %s Award" % awardType.award_type_short_name)
        PrintNavBar("edit/addawardcat.cgi", sys.argv[1])

	print '<div id="HelpBox">'
        print "<b>Help on adding an award category: </b>"
        print '<a href="http://%s/index.php/Help:Screen:AddAwardCat">Help:Screen:AddAwardCat</a><p>' % (WIKILOC)
	print '</div>'

	print '<form method="POST" action="/cgi-bin/edit/submitnewawardcat.cgi" onsubmit="return validateAwardCatForm()">'
        print "<table border=\"0\">"
        print '<tbody id="tagBody">'

        help = HelpAwardCat()

        printfield("Award Category", "award_cat_name", help)

        printfield("Display Order", "award_cat_order", help)

        printWebPages([], 'award_cat', help)

        printtextarea('Note', 'award_cat_note', help)

        printtextarea('Note to Moderator', 'mod_note', help)

	print '</tbody>'
	print '</table>'
	print '<p>'

	print '<input name="award_cat_type_id" value="%d" type="HIDDEN">' % (award_type_id)
	print '<input type="SUBMIT" value="Submit New Award Category" tabindex="1">'
	print '</form>'

	PrintPostSearch(0, 0, 0, 0, 0)
