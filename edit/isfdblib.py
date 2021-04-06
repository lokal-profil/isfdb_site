#
#     (C) COPYRIGHT 2004-2020 Al von Ruff, Bill Longley, Kevin Pulliam (kevin.pulliam@gmail.com), Ahasuerus, Jesse Weinstein <jesse@wefu.org>, Uzume and Dirk Stoecker
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
import MySQLdb
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

        print '<script type="text/javascript" src="http://%s/isfdb_main.js"></script>' % HTMLLOC
        # Include the JavaScript file with the general purpose JS functions that support editing
        print '<script type="text/javascript" src="http://%s/edit_js.js"></script>' % HTMLLOC

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
        print '<a href="http:/%s/index.cgi">Click here</a> to return to browsing ISFDB.</h1></noscript>' % (HTFAKE)

def JSscript(script_name):
        print '<script type="text/javascript" src="http://%s/%s.js"></script>' % (HTMLLOC, script_name)

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
		print 'You have to <a href="http:/%s/dologin.cgi?%s+%s">login</a> to edit data.' % (HTFAKE, executable, arg)
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	editStatus = SQLgetEditingStatus()
	if editStatus == 0:
		print '<h2>Editing facilities are currently offline</h2>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	elif editStatus == 2:
		(userid, username, usertoken) = GetUserData()
		if SQLisUserModerator(userid) == 0:
			print '<h2>Editing facilities have temporarily been restricted to moderators only.</h2>'
			PrintPostSearch(0, 0, 0, 0, 0)
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
		print '<a href="http:/%s/edit/%s.cgi?%s">[Records: %s]</a>' % (HTFAKE, executable, subsequent, records)

        print '</div>'
        print '<div id="bottom">'
        print COPYRIGHT
        print '<br>'
        print ENGINE
        print '</div>'
        print '</div>'
        print '</body>'
        print '</html>'


