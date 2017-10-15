#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2017   Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.67 $
#     Date: $Date: 2017/06/16 20:19:37 $


import cgi
import sys
import MySQLdb
from SQLparsing import *
from isfdb import *
from library import *
from isfdblib import *


def getPageNumber(title_id, pub_id):
	query = 'select pubc_page from pub_content where title_id=%d and pub_id=%d' % (int(title_id), int(pub_id))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	try:
		return record[0][0]
	except:
		return 0

def printtitletype(current_value, help):
	print '<tr>'
	printContentHeader('Title Type', help)
        print '<td><select tabindex="1" name="title_ttype">'
	for ttype in ['ANTHOLOGY','CHAPBOOK','COLLECTION','COVERART',
                      'EDITOR', 'ESSAY', 'INTERIORART', 'NONFICTION',
                      'NOVEL','OMNIBUS','POEM','SERIAL','SHORTFICTION']:
		if current_value == ttype:
        		print '<option selected="selected">%s</option>' % ttype
		else:
        		print '<option>%s</option>' % ttype
		
        print '</select></td></tr>'

def printlength(current_value, help):
	print '<tr>'
	printContentHeader('Length', help)
        print '<td><select tabindex="1" name="title_storylen">'
	for storylen in STORYLEN_CODES:
		if current_value == storylen:
        		print '<option selected>%s</option>' % storylen
		else:
        		print '<option>%s</option>' % storylen
        print '</select></td>'
        print '</tr>'

def printlanguage(current_language_code='', field='language', label='Language', help = None):
	(myID, username, usertoken) = GetUserData()
	# Get the currently defined preferences for the logged-in user
	preferences = SQLLoadUserPreferences(myID)
	# Get this user's default language code and name
        default_language_code = preferences[USER_DEFAULT_LANGUAGE]
        default_language_name = LANGUAGES[default_language_code]

        current_language_name = ''
        # If we are basing the language data on an existing record, get that record's language code and name
        if current_language_code:
                current_language_name = LANGUAGES[current_language_code]

	print '<tr>'
	printfieldlabel(label, help)

        print '<td><select tabindex="1" class="metainputselect" name="%s">' %(field)

        # Iterate over an alphabetized list of language names (excluding 'Unknown' in the 0th position)
        # and display them in a drop-down list
        for language_name in sorted(LANGUAGES[1:]):
                # If the current record's language is defined and we are processing it, then select it
		if current_language_name and language_name == current_language_name:
        		print '<option selected="selected">%s</option>' % (language_name)
        	# If the current title has no language code and this language is the user's default language, then select it
		elif not current_language_name and language_name == default_language_name:
        		print '<option selected="selected">%s</option>' % (language_name)
                # Otherwise this language is displayed, but is not "selected"
		else:
        		print '<option>%s</option>' % (language_name)

        print '</select>'
        print '</td>'
        print '</tr>'

def printbinding(field='pub_ptype', label='Binding', help = None, value='unknown'):
        if not value:
                value = 'unknown'
	print '<tr>'
	printfieldlabel(label, help)

        print '<td><select tabindex="1" name="%s">' %(field)

        # Iterate over the list of recognized bindings and display them in a drop-down list
        for binding in BINDINGS:
		if binding.lower() == value.lower():
        		print '<option selected="selected">%s</option>' % (binding)
		else:
        		print '<option>%s</option>' % (binding)

        print '</select>'
        print '</td>'
        print '</tr>'

