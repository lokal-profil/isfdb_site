#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2018   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
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
from library import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from isfdblib_print import *


def printtitlerecord(record):
        help = HelpTitle()
        
	print '<table border="0">'
        print '<tbody id="titleBody">'

	printfield("Title", "title_title", help, record[TITLE_TITLE])

        printmultiple([], "Transliterated Title", "trans_titles", help)

	authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "title_author", help)

	printfield("Date", "title_copyright", help, record[TITLE_YEAR])

        printlanguage(record[TITLE_LANGUAGE], 'language', 'Language', help)

        printtitletype(record[TITLE_TTYPE], help)

        printlength(record[TITLE_STORYLEN], help)

        printtextarea('Note', 'title_note', help, SQLgetNotes(record[TITLE_NOTE]), 10)

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print '</tbody>'
        print '</table>'

if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################

        try:
                title_id = int(sys.argv[1])
        except:
                displayError('Missing title ID', 'Add Variant Title', 'addvariant')

        title_data = SQLloadTitle(title_id)
        if not title_data:
                displayError('Non-existent parent title ID specified', 'Add Variant Title', 'addvariant')

	PrintPreSearch("Add Variant Title")
	PrintNavBar("edit/addvariant.cgi", title_id)

        if title_data[TITLE_PARENT]:
                displayError('This title is currently a variant of another title. Variants of variants are not allowed')

	print '<div id="HelpBox">'
	print "<b>Help on adding variant titles: </b>"
	print '<a href="http://%s/index.php/Help:Screen:AddVariant">Help:Screen:AddVariant</a><p>' % (WIKILOC)
	print '</div>'

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitvariant.cgi" onsubmit="return validateVariantTitleForm()">'
	printtitlerecord(title_data)

	print "<p>"
	print "<hr>"
	print "<p>"
	print "<input NAME=\"title_id\" VALUE=\""+sys.argv[1]+"\" TYPE=\"HIDDEN\">"
	print "<input TYPE=\"SUBMIT\" VALUE=\"Submit Data\">"
	print "</form>"
	print "<p>"

	PrintPostSearch(0, 0, 0, 0, 0)
