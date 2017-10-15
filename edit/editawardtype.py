#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.14 $
#     Date: $Date: 2016/04/30 04:43:37 $


import cgi
import sys
import MySQLdb
from awardtypeClass import *
from isfdblib import *
from isfdblib_help import *
from isfdb import *
from SQLparsing import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
		award_type_id = str(sys.argv[1])
		if int(award_type_id) < 1:
			raise
	except:
		PrintPreSearch("Award Type Editor - Argument Error")
		PrintNavBar("edit/editawardtype.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
		
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Award Type Editor")
	PrintNavBar("edit/editawardtype.cgi", award_type_id)

        help = HelpAwardType()

        printHelpBox('Award Type', 'AwardType')

	award_type = award_type()
	award_type.award_type_id = award_type_id
	award_type.load()

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitawardtype.cgi" onsubmit="return validateAwardTypeForm()">'

	print '<table border="0">'
	print '<tbody id="tagBody">'

	printfield('Short Name',      'award_type_short_name', help, award_type.award_type_short_name)

	printfield('Full Name',       'award_type_name',       help, award_type.award_type_name)

	printfield('Awarded For',     'award_type_for',        help, award_type.award_type_for)

	printfield('Awarded By',      'award_type_by',         help, award_type.award_type_by)

        values = {}
        if award_type.award_type_poll == 'Yes':
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Poll', 'award_type_poll', values, help)

        values = {}
        if award_type.award_type_non_genre == 'Yes':
                values['Yes'] = 1
                values['No'] = 0
        else:
                values['Yes'] = 0
                values['No'] = 1
        printdropdown('Non-Genre', 'award_type_non_genre', values, help)

        printWebPages(award_type.award_type_webpages, 'award_type', help)

        printtextarea('Note', 'award_type_note', help, award_type.award_type_note)

	print '</table>'

	print '<p>'
	print '<input NAME="award_type_id" VALUE="' + str(award_type.award_type_id) + '" TYPE="HIDDEN">'
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)

