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
import MySQLdb
from SQLparsing import *
from pubClass import pubs
from isfdb import *
from library import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *


def SQLCountPubs(record):
        # Retrieve the number of pubs that this title exists in
        query = "select count(*) from pub_content where title_id = %d;" % (int(record[TITLE_PUBID]))
        db.query(query)
        result = db.store_result()
        result_record = result.fetch_row()
        #If this Title exists in more than 1 pub, make it display-only
        if result_record:
                if result_record[0][0] > 1:
                        return 1
        return 0


###################################################################
# This function outputs a title record in table format
###################################################################
def printtitlerecord(record, index, container, help):
        args = ' class="%s"'
        readonly = False
        # Find out if the title is in more than 1 publication
        manypubs = SQLCountPubs(record)
        if manypubs:
                readonly = True
                # Titles in multiple pubs are gray
                args = ' READONLY class="%s titlemultiple"'
        # Containers in just 1 publication are yellow
        elif container:
                args = ' class="%s titlecontainer"'

        if readonly:
                taborder = 0
        else:
                taborder = 1

        print '<tr><td>'
        print '<input name="title_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])
        page = getPageNumber(record[TITLE_PUBID], pub_id)
	# Container titles shouldn't have page numbers, so the page field is not editable
        if container:
                print '<input name="title_page%d" tabindex="0" READONLY class="contentpageinput titlemultiple"></td>' % index
        # Non-container page numbers are always editable even for read-only titles
        else:
                if page:
                        print '<input name="title_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page))
                else:
                        print '<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index)

        print '<td><input name="title_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="title_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput")

	###################################
	# Title type
	###################################
	if readonly:
                print '<td><input name="title_ttype%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_TTYPE], args % "contenttypeinput")
        else:
                print '<td><select name="title_ttype%d" tabindex="%d" %s>' % (index, taborder, args % "contenttypeinput")
                for ttype in REGULAR_TITLE_TYPES:
                        if (record and record[TITLE_TTYPE] == ttype) or (not record and ttype == 'SHORTFICTION'):
                                print '<option selected="selected">%s</option>' % ttype
                        else:
                                print '<option>%s</option>' % ttype
                print '</select></td>'

	###################################
	# STORYLEN
	###################################
        length = ''
        if record[TITLE_STORYLEN]:
                length = record[TITLE_STORYLEN]
	if readonly:
                print '<td><input name="title_storylen%d" value="%s" tabindex="%d"%s></td>' % (index, length, taborder, args % "contentleninput")
        else:
                print '<td><select name="title_storylen%d" tabindex="%d"%s>' % (index, taborder, args % "contentleninput")
                for storylen in STORYLEN_CODES:
                        if record and length == storylen:
                                print '<option selected="selected">%s</option>' % storylen
                        else:
                                print '<option>%s</option>' % storylen
                print '</select></td>'
        print '</tr>'

	###################################
	# AUTHORS
	###################################

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        counter = 1
        if len(authors):
                for author in authors:
			print '<tr>'
			printContentHeader('Author%d:'% counter, help)
			print '<td><input name="title_author%d.%d" tabindex="%d" value="%s"%s></td>' % (index, counter, taborder, escape_string(author), args % "contentinput")
			print '</tr>'
                        counter += 1
	else:
		print '<tr>'
		printContentHeader('Author%d:'% counter, help)
		print '<td><input name="title_author%d.%d" tabindex="%d" %s></td>' % (index, counter, taborder, args % "contentinput")
		print '</tr>'
		counter += 1

        if not readonly:
                printAddContentAuthor('Author', help, index, counter)

        printSpacer(5, 'title', index)


