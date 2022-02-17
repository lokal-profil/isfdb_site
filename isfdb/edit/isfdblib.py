#
#     (C) COPYRIGHT 2004-2021 Al von Ruff, Bill Longley, Kevin Pulliam (kevin.pulliam@gmail.com), Ahasuerus, Jesse Weinstein <jesse@wefu.org>, Uzume and Dirk Stoecker
#     ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import string
import sys
from isfdb import *
from login import *
from library import *
from navbar import *
from SQLparsing import *


def displayError(message, title = '', cgi_script = '', record_id = 0):
        if title:
                PrintPreSearch(title)
        if cgi_script != '':
                if cgi_script == 0:
                        PrintNavBar(0, 0)
                else:
                        PrintNavBar("edit/%s.cgi" % cgi_script, record_id)
        print '<div id="WarningBox">'
        print "<h3>Error: %s.</h3>" % message
        print '</div>'
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)

def XMLunescape2(input):
	retval = string.replace(str(input), "&rsquo;", "'")
	retval = string.replace(retval, "&quot;", '"')
	retval = string.strip(retval)
	retval = string.rstrip(retval)
	return retval

def escape_string(input):
	retval = string.replace(str(input), "'", "&rsquo;")
	retval = string.replace(retval, '"', "&quot;")
	retval = string.replace(retval, '  ', ' ')
	retval = string.replace(retval, "<", "&lt;")
	retval = string.replace(retval, ">", "&gt;")
	retval = string.replace(retval, "\\r\\n", "")
	return retval

def escape_quotes(input):
	if input:
		return string.strip(repr(input+'"')[1:-2])
	else:
		return ''

def escape_spaces(input):
	return string.replace(input, ' ', '%20')

def unescape_spaces(input):
	return string.replace(input, '%20', ' ')


##################################################################
# Create an SQL search query substring
##################################################################

Query_DT_List = ['author_birthdate', 'author_deathdate']
Query_EQ_List = ['pub_tag', 'pub_ptype', 'pub', 'pubs', 'ttype']
Query_LL_List = ['pub_price', 'pub_pages']
Query_RL_List = ['pub_title', 'pub_author', 'pub_year', 'pub_publisher', 'pub_isbn', 
		'pub_coverart', 'pub_bcoverart', 'author_legalname', 
		'author_birthplace', 'author_pseudos', 'title_series', 'title_superseries',
		'author_canonical', 'title_title']

def makequery(entry, use):
	if use in Query_DT_List:
                return "%s >= '%s-00-00' and %s < '%s-00-00'" % (use, entry[0:4], use, int(entry[0:4])+1)
	elif use in Query_EQ_List:
		return use+" = '"+entry+"'"
	elif use in Query_LL_List:
		return use+" like '%"+entry+"'"
	elif use in Query_RL_List:
		return use+" like '%"+entry+"%'"
	else:
		print "BAD QUERY USE:", use
		return ''


##################################################################
# These routines start and end the HTML page
##################################################################
def PrintPreSearch(title):
        PrintHTMLHeaders(title)

        print '<script type="text/javascript" src="%s://%s/isfdb_main.js"></script>' % (PROTOCOL, HTMLLOC)
        # Include the JavaScript file with the general purpose JS functions that support editing
        print '<script type="text/javascript" src="%s://%s/edit_js.js"></script>' % (PROTOCOL, HTMLLOC)

	if title in ('Publication Editor', 'Add Publication', 'New Novel', 'New Magazine',
                     'New Anthology', 'New Collection', 'New Omnibus', 'New Nonfiction',
                     'New Fanzine', 'New Chapbook', 'Clone Publication', 'Import/Export Contents',
                     'Delete Publication'):
        	JSscript('edit_pub')
        	JSscript('edit_title')
	elif title in ('Title Editor', 'Make Variant Title', 'Add Variant Title'):
        	JSscript('edit_title')
	elif title == 'Author Editor':
        	JSscript('edit_author')
	elif title == 'Award Editor':
        	JSscript('edit_award')
        	JSscript('edit_author')
        	JSscript('edit_title')
        elif ('New Award Category for' in title) or title in ('Award Type Editor',
                                                            'Award Editor for a Title',
                                                            'Add New Award Type',
                                                            'Award Category Editor'):
        	JSscript('edit_award')
	elif title in ('Publisher Editor', 'Publication Series Editor', 'Series Editor'):
        	JSscript('edit_other')

        print '</div>'
        # The "<noscript>" part will only be executed if Javascript is not enabled on the browser side
        print '<noscript><h1>Your browser does not support JavaScript. Javascript is required to edit ISFDB.'
        print '%s to return to browsing ISFDB.</h1></noscript>' % ISFDBLink('index.cgi', '', 'Click here')

