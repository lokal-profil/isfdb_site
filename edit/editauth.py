#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2018   Al von Ruff, Ahasuerus and Bill Longley
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
from isfdblib import *
from isfdb import *
from SQLparsing import *
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
		authorID = int(sys.argv[1])
		# If the argument is non-numeric, raise an error
		if authorID < 1:
			raise
                record = SQLloadAuthorData(authorID)
                # If there is no author record with this ID on file, raise an error
                if not record:
                        raise
	except:
		PrintPreSearch("Author Editor - Non-Existing Author")
		PrintNavBar("edit/editauth.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Author Editor")
	PrintNavBar("edit/editauth.cgi", str(authorID))
        help = HelpAuthor()

        printHelpBox('author', 'AuthorData')

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitauth.cgi" onsubmit="return validateAuthorForm()" >'
	
	print '<table border="0">'
	print '<tbody id="tagBody">'

        # Limit the ability to edit canonical author names to moderators
        user = User()
        user.load()
	display_only = 1
	if SQLisUserModerator(user.id):
                display_only = 0
	printfield("Canonical Name", "author_canonical",  help, record[AUTHOR_CANONICAL], display_only)

        trans_names = SQLloadTransAuthorNames(record[AUTHOR_ID])
        printmultiple(trans_names, "Transliterated Name", "trans_names", "AddTransName", help)

	printfield("Legal Name",     "author_legalname",  help, record[AUTHOR_LEGALNAME])
        trans_legal_names = SQLloadTransLegalNames(record[AUTHOR_ID])
        printmultiple(trans_legal_names, "Trans. Legal Name", "trans_legal_names", "AddTransLegalName", help)

	printfield("Directory Entry","author_lastname",   help, record[AUTHOR_LASTNAME])
	printfield("Birth Place",    "author_birthplace", help, record[AUTHOR_BIRTHPLACE])
	printfield("Birth Date",     "author_birthdate",  help, record[AUTHOR_BIRTHDATE])
	printfield("Death Date",     "author_deathdate",  help, record[AUTHOR_DEATHDATE])

	printlanguage(record[AUTHOR_LANGUAGE], "author_language", "Working Language", help)

        emails = SQLloadEmails(record[AUTHOR_ID])
        printmultiple(emails, "Email Address", "author_emails", "AddEmail", help)

        webpages = SQLloadWebpages(record[AUTHOR_ID])
        printWebPages(webpages, 'author', help)

	printfield("Author Image",          "author_image",     help, record[AUTHOR_IMAGE])
	
        printtextarea('Note', 'author_note', help, record[AUTHOR_NOTE])

        printtextarea('Note to Moderator', 'mod_note', help)

	print '</table>'

	print '<p>'
	print '<input NAME="author_id" VALUE="%d" TYPE="HIDDEN">' % authorID
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)

