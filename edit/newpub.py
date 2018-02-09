#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2018   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
		pub_type = sys.argv[1]
                pub_ctype = pub_type.upper()
		if pub_ctype not in PUB_TYPES:
                        raise
	except:
		PrintPreSearch("Publication Editor")
		PrintNavBar('edit/newpub.cgi', 0)
                print '<h3>Invalid Publication Type</h3>'
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)

        PrintPreSearch("New %s" % pub_type)

	PrintNavBar('edit/newpub.cgi', pub_type)

	print '<div id="HelpBox">'
        print '<b>Help on adding new publication records: </b>'
        print '<a href="http://%s/index.php/Help:Screen:NewPub">Help:Screen:NewPub</a><p>' % (WIKILOC)
	print '</div>'

	##################################################################
	# Output the leading HTML stuff
	##################################################################

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitnewpub.cgi" onsubmit="return validatePubForm()">'

        # Retrieve the Help text for publication metadata
        help = HelpPub()

        # Title level data
	print '<h2>Title Data</h2>'
	print '<table border="0" id="referenceTitle">'
	print '<tbody id="referenceBody">'

	printfield("Title", "pub_title", help)

        printmultiple([], "Transliterated Title", "trans_titles",
                      "AddTransTitle", "AddMultipleField", help,
                      "'%s', '%s', '%s'" % ('Transliterated Title', 'trans_titles', 'referenceBody'))

	if pub_type in ('Chapbook', 'Collection', 'Nonfiction', 'Novel'):
                author_or_editor = 'Author'
        else:
                author_or_editor = 'Editor'
	printfield(author_or_editor+'1', 'pub_author1', help)

        printAddAuthor(author_or_editor, help, 'referenceBody')

        printlanguage('','language','Language',help)

        # CHAPBOOK records cannot have series or Synopsis data
        readonly = 0
	if pub_type == 'Chapbook':
		readonly = 1

	printfield("Series", "title_series", help, '', readonly)
	printfield("Series Num", "title_seriesnum", help, '', readonly)

        # Only Omnibus titles can have Content data
	if pub_type == 'Omnibus':
                printfield("Content", "title_content", help, '')
        else:
                printfield("Content", "title_content", help, '', 1)

        printcheckbox('Juvenile', 'title_jvn', '', '', help)

        printcheckbox('Novelization', 'title_nvz', '', '', help)

        printcheckbox('Non-Genre', 'title_non_genre', '', '', help)
	
        printcheckbox('Graphic Format', 'title_graphic', '', '', help)

        printtextarea('Synopsis', 'title_synopsis', help, '', 4, readonly)

        printtextarea('Title Note', 'title_note', help, '', 2)
        
        printWebPages([], 'title', help, 'referenceBody')

	print '</tbody>'
        print '</table>'

        # At this point we are done with title-specific data. The next section is publication-specific data.
	print '<h2>Publication Data</h2>'
	print '<table border="0" id="metadata">'
	print '<tbody id="pubBody">'

        printfield("Publication Type", "pub_ctype", help, pub_ctype, 1)

	printfield("Date", "pub_year", help)
	printfield("Publisher", "pub_publisher", help)
	printfield("Pages", "pub_pages", help)
	
	printformat("pub_ptype", "Format", help)

	printfield("ISBN", "pub_isbn", help)
	printfield("Catalog ID", "pub_catalog", help)
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
        printNewBriefCoverButton()

        print '</tbody>'
        print '</table>'

        #################################
        # Content section: regular Titles
        #################################
        print '<p>'
        print '<hr>'
        print '<p>'
        help = HelpTitleContent()
        if pub_type == 'Novel':
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
        # Display only 3 (i.e. 4-1) blank Content titles for Novels to account for essays, interior art, etc
        if pub_type == 'Novel':
                max = 4
        while counter < max:
                printblanktitlerecord(counter, help, pub_ctype)
                counter += 1
        printNewTitleButton()
        print "</tbody>"
        print "</table>"
        print '<p>'
        print '<hr>'
        print '<p>'

        ################################
        # Content section: Review Titles
        ################################
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
        # Display only 1 blank Content review for Novels
        if pub_type == 'Novel':
                max = 2
        while counter < max:
                printblankreviewrecord(counter, help)
                counter += 1

        printNewReviewButton()
        print "</tbody>"
        print "</table>"

        print '<p>'
        print '<hr>'
        print '<p>'

        ###################################
        # Content section: Interview Titles
        ###################################
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
        # Display only 1 blank Content interview for new Novel pubs
        if pub_type == 'Novel':
                max = 2
        while counter < max:
                printblankinterviewrecord(counter, help)
                counter += 1

        printNewInterviewButton()

        print "</tbody>"
        print "</table>"

	print "<p>"
	print "<hr>"
	print "<p>"
	print '<input name="pub_id" VALUE="0" type="HIDDEN">'
	print '<input tabindex="1" type="SUBMIT" VALUE="Submit Data">'
	print "</form>"
	print "<p>"

        PrintPostSearch(tableclose=False)
