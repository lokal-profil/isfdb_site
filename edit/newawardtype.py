#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2016/04/30 04:41:18 $


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

        (userid, username, usertoken) = GetUserData()
        if SQLisUserBureaucrat(userid) == 0:
		PrintPreSearch("Add New Award Type - Limited to Bureaucrats")
		PrintNavBar("edit/newawardtype.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Add New Award Type")
	PrintNavBar("edit/addawardtype.cgi", 0)

        help = HelpAwardType()

        printHelpBox('Award Type', 'AwardType')

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitnewawardtype.cgi" onsubmit="return validateAwardTypeForm()">'

	print '<table border="0">'
	print '<tbody id="tagBody">'

	printfield('Short Name',      'award_type_short_name', help)

	printfield('Full Name',       'award_type_name',       help)

	printfield('Awarded For',     'award_type_for',        help)

	printfield('Awarded By',      'award_type_by',         help)

        values = {}
        values['No'] = 1
        values['Yes'] = ''
        printdropdown('Poll', 'award_type_poll', values, help)

        values = {}
        values['No'] = 1
        values['Yes'] = ''
        printdropdown('Non-Genre', 'award_type_non_genre', values, help)

        printWebPages([], 'award_type', help)

        printtextarea('Note', 'award_type_note', help)

	print '</table>'

	print '<p>'
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)

