#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2017   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.9 $
#     Date: $Date: 2017/02/24 01:15:39 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import printfield, printtextarea


if __name__ == '__main__':

	try:
		arg = int(sys.argv[1])
                title = SQLloadTitle(arg)
                if not title:
                        raise
	except:
		PrintPreSearch("Link Review")
		PrintNavBar("edit/linkreview.cgi", 0)
		print '<h3>Invalid review record</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Link Review")
	PrintNavBar("edit/linkreview.cgi", arg)

	print '<div id="HelpBox">'
        print "<b>Help on linking reviews: </b>"
        print '<a href="http://%s/index.php/Help:Screen:LinkReview">Help:Screen:LinkReview</a><p>' % (WIKILOC)
	print '</div>'

        help = HelpGeneral()

	print "Linking the following review to the specified title:<p>"

	print "<b>Title:</b>", title[TITLE_TITLE]
	print "<br>"

	authors = SQLTitleAuthors(arg)
	print "<b>Author:</b>"
	counter = 0
	for author in authors:
		if counter:
			print " <b>and</b> "
		print author
		counter += 1
	print "<br>"

	print "<b>Date:</b>", title[TITLE_YEAR]
	print "<br>"
	print "<b>Type:</b>", title[TITLE_TTYPE]
	print "<br>"

	print "<p>"
	print "<hr>"
	print "<p>"

	title_id = SQLfindReviewedTitle(arg)

	##################################################################
	# Section 1
	##################################################################
	print "Enter the record number of the title that this review refers to or 0 to break the link:"
	print "<p>"

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitlinkreview.cgi">'
	print '<table border="0">'
        print '<tbody id="tagBody">'

        if title_id:
                printfield("Title #", "Parent", help, title_id)
        else:
                printfield("Title #", "Parent", help, '')

        printtextarea('Note to Moderator', 'mod_note', help, '')
        print '</tbody>'
        print '</table>'
	print '<p>'

	print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % arg
	print '<input TYPE="SUBMIT" VALUE="Link to Title" tabindex="1">'
	print "</form>"

	print "<p>"
	print "<hr>"
	print "<p>"


	PrintPostSearch(0, 0, 0, 0, 0)