def JSscript(script_name):
        print '<script type="text/javascript" src="%s://%s/%s.js"></script>' % (PROTOCOL, HTMLLOC, script_name)

def getSubmitter():
        (userid, username, usertoken) = GetUserData()
	return username

##################################################
#
#	Function appears in three different locations
#	See /mod/isfdblib.py for Moderator PrintUserInfo function
#	see /biblio/common.py for Regular PrintUserInfo function
#
##################################################
def PrintUserInfo():
	(userid, username, usertoken) = GetUserData()
	if username:
                PrintLoggedIn(userid, username)
	else:
                PrintNotLoggedIn(0,0)
	return username

#######################################################
#
#	Function appears in three different locations
#	Edit NavBar function.
#	See /mod/isfdblib.py for Moderator NavBar function
#	see /biblio/common.py for Regular NavBar function
#
#######################################################
def PrintNavBar(executable, arg):
	print '<div id="nav">'

	#Print the search box from module navbar
	PrintSearchBox('')

	username = PrintUserInfo()

        PrintOtherPages('Moderator')
	print '</div>'
	
	print '<div id="main2">'
	dbStatus = SQLgetDatabaseStatus()
        if dbStatus == 0:
                print "<h3>The ISFDB database is currently offline. Please check back in a few minutes.</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	onlineVersion = SQLgetSchemaVersion()
        if onlineVersion != SCHEMA_VER:
                print "<h3>Warning: database schema mismatch (%s vs %s)</h3>" % (onlineVersion, SCHEMA_VER)
	if username == 0:
		print '<h2>Login required to edit</h2>'
		print 'You have to %s to edit data.' % ISFDBLink('dologin.cgi', '%s+%s' % (executable, arg), 'login')
		PrintPostSearch(0, 0, 0, 0, 0, 0)
		sys.exit(0)
	editStatus = SQLgetEditingStatus()
	if editStatus == 0:
		print '<h2>Editing facilities are currently offline</h2>'
		PrintPostSearch(0, 0, 0, 0, 0, 0)
		sys.exit(0)
	elif editStatus == 2:
		(userid, username, usertoken) = GetUserData()
		if SQLisUserModerator(userid) == 0:
			print '<h2>Editing facilities have been temporarily restricted to moderators only.</h2>'
			PrintPostSearch(0, 0, 0, 0, 0, 0)
			sys.exit(0)

def PrintPostSearch(executable=0, records=0, subsequent=0, printed=0, mergeform=0, tableclose=True):
        if tableclose:
                print '</table>'
	if mergeform:
		print '<hr>'
		print '<p>'
		print '<input TYPE="SUBMIT" VALUE="Merge Selected Records">'
		print '</form>'
	if printed == 100:
		print '<hr>'
		print ISFDBLink('edit/%s.cgi' % executable, subsequent, '[Records: %s]' % records)

        print '</div>'
        print '<div id="bottom">'
        print COPYRIGHT
        print '<br>'
        print ENGINE
        print '</div>'
        print '</div>'
        print '</body>'
        print '</html>'

def PrintTitle(title):
	print "Content-type: text/html; charset=%s\n" % (UNICODE)
	print "<html>\n"
	print "<head><title>%s</title></head>\n" % (title)
	print "<body>\n"

def sameAuthors(title_authors, target_authors):
        # If the counts of authors for these two titles are not the same, then they are not duplicates
        if len(title_authors) != len(target_authors):
                return 0
        # If at least one author for the first title is not associated with the second title, then they are not duplicates
        for title in title_authors:
                if title not in target_authors:
                        return 0
        # If at least one author for the second title is not associated with the first title, then they are not duplicates
        for title in target_authors:
                if title not in title_authors:
                        return 0
        return 1

def PrintDuplicateTitleRecord(record, bgcolor, authors):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

	print '<td><INPUT TYPE="checkbox" NAME="merge" VALUE="' +str(record[TITLE_PUBID])+ '"></td>'
	print "<td>" +record[TITLE_YEAR][:4]+ "</td>"
	print "<td>" +record[TITLE_TTYPE]+ "</td>"
	if record[TITLE_STORYLEN]:
        	print "<td>" +record[TITLE_STORYLEN]+ "</td>"
	else:
		print "<td> </td>"

        # Print variant information
	if record[TITLE_PARENT]:
		print "<td>Variant</td>"
	else:
		print "<td> </td>"

        # Print this title's language
	if record[TITLE_LANGUAGE]:
		print "<td>%s</td>" % (LANGUAGES[int(record[TITLE_LANGUAGE])])
	else:
		print "<td> </td>"

        print "<td>%s</td>" % ISFDBLink('title.cgi', record[TITLE_PUBID], record[TITLE_TITLE])

	print "<td>"
	for author in authors:
        	print ISFDBLink('ea.cgi', author[0], author[1])
	print "</td>"

	print "<td>"
	if record[TITLE_NOTE]:
                note = SQLgetNotes(record[TITLE_NOTE])
                print FormatNote(note, '', 'edit')
        else:
                print "&nbsp;"
	print "</td>"

        print "</tr>"

