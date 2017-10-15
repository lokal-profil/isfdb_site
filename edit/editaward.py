#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2017   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.22 $
#     Date: $Date: 2017/03/11 16:09:49 $


import cgi
import sys
from awardClass import *
from awardtypeClass import *
from isfdb import *
from library import *
from isfdblib import *
from isfdblib_help import *
from SQLparsing import *
from isfdblib_print import printtextarea, printfield, printAwardCategory, printAwardLevel, printtextarea, printHelpBox


if __name__ == '__main__':

	try:
                award_id = int(sys.argv[1])
                award = awards(db)
                award.load(int(award_id))
                if not award.award_id:
                        raise
                awardType = award_type()
                awardType.award_type_id = award.award_type_id
                awardType.load()
	except:
        	PrintPreSearch("Award Editor")
		PrintNavBar("edit/editaward.cgi", 0)
		print '<h3>Bad or non-existing award ID</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
        if award.title_id:
        	PrintPreSearch("Award Editor for a Title")
        else:
        	PrintPreSearch("Award Editor")
	PrintNavBar("edit/editaward.cgi", award_id)

        help = HelpAward(awardType.award_type_poll)

        printHelpBox('award', 'EditAward')

        # Print appropriate message depending on whether this is a title-based award
        if award.title_id:
		print '<h3>You are editing an award for Title record <a href="http:/%s/title.cgi?%s">%s</a></h3>' % (HTFAKE, award.title_id, award.title_id)
	else:
                print '<h3>You are editing an award not associated with an ISFDB title</h3>'
	print '<p>'

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitaward.cgi" onsubmit="return validateAwardForm()">'

	print '<table border="0">'
        print '<tbody id="titleBody">'

	printfield("Title", "award_title", help, award.award_title, award.title_id)

        counter = 1
        if award.award_authors:
        	for author in award.award_authors:
                        printfield('Author'+str(counter), 'title_author'+str(counter), help, author, award.title_id)
                        counter += 1
        else:
                printfield('Author1', 'title_author1', help, '', award.title_id)
                counter += 1

        # Only allow adding authors for non-title based awards
        if not award.title_id:
                print '<tr id="AddAuthor" next="%d">' % (counter)
                print '<td><input type="button" value="Add Author" onclick="addMetadataTitleAuthor()" tabindex="1"></td>'
                print '<td> </td>'
                print '</tr>'

	printfield("Year", "award_year", help, award.award_year)

        # Award name is read-only because the list of categories depends on it. If we were to make it editable,
        # we would need to implement JavaScript-based logic to change categories based on the selected award type.
        printfield("Award Name", "award_type", help, award.award_type_name, 1)

	printAwardCategory("award_cat_id", "Category", award.award_type_id, award.award_cat_id, help)

        printAwardLevel("Award Level", award.award_level, awardType.award_type_poll, help)

        # Only display the IMDB title field for non-title based awards
        if not award.title_id:
                printfield("IMDB Title", "award_movie", help, award.award_movie)

        printtextarea('Note', 'award_note', help, award.award_note)

        printtextarea('Note to Moderator', 'mod_note', help)

        print '</tbody>'
        print '</table>'

	print '<p>'
	print '<hr>'
	print '<p>'
	print '<input NAME="award_id" VALUE="%d" TYPE="HIDDEN">' % (award_id)
	print '<input name="award_type_id" value="%d" type="HIDDEN">' % (awardType.award_type_id)
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'
	print '<hr>'
	print '<a href="/cgi-bin/edit/deleteaward.cgi?%d">Delete this award</a>' % (award_id)

	PrintPostSearch(tableclose=False)
