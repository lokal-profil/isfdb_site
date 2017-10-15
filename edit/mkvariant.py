#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.28 $
#     Date: $Date: 2017/02/24 14:58:07 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from library import *


if __name__ == '__main__':

	try:
		title_id = int(sys.argv[1])
                title = SQLloadTitle(title_id)
                if not title:
                        raise
	except:
		PrintPreSearch("Make Variant Title")
		PrintNavBar("edit/mkvariant.cgi", 0)
		print '<h3>Missing or non-existent title</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Make Variant Title")
	PrintNavBar("edit/mkvariant.cgi", title_id)

        help = HelpMakeVariant()

	print '<div id="HelpBox">'
        print "<b>Help on making variant titles: </b>"
        print '<a href="http://%s/index.php/Help:Screen:MakeVariant">Help:Screen:MakeVariant</a><p>' % (WIKILOC)
	print '</div>'

	print "Current Title:<br>"

	print "<b>Title:</b>", escape_string(title[TITLE_TITLE])
	print "<br>"

	authors = SQLTitleAuthors(title_id)
	print "<b>Author:</b>"
	counter = 0
	for author in authors:
		if counter:
			print " <b>and</b> "
		print escape_string(author)
		counter += 1
	print "<br>"

	print "<b>Date:</b>", title[TITLE_YEAR]
	print "<br>"
	print "<b>Type:</b>", title[TITLE_TTYPE]
	print "<p>"

	##################################################################
	# Data Entry Form 1
	##################################################################
	print '<hr class="divider">'
	print '<p>'
	print '<h2>Option 1</h2>'
	print "<p>"

	print "If the parent title already exists, enter its record number below."
	print "To BREAK an existing Variant link, enter 0."
	print "<p>"

	print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitmkvar1.cgi" onsubmit="return validateParentTitle()">'
	print "<table border=\"0\">"
        print '<tbody>'
	if title[TITLE_PARENT] > 0:
		printfield("Parent #", "Parent", help, title[TITLE_PARENT])
	else:
		printfield("Parent #", "Parent", help)

        printtextarea('Note to Moderator', 'mod_note', help)

        print '</tbody>'
        print '</table>'
	print '<p>'

	print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title_id)
	print '<input TYPE="SUBMIT" VALUE="Link to Existing Parent" tabindex="1">'
	print '</form>'

	print '<p>'

	##################################################################
	# Data Entry Form 2
	##################################################################
	print '<hr class="divider">'
	print '<p>'
	print '<h2>Option 2</h2>'
	print "If the parent title does not exist, enter the title information below to create it."
	print "<p>"

	print '<form METHOD="POST" ACTION="/cgi-bin/edit/submitmkvar2.cgi" onsubmit="return validateVariantTitleForm()">'
	print "<table border=\"0\">"
        print '<tbody id="titleBody">'

        printfield("Title", "title_title", help, title[TITLE_TITLE])
        trans_titles = SQLloadTransTitles(title[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles",
                      "AddTransTitle", "AddMultipleField", help,
                      "'%s', '%s', '%s', '%s'" % ('AddTransTitle', 'Transliterated Title', 'trans_titles', 'titleBody'))

	counter = 1
	for author in authors:
                printfield('Author'+str(counter), 'title_author'+str(counter), help, author)
		counter += 1

        print '<tr id="AddAuthor" next="%d">' % counter
        print '<td><input type="button" value="Add Author" onclick="addMetadataTitleAuthor()" tabindex="1"></td>'
        print '<td> </td>'
        print '</tr>'

        printfield("Date", "title_copyright", help, title[TITLE_YEAR])

	print '<tr>'
	printfieldlabel('Title Type', help)
        print '<td><select name="title_ttype" tabindex="1">'
	for ttype in ['ANTHOLOGY','CHAPBOOK','COLLECTION','COVERART', 'EDITOR', 'ESSAY', 'INTERIORART', 'INTERVIEW', 'NONFICTION', 'NOVEL','OMNIBUS','POEM','REVIEW','SERIAL','SHORTFICTION']:
		if ttype ==  title[TITLE_TTYPE]:
			print '<option selected="selected">' +ttype+ '</option>'
		else:
        		print '<option>' +ttype+ '</option>'
        print '</select></td>'
        print '</tr>'

        printlanguage(title[TITLE_LANGUAGE], 'language', 'Language', help)
	
        printtextarea('Note to Moderator', 'mod_note', help)

        print '</tbody>'
        print '</table>'
	print '<p>'

        print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title_id)
	print '<input TYPE="SUBMIT" VALUE="Create New Parent Title" tabindex="1">'
	print '</form>'


	PrintPostSearch(tableclose=False)