def PrintDuplicateTableColumns():
	print '<table class="generic_table">'
	print '<tr class="generic_table_header">'
	print '<th>Merge</th>'
	print '<th>Year</th>'
	print '<th>Type</th>'
	print '<th>Length</th>'
	print '<th>Variant</th>'
	print '<th>Language</th>'
	print '<th>Title</th>'
	print '<th>Authors</th>'
	print '<th>Note</th>'
 	print '</tr>'

def CompareTwoTitles(title, target, mode):
        match = 0
        title_type = title[TITLE_TTYPE]
        target_type = target[TITLE_TTYPE]
        # Define a list of title types that are "containers", i.e. can contain other titles
        containers = ("COLLECTION", "ANTHOLOGY", "OMNIBUS", "CHAPBOOK", "NONFICTION")
        # Define a list of title types that can be contained in containers
        contained = ("SHORTFICTION", "ESSAY", "POEM", "SERIAL")
        # If one title is a container and the other one is a "contained" title, they are not duplicates
        if title_type in contained and target_type in containers:
                pass
        elif title_type in containers and target_type in contained:
                pass
        # Exclude all REVIEW titles
        elif title_type == "REVIEW" or target_type == "REVIEW":
                pass
        # COVERART, INTERIORART and INTERVIEW titles should only be compared to other titles of the same type
        elif title_type == "COVERART" and target_type != "COVERART":
                pass
        elif title_type != "COVERART" and target_type == "COVERART":
                pass
        elif title_type == "INTERIORART" and target_type != "INTERIORART":
                pass
        elif title_type != "INTERIORART" and target_type == "INTERIORART":
                pass
        elif title_type == "INTERVIEW" and target_type != "INTERVIEW":
                pass
        elif title_type != "INTERVIEW" and target_type == "INTERVIEW":
                pass
        # If one of the titles is a variant of the other, they are not duplicates
        elif title[TITLE_PARENT] == target[TITLE_PUBID]:
                pass
        elif target[TITLE_PARENT] == title[TITLE_PUBID]:
                pass
        # For Exact Mode, SHORTFICTION/NOVEL, SHORTFICTION, COLLECTION/CHAPBOOK,
        # NOVEL/COLLECTION, NOVEL/OMNIBUS and NOVEL/POEM pairs are not considered potential duplicates
        elif mode == 0 and ((title_type == "SHORTFICTION" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "SHORTFICTION")):
                pass
        elif mode == 0 and ((title_type == "COLLECTION" and target_type == "CHAPBOOK") or (title_type == "CHAPBOOK" and target_type == "COLLECTION")):
                pass
        elif mode == 0 and ((title_type == "COLLECTION" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "COLLECTION")):
                pass
        elif mode == 0 and ((title_type == "OMNIBUS" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "OMNIBUS")):
                pass
        elif mode == 0 and ((title_type == "POEM" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "POEM")):
                pass
        # If the two titles have different language codes, they are not duplicates
        elif title[TITLE_LANGUAGE] and target[TITLE_LANGUAGE] and (title[TITLE_LANGUAGE] != target[TITLE_LANGUAGE]):
                pass
        elif mode == 2:
                if similarTitles(title[TITLE_TITLE], target[TITLE_TITLE]):
                        match = 1
        else:
                match = 1
        
        return match

def similarTitles(string1, string2):
	newstr1 = string1.lower()
	newstr1 = newstr1.replace(' ', '')
	newstr2 = string2.lower()
	newstr2 = newstr2.replace(' ', '')
	if newstr1 == newstr2:
		return 1

	if len(newstr1) > len(newstr2):
		maxlen = len(newstr2)
	else:
		maxlen = len(newstr1)

	counter = 0
	total = 0
	while counter < maxlen:
		if newstr1[counter] == newstr2[counter]:
			total += 1
		counter += 1

	counter = 0
	while counter < maxlen:
		if newstr1[(len(newstr1)-1)-counter] == newstr2[(len(newstr2)-1)-counter]:
			total += 1
		counter += 1

	if len(newstr1) > len(newstr2):
		#ratio = float(total)/float(len(newstr1))
		ratio = float(total)/float(len(newstr2))
	else:
		#ratio = float(total)/float(len(newstr2))
		ratio = float(total)/float(len(newstr1))

	#print '<br>RATIO:', newstr1, newstr2, ratio
	if ratio > 0.85:
		return 1
	else:
		return 0

