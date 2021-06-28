#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2021   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from awardClass import *
from awardtypeClass import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from login import *
from library import *
from isfdblib_print import *


if __name__ == '__main__':

        # If this script was accessed via the Award Type Selector, there are no CGI parameters;
        # the title ID and the Award Type ID are in the posted form values instead
        if not SESSION.parameters:
		sys.stderr = sys.stdout
		form = cgi.FieldStorage()
		try:
			title_id = int(form['title_id'].value)
                        # If the passed in title ID is not 0, i.e. this is a title-based award, so load the associated title data
                        if title_id:
                                title = SQLloadTitle(title_id)
                                if not title:
                                        raise
		except:
                        SESSION.DisplayError('Missing or invalid Title ID') 

		try:
			award_type_id = int(form['award_type_id'].value)
                        awardType = award_type()
                        awardType.award_type_id = award_type_id
                        awardType.load()
                        if not awardType.award_type_name:
                                raise
                except:
                        SESSION.DisplayError('Missing or invalid Award Type ID')

        else:
                title_id = SESSION.Parameter(0, 'int')
                # If the passed in ID is not 0, i.e. this is a title-based award, load the associated title data
                if title_id:
                        title = SQLloadTitle(title_id)
                        if not title:
                                SESSION.DisplayError('Missing or invalid Title ID')

                awardType = award_type()
                awardType.award_type_id = SESSION.Parameter(1, 'int')
                awardType.load()
                if not awardType.award_type_name:
                        SESSION.DisplayError('Missing or invalid Award Type ID')

        if title_id:
                PrintPreSearch('Award Editor for a Title')
        else:
                PrintPreSearch('Award Editor')
        PrintNavBar('edit/addaward.cgi', title_id)

        help = HelpAward(awardType.award_type_poll)

	print '<div id="HelpBox">'
        print '<b>Help on adding an award: </b>'
        print '<a href="http://%s/index.php/Help:Screen:AddAward">Help:Screen:AddAward</a><p>' % (WIKILOC)
	print '</div>'

        if title_id:
		print '<h3>You are entering an award for Title record <a href="http:/%s/title.cgi?%s">%s</a></h3>' % (HTFAKE, title[TITLE_PUBID], title[TITLE_PUBID])

	else:
		print '<h3>This data entry form is for awards that are given to people (for instance, Best Artist)'
		print 'or works not eligible for inclusion in ISFDB (for instance, Best Dramatic Presentation).'
		print 'If you want to add an award to a title in ISFDB, go to that title\'s page and use the'
		print 'Add Award link found there.</h3>'
		print '<p>'

	print '<form id="data" method="POST" action="/cgi-bin/edit/submitnewaward.cgi">'
        print '<table border="0">'
        print '<tbody id="titleBody">'

        if title_id:
		printfield("Title", "award_title", help, title[TITLE_TITLE], 1)
		authors = SQLTitleAuthors(title_id)
                printmultiple(authors, "Author", "title_author", help, 1)

        else:
		printfield("Title", "award_title", help)
                printmultiple([], "Author", "title_author", help)

	printfield("Year", "award_year", help)

        # Award name is read-only because the list of categories depends on it. If we were to make it editable,
        # we would need to implement JavaScript-based logic to change categories based on the selected award type.
        printfield("Award Name", "award_type", help, awardType.award_type_name, 1)

	printAwardCategory("award_cat_id", "Category", awardType.award_type_id, '', help)

        printAwardLevel("Award Level", '0', awardType.award_type_poll, help)

        # Only allow entering IMDB information for non-title awards
        if not title_id:
        	printfield("IMDB Title", "award_movie", help)

        printtextarea('Note', 'award_note', help)

        printtextarea('Note to Moderator', 'mod_note', help)

	print '</tbody>'
	print '</table>'
	print '<p>'

	print '<input name="title_id" value="%d" type="HIDDEN">' % (title_id)
	print '<input name="award_type_id" value="%d" type="HIDDEN">' % (awardType.award_type_id)
	print '<input type="SUBMIT" value="Submit Award" tabindex="1">'
	print '</form>'

	PrintPostSearch(tableclose=False)