def printExternalIDs(external_ids = None, label = 'External ID', field = 'external_id', help = None, readonly = 0):
        if not external_ids:
                external_ids = {}
        if not help:
                help = {}
        identifier_types = SQLLoadIdentifierTypes()

        print '<tr>'
        printfieldlabel('%ss' % label, help)
        print '<td>&nbsp;</td>'
        print '</tr>'

        counter = 1
        if readonly:
                for id_type in sorted(external_ids.keys()):
                        for id_value in external_ids[id_type]:
                                type_id = external_ids[id_type][id_value][0]
                                print '<tr>'
                                print '<td>'
                                print '<input type="hidden" name="%s_type.%d" VALUE="%d">' % (field, counter, type_id)
                                print '<b>%s</b>' % id_type
                                print '</td>'
                                print '<td>'
                                print '<INPUT name="%s.%d" id="%s.%d" READONLY class="titlemultiple metainput" value="%s">' % (field, counter, field, counter, id_value)
                                print '</td>'
                                print '</tr>'
                                counter += 1
                return

        # Create a list of ID types to display as mouse-over help
        type_list = 'The following external identifier types are currently supported:&#13;'
        for identifier_type in sorted(identifier_types, key = identifier_types.get):
                type_name = identifier_types[identifier_type][0]
                type_full_name = identifier_types[identifier_type][1]
                type_list += ' %s: %s&#13;' % (type_name, type_full_name)

        for id_type in sorted(external_ids.keys()):
                for id_value in external_ids[id_type]:
                        type_id = external_ids[id_type][id_value][0]
                        print '<tr>'
                        print '<td class="hint" title="%s">' % type_list
                        print '<select tabindex="1" name="%s_type.%d">' % (field, counter)
                        for identifier_type in sorted(identifier_types, key = identifier_types.get):
                                if identifier_type == type_id:
                                        selected = ' selected="selected"'
                                else:
                                        selected = ''
                                print '<option%s VALUE="%d">%s</option>' % (selected, identifier_type, identifier_types[identifier_type][0])
                        print '</select>'
                        print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help">' % (HTMLLOC)
                        print '</td>'
                        print '<td>'
                        print '<INPUT tabindex="1" name="%s.%d" id="%s.%d" class="metainput" value="%s">' % (field, counter, field, counter, id_value)
                        print '</td>'
                        print '</tr>'
                        counter += 1

        print '<tr>'
        print '<td class="hint" title="%s">' % type_list
        print '<select tabindex="1" name="%s_type.%d">' % (field, counter)
        # Iterate over the list of recognized external IDs and display them in a drop-down list
        for identifier_type in sorted(identifier_types, key = identifier_types.get):
                print '<option VALUE="%d">%s</option>' % (identifier_type, identifier_types[identifier_type][0])
        print '</select>'
        print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help">' % (HTMLLOC)
        print '</td>'
        print '<td>'
        print '<INPUT tabindex="1" name="%s.%d" id="%s.%d" class="metainput">' % (field, counter, field, counter)
        print '</td>'
        print '</tr>'
        onclick_parameters = "'%s', '%s'" % ('external_id', 'pubBody')
        printaddbutton('AddExternalID', counter, label, 'addNewExternalID', onclick_parameters, help)

