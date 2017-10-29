#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2017   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.32 $
#     Date: $Date: 2017/06/16 20:19:37 $


import cgi
import sys
import MySQLdb
from SQLparsing import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
		title = int(sys.argv[1])
                record = SQLloadTitle(title)
        	pub_type = record[TITLE_TTYPE]
                if not record:
                        raise
		pub = 0
	except:
		PrintPreSearch("Specified Title record not found")
		PrintNavBar("edit/addpub.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	if pub_type not in ('NOVEL', 'COLLECTION', 'OMNIBUS', 'ANTHOLOGY', 'CHAPBOOK', 'NONFICTION'):
		PrintPreSearch("Adding a publication to a " + pub_type + " record is not supported")
		PrintNavBar("edit/addpub.cgi", 0)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Add Publication")
	PrintNavBar("edit/addpub.cgi", sys.argv[1])

        print '<div id="HelpBox">'
        print '<b>Help on adding new publication records: </b>'
        print '<a href="http://%s/index.php/Help:Screen:AddPublication">Help:Screen:AddPublication</a><p>' % (WIKILOC)
        print '</div>'

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitaddpub.cgi" onsubmit="return validatePubForm()">'
	print '<h2>Publication Metadata</h2>'
	print '<table class="pub_metadata" id="metadata">'
	print '<tbody id="pubBody">'

        help = HelpPub()

	printfield("Title", "pub_title", help, record[TITLE_TITLE], 1)

        trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles",
                      "AddTransTitle", "AddMultipleField", help,
                      "'%s', '%s', '%s', '%s'" % ('AddTransTitle', 'Transliterated Title', 'trans_titles', 'pubBody'), 1)

	authors = SQLTitleAuthors(record[TITLE_PUBID])
	counter = 1
	if len(authors):
		for author in authors:
			printfield('Author%s' % (counter), 'pub_author%s' % (counter), help, author, 1)
			counter += 1
	else:
		printfield('Author%s' % (counter), 'pub_author%s' % (counter), help, '', 1)
		counter += 1

	printfield("Date", "pub_year", help)
	printfield("Publisher", "pub_publisher", help)
	printfield("Pages", "pub_pages", help)

	printformat("pub_ptype", "Format", help)

	printfield("Pub Type", "pub_ctype", help, pub_type, 1)

	printfield("ISBN / Catalog #", "pub_isbn", help)
	printfield("Price", "pub_price", help)

	printfield("Image URL", "pub_image", help)

	printfield("Pub Series", "pub_series", help)
	printfield("Pub Series #", "pub_series_num", help)

        printsource(help)

        printtextarea('Pub Note', 'pub_note', help)
        printExternalIDs(None, "External ID", "external_id", help)
        printtextarea('Note to Moderator', 'mod_note', help)

	print '</tbody>'
        print '</table>'

        print '<p>'
        print '<hr>'
        print '<p>'

        ###################
        # Cover Art section
        ###################
        help = HelpCoverArt()
        print '<h2 class="editheadline">Cover Art</h2>'
        print '<p>'
        print '<table class="coveredit">'
        print '<tbody id="coverBody">'

        printbriefblankcoverart(1, help)
        printNewBriefCoverButton(2)

        print "</tbody>"
        print "</table>"

        #################################
        # Regular Titles
        #################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        if pub_type == 'NOVEL':
                print '<h2>Additional Regular Titles</h2>'
        else:
                print '<h2>Regular Titles</h2>'
        print '<p>'

        print '<table class="titleedit">'
        print '<tbody id="titleBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print '</tr>'

        counter = 1
        max = 10
        # For NOVELs, display only 3 (i.e. 4-1) blank Content titles
        # to account for essays, interior art, bonus stories, etc
        if pub_type == 'NOVEL':
                max = 4
        while counter < max:
                printblanktitlerecord(counter, help, pub_type)
                counter += 1
        printNewTitleButton(counter)
        print "</tbody>"
        print "</table>"

        #####################################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for reviews
        help = HelpReviewContent()
        print '<h2>Reviews</h2>'
        print '<p>'

        print '<table class="reviewedit">'
        print '<tbody id="reviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        print '</tr>'

        counter = 1
        max = 4
        # For Novels, Display only 1 blank Content review
        if pub_type == 'NOVEL':
                max = 2
        while counter < max:
                printblankreviewrecord(counter, help)
                counter += 1

        printNewReviewButton(counter)
        print "</tbody>"
        print "</table>"

        #####################################################
        print '<p>'
        print '<hr>'
        print '<p>'
        # Retrieve the Help text for interviews
        help = HelpInterviewContent()
        print '<h2>Interviews</h2>'
        print '<p>'

        print '<table class="interviewedit">'
        print '<tbody id="interviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Interview Title', help)
        printContentHeader('Date', help)
        print '</tr>'

        counter = 1
        max = 3
        # For Novels, display only 1 blank Content interview
        if pub_type == 'NOVEL':
                max = 2
        while counter < max:
                printblankinterviewrecord(counter, help)
                counter += 1

        printNewInterviewButton(counter)

        print "</tbody>"
        print "</table>"


        print '<input tabindex="0" NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title)
        print '<input tabindex="0" name="editor" value="addpub" type="HIDDEN">'
        print '<input tabindex="0" NAME="pub_id" VALUE="%d" TYPE="HIDDEN">' % (pub)
        print '<input tabindex="1" TYPE="SUBMIT" VALUE="Submit Data">'
        print '</form>'
        print '<p>'
        print '<hr>'

        PrintPostSearch(tableclose=False)
