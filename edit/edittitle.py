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
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from library import *
from SQLparsing import *
from isfdblib_print import *

help = HelpTitle()


def printCommonSection(record, help):
	printfield("Date", "title_copyright",        help, record[TITLE_YEAR])

	series_name = ''
	if record[TITLE_SERIES]:
		series = SQLget1Series(record[TITLE_SERIES])
		series_name = series[SERIES_NAME]
        # Variant titles and CHAPBOOKS can't be in series. Consequently, the two
        # series-related fields are displayed as read-only for VTs and CHAPBOOKs
        # ***if*** these fields have no value. If there is a value on file, then
        # the field is editable to make it easy for editors to remove the value.
        if (record[TITLE_PARENT] or record[TITLE_TTYPE] == 'CHAPBOOK') and not series_name:
                readonly = 1
        else:
                readonly = 0
        printfield("Series", "title_series", help, series_name, readonly)
        if (record[TITLE_PARENT] or record[TITLE_TTYPE] == 'CHAPBOOK') and not series_number:
                readonly = 1
        else:
                readonly = 0
        printfield("Series Num", "title_seriesnum",  help, series_number, readonly)

	webpages = SQLloadTitleWebpages(record[TITLE_PUBID])
        printWebPages(webpages, 'title', help)

        printlanguage(record[TITLE_LANGUAGE], 'language', 'Language', help)


###################################################################
# This function outputs a title record in table format
###################################################################
def printtitlerecord(record, series_number):
	print '<table border="0">'
        print '<tbody id="titleBody">'

	printfield("Title", "title_title", help, record[TITLE_TITLE])
        trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", "AddTransTitle", help)

	authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "title_author", "AddAuthor", help)

        printCommonSection(record, help)

        printtitletype(record[TITLE_TTYPE], help)
        
        printlength(record[TITLE_STORYLEN], help)

        printfield('Content', 'title_content', help, record[TITLE_CONTENT])

        printcheckbox('Non-Genre', 'title_non_genre', record[TITLE_NON_GENRE], '', help)

        printcheckbox('Juvenile', 'title_jvn', record[TITLE_JVN], '', help)

        printcheckbox('Novelization', 'title_nvz', record[TITLE_NVZ], '', help)

        # COVERART and INTERIORART titles can't be "graphic", so we disable the checkbox
        disabled = ''
        if record[TITLE_TTYPE] in ('COVERART', 'INTERIORART'):
                disabled = 'disabled'
        printcheckbox('Graphic Format', 'title_graphic', record[TITLE_GRAPHIC], disabled, help)

        # CHAPBOOKS can't synopses. Consequently the Synopsis field is displayed
        # as read-only ***if*** there is no pre-existing value. If there is a value
        # on file, then the field is editable to make it easy for editors to remove
        # the value.
        readonly = 0
        if record[TITLE_TTYPE] == 'CHAPBOOK' and not record[TITLE_SYNOP]:
                readonly = 1
        printtextarea('Synopsis', 'title_synopsis', help, SQLgetNotes(record[TITLE_SYNOP]), 10, readonly)

        printtextarea('Title Note', 'title_note', help, SQLgetNotes(record[TITLE_NOTE]), 10)

        printtextarea('Note to Moderator', 'mod_note', help, '')

	print "</tbody>"
        print "</table>"

def printreviewrecord(record, series_number):
	print "<table border=\"0\">"

	printfield("Review of", "title_title", help, record[TITLE_TITLE])

	print '<tbody id="reviewBody">'
	print '<input name="review_id1" value="%s" type="HIDDEN">' % (record[TITLE_PUBID])

        trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", "AddTransTitle", help)

	authors = SQLReviewAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Author", "review_author1.", "AddReviewee1", help)

	authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Reviewer", "review_reviewer1.", "AddReviewer1", help)

	print "</tbody>"

        print '<tbody id="titleBody">'
        printCommonSection(record, help)

	print "<tr>"
	print "<td><b>Title Type</b></td>"
	print '<td><input name="title_ttype" value="REVIEW" READONLY class="titletype displayonly"></td>'
	print '</tr>'

        printtextarea('Note', 'title_note', help, SQLgetNotes(record[TITLE_NOTE]), 10)

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print "</tbody>"
        print "</table>"

def printinterviewrecord(record, series_number):
	print "<table border=\"0\">"

	printfield("Interview Title", "title_title", help, record[TITLE_TITLE])

	print '<tbody id="interviewBody">'
	print '<input name="interview_id1" value="%s" type="HIDDEN">' % (record[TITLE_PUBID])
        trans_titles = SQLloadTransTitles(record[TITLE_PUBID])
        printmultiple(trans_titles, "Transliterated Title", "trans_titles", "AddTransTitle", help)

	authors = SQLInterviewAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Interviewee", "interviewee_author1.", "AddInterviewee1", help)

	authors = SQLTitleAuthors(record[TITLE_PUBID])
        printmultiple(authors, "Interviewer", "interviewer_author1.", "AddInterviewer1", help)

	print "</tbody>"

        print '<tbody id="titleBody">'

        printCommonSection(record, help)

	print "<tr>"
	print "<td><b>Title Type</b></td>"
	print '<td><input name="title_ttype" value="INTERVIEW" READONLY class="titletype displayonly"></td>'
	print '</tr>'

        printtextarea('Note', 'title_note', help, SQLgetNotes(record[TITLE_NOTE]), 10)

        printtextarea('Note to Moderator', 'mod_note', help, '')

        print "</tbody>"
        print "</table>"


def displayError():
        PrintPreSearch("Title Editor")
        PrintNavBar("edit/edittitle.cgi", 0)
        print '<h3>Missing or non-existing title</h3>'
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
                title_id = int(sys.argv[1])
                title_data = SQLloadTitle(title_id)
                if not title_data:
                        raise
        except:
                displayError()

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Title Editor")
	PrintNavBar("edit/edittitle.cgi", title_id)

        printHelpBox('title', 'EditTitle')

        # Pass the title type to the form validation function so that it would know what fields exist in the form
	print "<form id='data' METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submittitle.cgi\" onsubmit=\"return validateTitleForm('%s')\" >" % (title_data[TITLE_TTYPE])

        # Combine the two series number fields into one for display purposes
        series_number = title_data[TITLE_SERIESNUM]
        if title_data[TITLE_SERIESNUM_2] is not None:
                series_number = '%s.%s' % (title_data[TITLE_SERIESNUM], title_data[TITLE_SERIESNUM_2])

	if title_data[TITLE_TTYPE] == 'INTERVIEW':
		printinterviewrecord(title_data, series_number)
	elif title_data[TITLE_TTYPE] == 'REVIEW':
		printreviewrecord(title_data, series_number)
	else:
		printtitlerecord(title_data, series_number)

	print '<p>'
	print '<hr>'
	print '<p>'
	print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % (title_id)
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'
	print '<hr>'
	print ISFDBLink("edit/deletetitle.cgi", title_id, "Delete record")

	PrintPostSearch(tableclose=False)