###################################################################
# This function outputs an existing title record in table format
###################################################################
def printtitlerecord(record, index, pub_id, help = None, reuse_page_numbers = 1):

        if not help:
                help = {}

        args = ' READONLY class="%s titlemultiple"'

        print "<tr><td>"
        print '<input name="title_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])
        page = getPageNumber(record[TITLE_PUBID], pub_id)
	if page and reuse_page_numbers:
		print '<input name="title_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page))
	else:
		print '<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index)

        print '<td><input name="title_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="title_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput")
        print '<td><input name="title_ttype%d" value="%s"%s></td>' % (index, record[TITLE_TTYPE], args % "contenttypeinput")

	###################################
	# STORYLEN
	###################################
        length = ''
        for storylen in STORYLEN_CODES:
                if record and record[TITLE_STORYLEN] == storylen:
                        length = storylen
                        break
        print '<td><input name="title_storylen%d" value="%s"%s></td>' % (index, length, args % "contentleninput")
        print '</tr>'

        authors = SQLTitleAuthors(record[TITLE_PUBID])
        counter = 1
        if len(authors):
                for author in authors:
                        print '<tr>'
                        print '<td><b>Author%d:</b></td>' % (counter)
                        print '<td><input name="title_author%d.%d" value="%s"%s></td>' % (index, counter, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

	printSpacer(5)

def printblanktitlerecord(index, help = None, pub_type = 'NOVEL'):
        if not help:
                help = {}
        args = ' READONLY class="%s titlemultiple"'

        # Use the publication type to determine the default title type for
        # contents titles
	if pub_type == 'OMNIBUS':
                default_title_type = 'NOVEL'
	elif pub_type == 'NONFICTION':
                default_title_type = 'ESSAY'
	else:
                default_title_type = 'SHORTFICTION'

        print '<tr>'
        print '<td><input name="title_id%d" type="HIDDEN">' % (index)
        print '<input name="title_page%d" tabindex="1" class="contentpageinput"></td>' % (index)
        print '<td><input name="title_title%d" tabindex="1" class="contentinput"></td>' % (index)
        print '<td><input name="title_date%d" tabindex="1" class="contentyearinput"></td>' % (index)

        print '<td><select tabindex="1" name="title_ttype%d" class="contenttypeinput">' % (index)
        print '<option selected="selected">%s</option>' % default_title_type
        for ttype in ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'EDITOR', 'ESSAY', 'INTERIORART',
                      'NONFICTION', 'NOVEL', 'OMNIBUS', 'POEM', 'SERIAL', 'SHORTFICTION'):
                if ttype != default_title_type:
                        print '<option>%s</option>' % ttype
        print '</select></td>'

        print '<td><select tabindex="1" name="title_storylen%d" class="contentleninput">' % (index)
        for storylen in STORYLEN_CODES:
                print '<option>%s</option>' % storylen
        print '</select></td>'
        print '</tr>'

        counter = 1
        print '<tr>'
        printContentHeader('Author1:', help)
        print '<td><input tabindex="1" name="title_author%d.%d" class="contentinput"></td>' % (index, counter)
        print '</tr>'
        counter +=1

        printAddContentAuthor('Author', help, index, counter)
	printSpacer(5)