def CheckOneTitle(title):
        # Retrieve a list of title records whose titles are the same as the passed-in title's
        targets = SQLFindExactTitles(title[TITLE_TITLE])
        counter = 0
        found = 0
        first = 1
        for target in targets:
                # Skip the title record whose title ID is the same as the passed in title's
                if target[TITLE_PUBID] == title[TITLE_PUBID]:
                        continue
                match = CompareTwoTitles(title, target, 0)
                if match:
                        title_authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
                        target_authors = SQLTitleBriefAuthorRecords(target[TITLE_PUBID])
                        # Only titles with identical authors are potential duplicates
                        if sameAuthors(title_authors, target_authors):
                                found = 1
                                if first:
                                        print '<form METHOD="POST" ACTION="/cgi-bin/edit/tv_merge.cgi">'
                                        PrintDuplicateTableColumns()
                                        PrintDuplicateTitleRecord(title, 0, title_authors)
                                        first = 0
                                PrintDuplicateTitleRecord(target, 0, target_authors)

        if first == 0:
                print '</table>'
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Merge Selected Records">'
                print '</form>'
                print '<p>'
	return found

class Submission:
	def __init__(self):
		self.header = ''
		self.cgi_script = 0
		self.type = 0
		self.viewer = ''
		self.user = User()
		self.user.load()

	def file(self, update_string):
                update = """insert into submissions(sub_state, sub_type, sub_data, sub_time, sub_submitter)
                            values('N', %d, '%s', NOW(), %d)""" % (self.type, update_string, int(self.user.id))
                db.query(update)
                submission_id = db.insert_id()

                # If the user is a moderator or a self-approver and there is no override preference,
                # redirect to the review/approval page
                if not self.user.display_post_submission:
                        if SQLisUserModerator(self.user.id) or SQLisUserSelfApprover(self.user.id):
                                location = "mod/%s.cgi?%s" % (SUBMAP[self.type][0], submission_id)
                                ISFDBLocalRedirect(location)
                
                PrintPreSearch(self.header)
                PrintNavBar(self.cgi_script, 0)

                PrintWikiPointer(self.user.name)
                print '<h1>Submitting the following changes:</h1>'
                self.viewer(submission_id)
                
                # If the user is a moderator or a self-approver, allow going to the approval page
                if SQLisUserModerator(self.user.id) or SQLisUserSelfApprover(self.user.id):
                        print '<br>Moderate %s' % ISFDBLink('mod/%s.cgi' % SUBMAP[self.type][0], submission_id, 'submission')
                PrintPostSearch(0, 0, 0, 0, 0, 0)
        
        def error(self, error = '', record_id = 0):
                displayError(error, self.header, self.cgi_script, record_id)

        def CheckField(self, newUsed, oldUsed, newField, oldField, tag, multi):
                update = 0
                changes = 0
                update_string = ''

                ######################################################################
                # If a field is and was being used, update it only if it's different
                ######################################################################
                if newUsed and oldUsed:
                        if multi:
                                update = compare_lists(newField, oldField)
                        else:
                                if newField != XMLescape(oldField):
                                        update = 1

                ######################################################################
                # If a field is being used, but wasn't before, update it
                ######################################################################
                elif newUsed and (oldUsed == 0):
                        update = 1

                ######################################################################
                # If a field is not being used, but it was before, update it
                ######################################################################
                elif (newUsed == 0) and oldUsed:
                        newField = ""
                        update = 1

                if update:
                        if multi:
                                update_string = "    <%ss>\n" % (tag)
                                for field in newField:
                                        update_string += "      <%s>%s</%s>\n" % (tag, db.escape_string(field), tag)
                                update_string += "    </%ss>\n" % (tag)
                        else:
                                update_string = "    <%s>%s</%s>\n" % (tag, db.escape_string(newField), tag)

                        changes = 1
                return (changes, update_string)

        def different_authors(self, new_authors, old_authors):
                old_list = []
                for old_author in old_authors:
                        old_list.append(XMLescape(old_author))
                if set(new_authors) != set(old_list):
                        return 1
                else:
                        return 0


def compare_lists(newField, oldField):
        # Compare two lists of values. Return 1 if there are different elements, 0 otherwise.
        # The elements in the first list are XML-escaped while the second one's aren't.
        
        if len(newField) != len(oldField):
                return 1
        
        for subvalue in oldField:
                if XMLescape(subvalue) not in newField:
                        return 1

        for subvalue in newField:
                if XMLunescape(subvalue) not in oldField:
                        return 1
        return 0
