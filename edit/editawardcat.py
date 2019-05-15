#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2018   Ahasuerus
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
from awardcatClass import *
from isfdblib import *
from isfdblib_help import *
from isfdb import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
                awardCat = award_cat()
                awardCat.award_cat_id = int(sys.argv[1])
                awardCat.load()
		if not awardCat.award_cat_name:
			raise
	except:
		PrintPreSearch("Award Category Editor - Argument Error")
		PrintNavBar("edit/editawardcat.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
		
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Award Category Editor")
	PrintNavBar("edit/editawardcat.cgi", awardCat.award_cat_id)

        help = HelpAwardCat()

        printHelpBox('Award Category', 'AwardCat')


	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitawardcat.cgi">'

	print '<table border="0">'
	print '<tbody id="tagBody">'

	printfield('Award Category',       'award_cat_name',       help, awardCat.award_cat_name)

	printfield('Display Order',       'award_cat_order',    help, awardCat.award_cat_order)

        printWebPages(awardCat.award_cat_webpages, 'award_cat', help)

        printtextarea('Note', 'award_cat_note', help, awardCat.award_cat_note)

	print '</table>'

	print '<p>'
	print '<input NAME="award_cat_type_id" VALUE="%d" TYPE="HIDDEN">' % awardCat.award_cat_type_id
	print '<input NAME="award_cat_id" VALUE="%d" TYPE="HIDDEN">' % awardCat.award_cat_id
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)