def printfullcoverart(cover, index, help = None, readonly = 0):
        if not help:
                help = {}

        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'

        print '<tr>'
        print '<td><input name="cover_id%d" value="%s" type="HIDDEN"></td>' % (index, cover[TITLE_PUBID])
        print '<td><input name="cover_title%d" value="%s"%s></td>' % (index, escape_string(cover[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="cover_date%d" value="%s"%s></td>' % (index, cover[TITLE_YEAR], args % "contentyearinput")
        print '</tr>'
        artists = SQLTitleAuthors(cover[TITLE_PUBID])
        counter = 1
        if len(artists):
                for artist in artists:
                        print '<tr>'
                        printContentHeader('Artist%d:'% counter, help)
                        print '<td><input name="cover_artist%d.%d" value="%s"%s></td>' % (index, counter, escape_string(artist), args % "contentinput")
                        print '</tr>'
                        counter += 1
        if not readonly:
                printAddContentAuthor('Artist', help, index, counter)
        printSpacer(3)

def printbriefblankcoverart(index, help = None):
        if not help:
                help = {}
        counter = 1
        print '<tr>'
        print '<td>'
        print '<input name="cover_id%d" value="0" type="HIDDEN">' % (index)
        print '<input name="cover_title%d" type="HIDDEN">' % (index)
        print '<input name="cover_date%d" type="HIDDEN">' % (index)
        print '</td>'
        print '</tr>'
        print '<tr>'
        printContentHeader('Artist1:', help)
        print '<td><input tabindex="1" name="cover_artist%d.%d" class="contentinput"></td>' % (index, counter)
        print '</tr>'
        counter +=1
        printAddContentAuthor('Artist', help, index, counter)
	printSpacer(2)

def printfullblankcoverart(index, help = None):
        if not help:
                help = {}
        counter = 1
        print '<tr>'
        print '<td>'
        print '<input name="cover_id%d" value="0" type="HIDDEN">' % (index)
        print '</td>'
        print '<td><input name="cover_title%d" class="contentinput"></td>' % index
        print '<td><input name="cover_date%d" class="contentyearinput"></td>' % index
        print '</tr>'
        print '<tr>'
        printContentHeader('Artist1:', help)
        print '<td><input tabindex="1" name="cover_artist%d.%d" class="contentinput"></td>' % (index, counter)
        print '</tr>'
        counter +=1
        printAddContentAuthor('Artist', help, index, counter)
	printSpacer(3)


def printreviewrecord(record, index, pub_id, help = None, reuse_page_numbers = 1):
        if not help:
                help = {}
        args = ' READONLY class="%s titlemultiple"'

        print '<tr><td>'
        print '<input name="review_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])
        page = getPageNumber(record[TITLE_PUBID], pub_id)
	if page and reuse_page_numbers:
		print '<input name="review_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page))
	else:
		print '<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % index

        print '<td><input name="review_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="review_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput")
        print '</tr>'

	counter = 1
        authors = SQLReviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        print '<td><b>Author%d:</b></td>' % counter
                        print '<td><input name="review_author%d.%d" value="%s"%s></td>' % (index, counter, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        print '<td><b>Reviewer%d:</b></td>' % (counter)
                        print '<td><input name="review_reviewer%d.%d" value="%s"%s></td>' % (index, counter, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

	printSpacer(3)

def printblankreviewrecord(index, help = None):
        if not help:
                help = {}

        print '<tr>'
        print '<td><input name="review_id%d" type="HIDDEN">' % int(index)
        print '<input name="review_page%d" tabindex="1" class="contentpageinput"></td>' % int(index)
        print '<td><input name="review_title%d" tabindex="1" class="contentinput"></td>' % int(index)
        print '<td><input name="review_date%d" tabindex="1" class="contentyearinput"></td>' % int(index)
        print '</tr>'

	counter = 1
        print '<tr>'
        printContentHeader('Author1:', help)
        print '<td><input name="review_author%d.%d" tabindex="1" class="contentinput"></td>' % (int(index), int(counter))
        print '</tr>'
        counter += 1
        printAddContentAuthor('Reviewee', help, index, counter)

        counter = 1
        print '<tr>'
        printContentHeader('Reviewer1:', help)
        print '<td><input name="review_reviewer%d.%d" tabindex="1" class="contentinput"></td>' % (int(index), int(counter))
        print '</tr>'
        counter += 1
        printAddSecondaryAuthor('Reviewer', help, index, counter)

	printSpacer(3)

def printinterviewrecord(record, index, pub_id, help = None, reuse_page_numbers = 1):
        if not help:
                help = {}

        args = ' READONLY class="%s titlemultiple"'
        print '<tr><td>'
        print '<input name="interview_id%d" value="%s" type="HIDDEN">' % (index, record[TITLE_PUBID])

        page = getPageNumber(record[TITLE_PUBID], pub_id)
	if page and reuse_page_numbers:
		print '<input name="interview_page%d" tabindex="1" value="%s" class="contentpageinput"></td>' % (index, escape_string(page))
	else:
		print '<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % index

        print '<td><input name="interview_title%d" value="%s"%s></td>' % (index, escape_string(record[TITLE_TITLE]), args % "contentinput")
        print '<td><input name="interview_date%d" value="%s"%s></td>' % (index, record[TITLE_YEAR], args % "contentyearinput")
        print '</tr>'

        counter = 1
        authors = SQLInterviewAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        print '<td><b>Interviewee%d:</b></td>' % (counter)
                        print '<td><input name="interviewee_author%d.%d" value="%s"%s></td>' % (index, counter, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

        counter = 1
        authors = SQLTitleAuthors(record[TITLE_PUBID])
        if len(authors):
                for author in authors:
                        print '<tr>'
                        print '<td><b>Interviewer%d:</b></td>' % (counter)
                        print '<td><input name="interviewer_author%d.%d" value="%s"%s></td>' % (index, counter, escape_string(author), args % "contentinput")
                        print '</tr>'
                        counter += 1

	printSpacer(3)

def printblankinterviewrecord(index, help = None):
        if not help:
                help = {}

        print '<tr>'
        print '<td><input name="interview_id%d" type="HIDDEN">' % int(index)
        print '<input name="interview_page%d" tabindex="1" class="contentpageinput"></td>' % int(index)
        print '<td><input name="interview_title%d" tabindex="1" class="contentinput"></td>' % int(index)
        print '<td><input name="interview_date%d" tabindex="1" class="contentyearinput"></td>' % int(index)
        print '</tr>'

        counter = 1
        print '<tr>'
        printContentHeader('Interviewee1:', help)
        print '<td><input name="interviewee_author%d.%d" tabindex="1" class="contentinput"></td>' % (int(index), int(counter))
        print '</tr>'
        counter += 1
        printAddContentAuthor('Interviewee', help, index, counter)

        counter = 1
        print '<tr>'
        printContentHeader('Interviewer1:', help)
        print '<td><input name="interviewer_author%d.%d" tabindex="1" class="contentinput"></td>' % (int(index), int(counter))
        print '</tr>'
        counter += 1
        printAddSecondaryAuthor('Interviewer', help, index, counter)

	printSpacer(3)

def printtextarea(label, fieldname, help, notes = '', rows = 4, readonly = 0):
        print '<tr>'
        
        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'

        printfieldlabel(label, help)
        print '<td>'
        print '<textarea tabindex="1" name="%s" rows="%s"%s cols="60">' % (fieldname, rows, args % "metainput")
        if notes:
                print ISFDBText(notes, True)
        print '</textarea>'
        print '</td>'
        print '</tr>'

def printsource(help):
	print '<tr>'
	if help.get("Source"):
                print '<td class="hint" title="%s"><b>Source of the data: </b>' % (help['Source'][0])
                print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></td>' % (HTMLLOC)
        else:
                print '<td><b>Source of the data: </b></td>'
	print '<td>'
	print '<input type="radio" name="Source" value="Primary">I own this publication (will be auto-verified as Primary)<br>'
	print '<input type="radio" name="Source" value="Transient">I am working from this publication but will not have it permanently (will be auto-verified as Transient)<br>'
	print '<input type="radio" name="Source" value="PublisherWebsite">Publisher\'s website<br>'
	print '<input type="radio" name="Source" value="AuthorWebsite">Author\'s website<br>'
	print '<input type="radio" tabindex="1" name="Source" value="Other" CHECKED>Other website, later printing/edition or another source (please explain in Publication Note)'
	print '</td>'
	print '</tr>'

def printAddArtist(help, next = '2'):
	print '<tr id="AddArtist" next="%s">' % (str(next))
       	if help.get("Add Artist"):
                print '<td class="hint" title="%s"><input type="button" value="Add Artist" tabindex="1" onclick="addPubArtist()">' % (help['Add Artist'][0])
                print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></td>' % (HTMLLOC)
        else:
                print '<td><input type="button" value="Add Artist" tabindex="1" onclick="addPubArtist()"></td>'
	print '<td>&nbsp;</td>'
	print '</tr>'

def printAddAuthor(author_or_editor, help, next = '2', table_name = 'pubBody'):
	print '<tr id="AddAuthor" next="%s">' % (str(next))
	label = 'Add ' + author_or_editor
       	if help.get(label):
                print """<td class="hint" title="%s"><input type="button" value="Add %s" tabindex="1"
                        onclick="addPubAuthor('%s', '%s')">""" % (help[label][0], author_or_editor, author_or_editor, table_name)
                print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></td>' % (HTMLLOC)
        else:
                print """<td><input type="button" value="Add %s" tabindex="1"
                        onclick="addPubAuthor('%s', '%s')"></td>""" % (author_or_editor, author_or_editor, table_name)
	print '<td>&nbsp;</td>'
	print '</tr>'

def printAddContentAuthor(type, help, index, next = '2'):
	print '<tr id="Add%s%d" next="%d">' % (type, int(index), int(next))
	print '<td>&nbsp;</td>'
	if type == 'Author':
                onclick = 'addContentTitleAuthor'
                label = 'Author'
        elif type == 'Reviewee':
                onclick = 'addReviewee'
                label = 'Author'
        elif type == 'Interviewee':
                onclick = 'addInterviewee'
                label = 'Interviewee'
        elif type == 'Artist':
                onclick = 'addArtist'
                label = 'Artist'

        # Only display the help pop-up for the first occurence of this button
        if help.get(('Add '+label)) and int(index) < 2:
        	print '<td class="hint" title="%s"><input type="button" tabindex="1" value="Add %s" onclick="%s(%d)">' % (help[('Add '+label)][0], label, onclick, int(index))
        	print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></td>' % (HTMLLOC)
        else:
                print '<td><input type="button" tabindex="1" value="Add %s" onclick="%s(%d)"></td>' % (label, onclick, int(index))
	print '</tr>'

def printAddSecondaryAuthor(type, help, index, next = '2'):
	print '<tr id="Add%s%d" next="%d">' % (type, int(index), int(next))
	print '<td>&nbsp;</td>'
	if help.get(('Add '+type)) and int(index) < 2:
        	print '<td class="hint" title="%s"><input type="button" tabindex="1" value="Add %s" onclick="add%s(%d)">' % (help[('Add '+type)][0], type, type, int(index))
        	print '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></td>' % (HTMLLOC)
        else:
                print '<td><input type="button" tabindex="1" value="Add %s" onclick="add%s(%d)"></td>' % (type, type, int(index))
	print '</tr>'


def printContentHeader(label, help, index = 1):
        # The 4th parameter is '' in order to avoid displaying a colon
        printfieldlabel(label, help, index, '')

def printNewTitleButton(index):
        print '<tr id="AddTitle" next="%d">' % int(index)
        print '<td>&nbsp;</td>'
        print '<td><input type="button" value="Add Title" onclick="addNewTitle()" tabindex="1"></td>' 
        print '</tr>'

def printNewBriefCoverButton(index):
        printNewRecordButton('Cover', index, 'addNewBriefCover')

def printNewFullCoverButton(index):
        printNewRecordButton('Cover', index, 'addNewFullCover')

def printNewReviewButton(index):
        print '<tr id="AddReview" next="%d">' % int(index)
        print '<td>&nbsp;</td>'
        print '<td><input type="button" value="Add Review" onclick="addNewReview()" tabindex="1"></td>' 
        print '</tr>'

def printNewInterviewButton(index):
        print '<tr id="AddInterview" next="%d">' % int(index)
        print '<td>&nbsp;</td>'
        print '<td><input type="button" value="Add Interview" onclick="addNewInterview()" tabindex="1"></td>'
        print '</tr>'

def printNewRecordButton(record_type, index, onclick = None):
        if not onclick:
                onclick = 'addNew%s' % record_type
        print '<tr id="Add%s" next="%d">' % (record_type, int(index))
        print '<td>&nbsp;</td>'
        print '<td><input type="button" value="Add %s" onclick="%s()" tabindex="1"></td>' % (record_type, onclick)
        print '</tr>'

def printfieldlabel(label, help, index = 1, colon = ':'):
        # Only display the help pop-up for the first occurrence of repeating fields
       	if help and help.get(label) and (int(index) < 2):
                text = escape_string(help[label][0])
               	print '<td class="hint" title="%s"><b>%s%s </b>' % (text, label, colon)
                image = '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help">' % HTMLLOC
                if help[label][1]:
                        print '<a tabindex="0" href="%s">%s</a>' % (help[label][1], image)
                else:
                        print image

                print '</td>'
        else:
                print '<td><b>%s%s</b></td>' % (label, colon)

def printfield(label, fieldname, help = None, value = '', readonly = 0):
        if readonly:
                args = ' READONLY class="%s titlemultiple"'
        else:
                args = ' class="%s"'
	print '<tr>'

	printfieldlabel(label, help)

        if value is not None:
               	print '<td><INPUT tabindex="1" name="%s" id="%s" value="%s"%s></td>' % (fieldname, fieldname, escape_string(value), args % "metainput")
        else:
               	print '<td><INPUT tabindex="1" name="%s" id="%s"%s></td>' % (fieldname, fieldname, args % "metainput")
	print '</tr>'

def printAwardName(field, label, help):
	print '<tr>'
	printfieldlabel(label, help)
        print '<td><select name="%s" tabindex="1">' % (field)
        award_types = SQLListAwardTypes()
        for award_type in award_types:
                print '<option value="%d">%s</option>' % (int(award_type[AWARD_TYPE_ID]), award_type[AWARD_TYPE_NAME])
        print '</select></td>'
        print '</tr>'

def printAwardCategory(field, label, award_type_id, default_award_cat_id, help):
	print '<tr>'
	printfieldlabel(label, help)
        print '<td><select name="%s" tabindex="1">' % (field)
        award_cats = SQLGetAwardCategories(award_type_id)
        for award_cat in award_cats:
                if int(award_cat[AWARD_CAT_ID]) == default_award_cat_id:
                        print '<option selected="selected" value="%d">%s</option>' % (award_cat[AWARD_CAT_ID], award_cat[AWARD_CAT_NAME])
                else:
                        print '<option value="%d">%s</option>' % (award_cat[AWARD_CAT_ID], award_cat[AWARD_CAT_NAME])
        print '</select></td>'
        print '</tr>'

def printAwardLevel(label, value, poll, help):
	print '<tr>'
	printfieldlabel(label, help)
	print '<td>'
	# For non-poll awards, display Win/Nomination radio buttons
	if poll == 'No':
                if value == '1':
                        print '<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" CHECKED tabindex="1">Win'
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" tabindex="1">Nomination'
                elif int(value) < 71:
                        print '<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" tabindex="1">Win'
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" CHECKED tabindex="1">Nomination'
                else:
                        print '<INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_WIN" VALUE="WIN" tabindex="1">Win'
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_NOM" VALUE="NOM" tabindex="1">Nomination'
        # For poll awards, display the level radio button and the "Poll place" field
        else:
                # '0' is the value for new poll awards, so the "Poll place" field should be blank
                if value == '0':
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" CHECKED tabindex="1">Poll place:'
                        print '<INPUT NAME="award_level" SIZE=5 VALUE="" tabindex="1">'
                elif int(value) < 71:
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" CHECKED tabindex="1">Poll place:'
                        print '<INPUT NAME="award_level" SIZE=5 VALUE="%s" tabindex="1">' % value
                else:
                        print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_LEVEL" VALUE="LEVEL" tabindex="1">Poll place:'
                        print '<INPUT NAME="award_level" SIZE=5 VALUE="" tabindex="1">'
        # Special awards section
        if int(value)>70:
                print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_SPECIAL" VALUE="SPECIAL" CHECKED tabindex="1">Special:'
        else:
                print '<br><INPUT TYPE="radio" NAME="LEVEL" ID="LEVEL_SPECIAL" VALUE="SPECIAL" tabindex="1">Special:'
        special_awards = SpecialAwards()
        print '<select NAME="award_special" tabindex="1">'
	for special_level in sorted(special_awards.keys()):
		if special_level == value:
        		print '<option selected="selected" value="%s">%s</option>' % (special_level, special_awards[special_level])
        	else:
                        print '<option value="%s">%s</option>' % (special_level, special_awards[special_level])
	print '</select></td>'
	print '</tr>'

def printSpacer(rows):
        print '<tr class="titleeditspacer"><td colspan="%d"> </td></tr>' % rows

def printmultiple(values, label, field_name, row_id, onclick_function, help, onclick_parameters = '', readonly = 0):
	counter = 1
        for value in values:
                printfield(("%s %d" % (label, counter)), ("%s%d" % (field_name, counter)), help, value, readonly)
                counter += 1

        if not readonly:
                printfield(("%s %d" % (label, counter)), ("%s%d" % (field_name, counter)), help, '', readonly)
                printaddbutton(row_id, counter, label, onclick_function, onclick_parameters, help)

def printaddbutton(row_id, counter, label, onclick_function, onclick_parameters, help = None):
        if not help:
                help = {}
        print '<tr id="%s" next="%d">' % (row_id, counter+1)
        mouse_over1 = ''
        mouse_over2 = ''
       	if help.get("Add %s" % label):
                mouse_over1 = ' class="hint" title="%s"' % help['Add %s' % label][0]
                mouse_over2 = '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help">' % HTMLLOC
        print '<td%s><input type="button" value="Add %s" tabindex="1" onclick="%s(%s)">%s</td>' % (mouse_over1, label,
                                                                                                   onclick_function, onclick_parameters, mouse_over2)
        print '<td> </td>'
        print '</tr>'

def printWebPages(webpages, web_page_type, help, bodyname = 'tagBody'):
        parameters = "'%s', '%s'" % (web_page_type, bodyname)
        printmultiple(webpages, "Web Page", "%s_webpages" % web_page_type,
                      "AddWebPage", "addNewWebPage", help, parameters)

def printHelpBox(type, helplink):
	print '<div id="HelpBox">'
	print '<a href="http://%s/index.php/Help:Screen:%s">Help on editing %s records</a><br>' % (WIKILOC, helplink, type)
	print '<a href="http://%s/index.php/Help:Using_Templates_and_HTML_in_Note_Fields">List of supported templates and HTML tags in notes</a><p>' % WIKILOC
	print '</div>'

def printISBN(help, isbn):
        from isbn import convertISBN
	if isbn:
                compact = string.replace(isbn, '-', '')
                compact = string.replace(compact, ' ', '')
                compactlen = len(compact)

                pseudo = pseudoISBN(isbn)
                invalid = validISBN(isbn) ^ 1
                if compactlen == 10:
                        if invalid and pseudo:
                                printfield("ISBN / Catalog #", "pub_isbn", help, isbn)
                        elif invalid:
                                printfield("ISBN / Catalog #", "pub_isbn", help, isbn)
                        else:
                                printfield("ISBN / Catalog #", "pub_isbn", help, convertISBN(compact))
                elif compactlen == 13:
                        if invalid and pseudo:
                                printfield("ISBN / Catalog #", "pub_isbn", help, isbn)
                        elif invalid:
                                printfield("ISBN / Catalog #", "pub_isbn", help, isbn)
                        else:
                                printfield("ISBN / Catalog #", "pub_isbn", help, convertISBN(compact))
                else:
                        printfield("ISBN / Catalog #", "pub_isbn", help, isbn)
	else:
		printfield("ISBN / Catalog #", "pub_isbn", help)

        
def printdropdown(label, fieldname, values, help):
        print '<tr>'
        printfieldlabel(label, help)
        print '<td>'
	print '<select name="%s" tabindex="1">' % fieldname
	for value in values:
                if values[value]:
                        print '<option selected="selected">%s</option>' % value
                else:
                        print '<option>%s</option>' % value
        print '</select>'
        print '</td>'
        print '</tr>'

def printcheckbox(label, fieldname, current_value, disabled, help):
        # Displays a checkbox. If "current_value" is "Yes", then it will be checked
        print '<tr>'
        printfieldlabel(label, help)
        print '<td>'
        checked = ''
        if current_value == 'Yes':
                checked = 'checked'
        if disabled == 'disabled':
                disabled = 'disabled readonly'
        print '<input type="checkbox" name="%s" value="on" %s %s>' % (fieldname, disabled, checked)
        print '</td>'
        print '</tr>'

def printTitleAuthors(record, help):
	authors = SQLTitleAuthors(record[TITLE_PUBID])
        counter = 1
        if len(authors):
                for author in authors:
                        printfield('Author%s' % (counter), 'title_author%s' % (counter), help, author)
                        counter += 1
        else:
                printfield('Author%s' % (counter), 'title_author%s' % (counter), help, '')
                counter += 1

        print '<tr id="AddAuthor" next="%d">' % counter
        print '<td><input type="button" value="Add Author" onclick="addMetadataTitleAuthor()"></td>'
        print '<td> </td>'
        print '</tr>'