##################################################################
# Object class for routines that interact with MySQL
##################################################################
class ISFDB:
	def __init__(self):
		self.changes = 0
		self.need_comma = 0
		self.entry1 = 0
		self.entry2 = 0
		self.entry3 = 0
		self.use1 = 0
		self.use2 = 0
		self.use3 = 0
		self.op1 = 0
		self.op2 = 0
		self.orderby = 0
		self.start = 0
		self.column_list = ""
		self.value_list = ""
		self.form = []
		self.db = []

	def SetForm(self, form):
		self.form = form
	def SetPubID(self, pubid):
		self.pubid = pubid
	def SetDb(self, db):
		self.db = db
	def GetColumnList(self):
		return self.column_list
	def GetValueList(self):
		return self.value_list
	def GetChanges(self):
		return self.changes
	def GetStart(self):
		return self.start

	def SyncTablesNew(self, newtitle, newauthor, newtag, newyear, newctype):
		if newctype and newctype != 'z':
			pubid = 0
			while pubid == 0:
				search = "select pubid from canonical where title = '"+newtitle+"'"
				search += " and author = '" +newauthor+ "'"
				search += " and ttype = '" +newctype+ "'"
	       			self.db.query(search)
				result = self.db.store_result()
				record = result.fetch_row()
				if record:
					pubid = record[0][CANONICAL_PUBID]
				else: 
					caninsert = "insert into canonical(title, author, pubs, copyright, ttype)"
					caninsert += " values( '"+ newtitle+"', '"+ newauthor+"', '"
					caninsert += newtag+"', '"+ newyear+"', '"+ newctype+"')"
					print "<br>Adding title to canonical table"
	       				self.db.query(caninsert)
					self.changes += 1

			# Check to see if a title/author entry with this tag exists
			# in the title table
			search = "select pubid from titles where title = '"+newtitle+"'"
			search += " and author = '" +newauthor+ "'"
			search += " and pub = '" +newtag+ "'"
	       		self.db.query(search)
			result = self.db.store_result()
			record = result.fetch_row()
			if record:
				pass
			else: 
				pubinsert = "insert into title(title, author, pub, year, ttype, canonical)"
				pubinsert += " values( '"+ newtitle+"', '"+ newauthor+"', '"
				pubinsert += newtag+"', '"+ newyear+ "', '"+ newctype+ "', %d)" % (pubid)
				print "<br>Adding title to title table"
	       			self.db.query(pubinsert)
				self.changes += 1


	def BuildColumnValues(self, target):
		if self.form.has_key(target):
			newtarget = escape_string(self.form[target].value)
			if self.need_comma:
				self.column_list = self.column_list+", "+target
				self.value_list = self.value_list+", '"+newtarget+"'"
			else:
				self.column_list = target
				self.value_list = "'"+newtarget+"'"
				self.need_comma = 1
			return newtarget
		else:
			return 0

	def HTMLBuildColumnValues(self, target):
		if self.form.has_key(target):
			newtarget = escape_string(self.form[target].value)
			if self.need_comma:
				self.column_list = self.column_list+", "+target
				self.value_list = self.value_list+", '"+newtarget+"'"
			else:
				self.column_list = target
				self.value_list = "'"+newtarget+"'"
				self.need_comma = 1
			return newtarget
		else:
			return 0


	def updatetable(self, newvar, oldvar, field, label, table):
		if newvar != oldvar:
			update = "update "+table+" set "+field+" = '"
			doit = 0
			if newvar:
				update = update + newvar +"' where pubid = "+self.pubid
				doit = 1
			elif oldvar != '':
				update = update + "' where pubid = "+self.pubid
				doit = 1
			if doit:
				self.changes = self.changes + 1
				self.db.query(update)
				print "<br><b>Old "+label+": </b>", oldvar
				print "<br><b>New "+label+": </b>", newvar
				print "<hr>"

	def ExtractTermsFromForm(self, default_order):
		if self.form.has_key('TERM_1'):
			self.entry1 = escape_quotes(self.form['TERM_1'].value)
		if self.form.has_key('TERM_2'):
			self.entry2 = escape_quotes(self.form['TERM_2'].value)
		if self.form.has_key('TERM_3'):
			self.entry3 = escape_quotes(self.form['TERM_3'].value)
		if self.form.has_key('USE_1'):
			self.use1 = escape_quotes(self.form['USE_1'].value)
		if self.form.has_key('TERM_2'):
			self.use2 = escape_quotes(self.form['USE_2'].value)
		if self.form.has_key('TERM_3'):
			self.use3 = escape_quotes(self.form['USE_3'].value)
		if self.form.has_key('OPERATOR_1'):
			self.op1 = escape_quotes(self.form['OPERATOR_1'].value)
		if self.form.has_key('OPERATOR_2'):
			self.op2 = escape_quotes(self.form['OPERATOR_2'].value)
		if self.form.has_key('ORDERBY'):
			self.orderby = escape_quotes(self.form['ORDERBY'].value)
		else:
			self.orderby = default_order

	def ExtractTermsFromCmdline(self):
		try:
			self.use1 = sys.argv[1]
			self.entry1 = sys.argv[2]
		except:
			pass
		try:
			self.op1 = sys.argv[3]
			if self.op1 == 'orderby':
				self.orderby = sys.argv[4]
				self.start   = string.atoi(sys.argv[5])
			else:
				self.use2 = sys.argv[4]
				self.entry2 = sys.argv[5]
		except:
			pass
		try:
			self.op2 = sys.argv[6]
			if self.op2 == 'orderby':
				self.orderby = sys.argv[7]
				self.start   = stinrg.atoi(sys.argv[8])
			else:
				self.use3 = sys.argv[7]
				self.entry3 = sys.argv[8]
				self.orderby = sys.argv[9]
				self.start   = string.atoi(sys.argv[10])
		except:
			pass


	def BuildSearchNow(self):
		retval = ''
		if self.entry1:
			retval += " "+makequery(self.entry1, self.use1)
		if self.entry2:
			retval += " "+self.op1
			retval += " "+makequery(self.entry2, self.use2)
		if self.entry3:
			retval += " "+self.op2
			retval += " "+makequery(self.entry3, self.use3)
		if self.start:
			retval += " order by "+self.orderby+" limit %d,100" % (self.start)
		else:
			retval += " order by "+self.orderby+" limit 100"
		return retval

	def BuildSearchNext(self):
		retval = ''
		if self.entry1:
			retval += self.use1+"+"+escape_spaces(self.entry1)
		if self.entry2:
			retval += "+"+escape_spaces(self.op1)+"+"+self.use2+"+"+escape_spaces(self.entry2)
		if self.entry3:
			retval += "+"+escape_spaces(self.op2)+"+"+self.use3+"+"+escape_spaces(self.entry3)
		retval += "+orderby+"+self.orderby+"+%d" % (self.start + 100)
		return retval

	def BuildPubSQL_FromForm(self, form, start):
		self.form = form
		self.ExtractTermsFromForm("isbn")
		search_string = "select * from pubs where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def BuildAuthSQL_FromForm(self, form, start):
		self.form = form
		self.ExtractTermsFromForm("birthdate")
		search_string = "select * from authors where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def BuildTitleSQL_FromForm(self, form, start):
		self.form = form
		self.ExtractTermsFromForm("year")
		search_string = "select * from titles where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def BuildPubSQL_FromCmdline(self):
		self.ExtractTermsFromCmdline()
		search_string = "select * from pubs where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def BuildAuthSQL_FromCmdline(self):
		self.ExtractTermsFromCmdline()
		search_string = "select * from authors where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def BuildTitleSQL_FromCmdline(self):
		self.ExtractTermsFromCmdline()
		search_string = "select * from titles where " + self.BuildSearchNow()
		subsequent = self.BuildSearchNext()
		return(search_string, subsequent)

	def updatepub(self, newvar, oldvar, field, label):
		self.updatetable(newvar, oldvar, field, label, 'pubs')

	def updateauth(self, newvar, oldvar, field, label):
		self.updatetable(newvar, oldvar, field, label, 'authors')

	def updatetitle(self, newvar, oldvar, field, label):
		self.updatetable(newvar, oldvar, field, label, 'titles')

	def updatenote(self, newnote, oldnote, pubid, label):
		retval = pubid
		if newnote != oldnote:
			update = "update notes set note = '"
			doit = 0
			if newnote:
				if pubid == -1:
					update = "insert into notes(note) values('" + newnote+ "');"
				else:
					update = update + escape_string(newnote) +"' where pubid = "+ str(pubid)
				doit = 1
			elif oldnote != '':
				update = update + "' where pubid = "+ str(pubid)
				doit = 1

			if doit:
				self.changes = self.changes + 1
				self.db.query(update)
				if pubid == -1:
					# Get new pubid and return to caller
					retval = self.db.insert_id()
				print "<br><b>Old "+label+": </b>", oldnote
				print "<br><b>New "+label+": </b>", newnote
				print "<hr>"
		return retval