def printreviewrecord(record, index, help):
        # Find out if this title is in more than 1 publication
        manypubs = SQLCountPubs(record)
        if manypubs:
                readonly = True
                args = ' READONLY class="%s titlemultiple"'
                taborder = 0
        else:
                readonly = False
                args = ' class="%s"'
                taborder = 1

        print '<tr><td>'
        print '<input name="review_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])
        page = getPageNumber(record[TITLE_PUBID], pub_id)
	# Page numbers are always editable and included in the tab order
	if page:
		print '<input name="review_page%d" value="%s" tabindex="1" class="contentpageinput"></td>' % (index, escape_string(page))
	else:
		print '<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % (index)

        print '<td><input name="review_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="review_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput")
        print '</tr>'

	counter = 1
        authors = SQLReviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        printContentHeader('Author%d:'% counter, help)
                        print '<td><input name="review_author%d.%d" tabindex="%d" value="%s"%s></td>' % (index, counter, taborder, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

        if not readonly:
                printAddContentAuthor('Reviewee', help, index, counter)

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        printContentHeader('Reviewer%d:'% counter, help)
                        print '<td><input name="review_reviewer%d.%d" tabindex="%d" value="%s"%s></td>' % (index, counter, taborder, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

        if not readonly:
                printAddSecondaryAuthor('Reviewer', help, index, counter)

        printSpacer(3, 'review', index)


def printinterviewrecord(record, index, help):
        # Find out if this title is in more than 1 publication
        manypubs = SQLCountPubs(record)
        if manypubs:
                readonly = True
                args = ' READONLY class="%s titlemultiple"'
                taborder = 0
        else:
                readonly = False
                args = ' class="%s"'
                taborder = 1

        print '<tr><td>'
        print '<input name="interview_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])
        page = getPageNumber(record[TITLE_PUBID], pub_id)
	# Page numbers are always editable and belong to the primary tab group
	if page:
		print '<input name="interview_page%d" value="%s" tabindex="1" class="contentpageinput"></td>' % (index, escape_string(page))
	else:
		print '<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % index

        print '<td><input name="interview_title%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, escape_string(record[TITLE_TITLE]), args % "contentinput")

        print '<td><input name="interview_date%d" tabindex="%d" value="%s"%s></td>' % (index, taborder, record[TITLE_YEAR], args % "contentyearinput")
        print "</tr>"

        counter = 1
        authors = SQLInterviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        printContentHeader('Interviewee%d:'% counter, help)
                        print '<td><input name="interviewee_author%d.%d" tabindex="%d" value="%s"%s></td>' % (index, counter, taborder, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

        if not readonly:
                printAddContentAuthor('Interviewee', help, index, counter)

	print '<tr>'
        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        printContentHeader('Interviewer%d:'% counter, help)
                        print '<td><input name="interviewer_author%d.%d" tabindex="%d" value="%s"%s></td>' % (index, counter, taborder, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1
        print '</tr>'

        if not readonly:
                printAddSecondaryAuthor('Interviewer', help, index, counter)

	printSpacer(3, 'interview', index)


###################################################################
# This function outputs a publication record in table format
###################################################################
def printpubrecord(pub):
        help = HelpPub()
	print '<h2>Publication Metadata</h2>'
	print '<table id="metadata">'
	print '<tbody id="pubBody">'
	printfield("Title", "pub_title", help, pub.pub_title)
        trans_titles = SQLloadTransPubTitles(pub.pub_id)
        printmultiple(trans_titles, "Transliterated Title", "trans_titles",
                      "AddTransTitle", "AddMultipleField", help,
                      "'%s', '%s', '%s'" % ('Transliterated Title', 'trans_titles', 'pubBody'))

	authors = SQLPubAuthors(pub.pub_id)
	counter = 1
	if len(authors):
		for author in authors:
                        printfield('Author%d' % counter, 'pub_author%d' % counter, help, author)
			counter += 1
	else:
		printfield('Author%d' % counter, 'pub_author%d' % counter, help)
		counter += 1

        printAddAuthor('Author', help, counter)
	printfield("Date", "pub_year", help, pub.pub_year)
        printfield("Publisher", "pub_publisher", help, pub.pub_publisher)
	printfield("Pages", "pub_pages", help, pub.pub_pages)
	printformat("pub_ptype", "Format", help, pub.pub_ptype)

	print '<tr>'
	printContentHeader('Pub Type:', help)
        print '<td><select tabindex="1" name="pub_ctype" class="metainputselect">'
        print '<option selected="selected">%s</option>' % pub.pub_ctype
        for ctype in ['ANTHOLOGY','CHAPBOOK','COLLECTION','FANZINE','MAGAZINE','NONFICTION','NOVEL','OMNIBUS']:
		if ctype != pub.pub_ctype:
        		print '<option>%s</option>' % (ctype)
        print '</select>'
        print '</tr>'

        printISBN(help, pub.pub_isbn)
	printfield("Catalog ID", "pub_catalog", help, pub.pub_catalog)
	printfield("Price", "pub_price", help, pub.pub_price)
	printfield("Image URL", "pub_image", help, pub.pub_image)
	printfield("Pub Series", "pub_series", help, pub.pub_series)
        printfield("Pub Series #", "pub_series_num", help, pub.pub_series_num)
        printtextarea('Pub Note', 'pub_note', help, pub.pub_note)
        printExternalIDs(pub.identifiers, "External ID", "external_id", help)
        printtextarea('Note to Moderator', 'mod_note', help)

	print '</tbody>'
        print '</table>'

if __name__ == '__main__':

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Publication Editor")
	try:
		pub_id = int(sys.argv[1])
                pub = pubs(db)
                pub.load(pub_id)
                if pub.error:
                        raise
	except:
        	PrintNavBar('edit/editpub.cgi', 0)
        	print "<h3>Missing or Invalid publication ID</h3>"
        	PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	PrintNavBar('edit/editpub.cgi', pub_id)

        titles = getSortedTitlesInPub(pub_id)
        covers = SQLPubCovers(pub_id)

        printHelpBox('publication', 'EditPub')

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitpub.cgi" onsubmit="return validatePubForm()">'

        printpubrecord(pub)

        print '<hr class="topspace">'
        print '<h2 class="editheadline">Content</h2>'
        print """<ul>
                <li>White: non-container titles appearing only in this publication; can be edited
                <li>Yellow: container titles appearing only in this publication; can be edited except for page numbers and OMNIBUS length
                <li>Gray: titles appearing in multiple publications; cannot be edited here
                <li>See <a href="http://%s/index.php/Help:How to change a story in a collection">Help:How
                to change a story in a collection</a> for details.
                </ul>"""  % (WIKILOC)
        print '<p>'

        print '<hr class="topspace">'
        # Retrieve the Help text for covers
        help = HelpCoverArt()
        print "<h2>Cover Art</h2>"
        print '<table class="coveredit">'
        print '<tbody id="coverBody">'

        if not covers:
                index = 1
                printbriefblankcoverart(index, help)
                index += 1
                printNewBriefCoverButton()
        else:
                print '<tr>'
                print '<td>&nbsp;</td>'
                printContentHeader('Title', help)
                printContentHeader('Date', help)
                print '</tr>'
                index = 1
                for cover in covers:
                        # Find out if this cover is in more than 1 publication
                        manypubs = SQLCountPubs(cover)
                        if manypubs:
                                printfullcoverart(cover, index, help, 1)
                        else:
                                printfullcoverart(cover, index, help, 0)
                        index += 1
                printNewFullCoverButton()
        print "</tbody>"
        print "</table>"

        # Retrieve the Help text for publication content
        help = HelpTitleContent()
        print '<hr class="topspace">'
        print '<h2 class="editheadline">Regular Titles</h2>'
        print '<table class="titleedit">'
        print '<tbody id="titleBody">'

        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        printContentHeader('Title Type', help)
        printContentHeader('Length', help)
        print '</tr>'

	normal_titles = []
	container_titles = []
	review_titles = []
	interview_titles = []

        for title in titles:
                if title[TITLE_TTYPE] == 'COVERART':
                        continue
                elif title[TITLE_TTYPE] == 'EDITOR':
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'OMNIBUS') and (pub.pub_ctype == 'OMNIBUS'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'COLLECTION') and (pub.pub_ctype == 'COLLECTION'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'ANTHOLOGY') and (pub.pub_ctype == 'ANTHOLOGY'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'CHAPBOOK') and (pub.pub_ctype == 'CHAPBOOK'):
                        container_titles.append(title)
                elif (title[TITLE_TTYPE] == 'REVIEW'):
                        review_titles.append(title)
                elif (title[TITLE_TTYPE] == 'INTERVIEW'):
                        interview_titles.append(title)
                else:
                        normal_titles.append(title)

        index = 1
	if container_titles:
                for title in container_titles:
                        printtitlerecord(title, index, 1, help)
                        index += 1

	if normal_titles:
                for title in normal_titles:
                        printtitlerecord(title, index, 0, help)
                        index += 1
        
        if index == 1:
                printblanktitlerecord(index, help, pub.pub_ctype)
                index += 1
        printNewTitleButton()
        print "</tbody>"
        print "</table>"

        print '<hr class="topspace">'
        # Retrieve the Help text for reviews
        help = HelpReviewContent()
        print '<h2 class="editheadline">Reviews</h2>'
        print '<table class="reviewedit">'
        print '<tbody id="reviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Title', help)
        printContentHeader('Date', help)
        print '</tr>'
        index = 1
        if review_titles:
                for title in review_titles:
                        printreviewrecord(title, index, help)
                        index += 1
        else:
                printblankreviewrecord(index, help)
                index += 1
        printNewReviewButton()
        print "</tbody>"
        print "</table>"

        print '<hr class="topspace">'
        # Retrieve the Help text for interviews
        help = HelpInterviewContent()
        print '<h2 class="editheadline">Interviews</h2>'
        print '<table class="interviewedit">'
        print '<tbody id="interviewBody">'
        print '<tr>'
        printContentHeader('Page', help)
        printContentHeader('Interview Title', help)
        printContentHeader('Date', help)
        print '</tr>'
        index = 1
        if interview_titles:
                for title in interview_titles:
                        printinterviewrecord(title, index, help)
                        index += 1
        else:
                printblankinterviewrecord(index, help)
                index += 1
        printNewInterviewButton()
        print "</tbody>"
        print "</table>"

        print "<hr class=\"topspace\">"
	print "<p>"
	print '<input name="pub_id" value="%d" type="HIDDEN">' % pub_id
	print '<input name="editor" value="editpub" type="HIDDEN">'
	print '<input type="SUBMIT" value="Submit Changed Data" tabindex="1">'
	print "</form>"
        print "<hr class=\"topspace\">"
	print ISFDBLink("edit/deletepub.cgi", pub_id, "Delete record")

        PrintPostSearch(tableclose=False)