def Date_or_None(s):
    return s

def IsfdbConvSetup():
	import MySQLdb.converters
	IsfdbConv = MySQLdb.converters.conversions
	IsfdbConv[10] = Date_or_None
	return(IsfdbConv)

def dbConnect():
	db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
	return db

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

        print "<td><a href=\"http:/"+HTFAKE+"/title.cgi?%s\">%s</a></td>" % (record[TITLE_PUBID], record[TITLE_TITLE])

	print "<td>"
	for author in authors:
        	print "<a href=\"http:/"+HTFAKE+"/ea.cgi?%s\">%s</a>" % (author[0], author[1])
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
                                location = "http:/%s/mod/%s.cgi?%s" % (HTFAKE, SUBMAP[self.type][0], submission_id)
                                ServerSideRedirect(location)
                
                ##################################################################
                # Output the leading HTML stuff
                ##################################################################
                PrintPreSearch(self.header)
                PrintNavBar(self.cgi_script, 0)

                PrintWikiPointer(self.user.name)
                print "<h1>Submitting the following changes:</h1>"
                self.viewer(submission_id)
                
                # If the user is a moderator or a self-approver, allow going to the approval page
                if SQLisUserModerator(self.user.id) or SQLisUserSelfApprover(self.user.id):
                        print '<br>Moderate <a href="http:/%s/mod/%s.cgi?%s">submission</a>' % (HTFAKE, SUBMAP[self.type][0], submission_id)
        
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
