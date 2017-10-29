#
#     (C) COPYRIGHT 2004-2017 Al von Ruff, Bill Longley, Kevin Pulliam (kevin.pulliam@gmail.com), Ahasuerus, Jesse Weinstein <jesse@wefu.org>, Uzume and Dirk Stoecker
#     ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.203 $
#     Date: $Date: 2017/08/31 20:10:54 $


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
# Various routines to print a full record for a particular table
##################################################################

PubFields   = [ PUB_TAG, PUB_TITLE, PUB_YEAR, 
	        PUB_PUBLISHER, PUB_ISBN, PUB_PRICE, PUB_PAGES,
	        PUB_PTYPE, PUB_CTYPE, PUB_IMAGE ]
AuthFields  = [ AUTHOR_CANONICAL, AUTHOR_LEGALNAME, AUTHOR_BIRTHPLACE,
	        AUTHOR_BIRTHDATE, AUTHOR_DEATHDATE]
TitleFields = [ TITLE_PUBID, TITLE_TITLE, TITLE_YEAR, TITLE_TTYPE, TITLE_SERIES, TITLE_SERIESNUM ]

	     
def printfield(record, field):
	if record[0][field]:
		print "<td>%s</td>" % record[0][field]
	else:
		print "<td>?</td>"

def PrintRecord(record, eccolor, table, editor, pubid, checkbox, auth):
	if eccolor:
		print '<tr align=left class="table1">'
	else:
		print '<tr align=left class="table2">'

	if checkbox:
		print '<td><INPUT TYPE="checkbox" NAME="merge" VALUE="%s"></td>' % record[0][TITLE_PUBID]
	print "<td>%s<td>" % ISFDBLink("edit/%s.cgi" % editor, record[0][pubid], record[0][pubid])
	for column in table:
		if auth and column == AUTHOR_CANONICAL:
			au = record[0][column]
			print "<td>%s</td>" % ISFDBLink("ea.cgi", record[0][AUTHOR_ID], au)
		else:
			printfield(record, column)
	print "</tr>"

def PrintPubRecord(record, eccolor):
	PrintRecord(record, eccolor, PubFields, "editpub", PUB_PUBID, 0, 0)
	
def PrintAuthRecord(record, eccolor):
	PrintRecord(record, eccolor, AuthFields, "editauth", AUTHOR_ID, 1, 1)

def PrintTitleRecord(record, eccolor):
	PrintRecord(record, eccolor, TitleFields, "edittitle", TITLE_PUBID, 1, 0)

##################################################################
# Various routines to print table headers are defined here
##################################################################

PubHeader   = ['Record #', 'Tag', 'Title', 'Author',  'Year', 'Publisher',
	       'ISBN / Cat#', 'Price', 'Pages', 'Pub Type', 'C Type',
	       'Cover Artist', 'Image URL']
AuthHeader  = ['Record #', 'Canonical Name', 'Legal Name', 'Birthplace', 
	       'Birthdate', 'Deathdate']
TitleHeader = ['Record #', 'Title', 'Author',  'Year', 'Type' ]

def PrintHeader(record, table, merge):
	if merge == 1:
		print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/tv_merge.cgi\">"
	elif merge == 2:
		print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/mergeauth.cgi\">"
	if record:
		print "<table cellpadding=0 BGCOLOR=\"#FFFFFF\">"
		print "<tr align=left bgcolor=\"#d6d6d6\">"
		if merge:
			print "<td><b>Merge</b></td>"
		for column in table:
			print "<td><b>%s</b></td>" % (column)
		print "</tr>"
	else:
		print "<h2>Query: No Records Found</h2>"
		print "<table>"

def PrintPubHeader(record):
	PrintHeader(record, PubHeader, 0)

def PrintTitleHeader(record):
	PrintHeader(record, TitleHeader, 1)

def PrintAuthHeader(record):
	PrintHeader(record, AuthHeader, 2)

##################################################################
# These routines start and end the HTML page
##################################################################
def PrintPreSearch(title):
        print 'Content-type: text/html; charset=%s\n' % (UNICODE)
	print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
	print '<html lang="en-us">'
        print '<head>'
        print '<meta http-equiv="content-type" content="text/html; charset=%s" >' % UNICODE
	print '<link rel="shortcut icon" href="http://%s/favicon.ico">' % (HTMLHOST)
        print '<title>%s</title>' % (title)

        # Include the JavaScript file with the general purpose JS functions that support editing
        print '<script type="text/javascript" src="http://%s/edit_js.js"></script>' % HTMLLOC

	if title in ('Publication Editor', 'Add Publication', 'New Novel', 'New Magazine',
                     'New Anthology', 'New Collection', 'New Omnibus', 'New Nonfiction',
                     'New Fanzine', 'New Chapbook', 'Clone Publication', 'Import/Export Contents'):
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

        print '<style type="text/css" media="screen">'
        print '  @import url("http://%s/biblio.css");' % (HTMLHOST)
        print '</style></head>'

        body = '<body'
        # Set focus on the first active field in the form
        if 'New Award Category for' in title:
                body += ' onload="document.getElementById(\'award_cat_name\').focus();" '
        elif ((title[0:4] == 'New ') and (title != "New Publication Submission")) or (title == 'Clone Publication'):
                body += ' onload="document.getElementById(\'pub_title\').focus();" '
        # For Add Pub, focus on the Pub Year field since the first two fields are read-only
        elif title == 'Add Publication':
                body += ' onload="document.getElementById(\'pub_year\').focus();" '
        # 
        elif title[:14] == 'Import Content':
                body += ' onload="document.getElementById(\'ExportFrom\').focus();" '
        elif title[:14] == 'Export Content':
                body += ' onload="document.getElementById(\'ExportTo\').focus();" '
	elif title == 'Title Editor':
                body += ' onload="document.getElementById(\'title_title\').focus();" '
	elif title == 'Author Editor':
                body += ' onload="document.getElementById(\'author_canonical\').focus();" '
	elif title == 'Award Editor':
                body += ' onload="document.getElementById(\'award_title\').focus();" '
	elif title == 'Award Editor for a Title':
                body += ' onload="document.getElementById(\'award_year\').focus();" '
	elif (title == 'Award Type Editor') or (title == 'Add New Award Type'):
                body += ' onload="document.getElementById(\'award_type_short_name\').focus();" '
	elif title == 'Publication Editor':
                body += ' onload="document.getElementById(\'pub_title\').focus();" '
	elif title == 'Publisher Editor':
                body += ' onload="document.getElementById(\'publisher_name\').focus();" '
	elif title == 'Publication Series Editor':
                body += ' onload="document.getElementById(\'pub_series_name\').focus();" '
	elif title == 'Series Editor':
                body += ' onload="document.getElementById(\'series_name\').focus();" '
        # Setting focus is commented out for Tag Editor because setting focus to the
        # first tag is not useful when there are pre-existing tags
##	elif title == 'Tag Editor':
##                body += ' onload="document.getElementById(\'tag_name1\').focus();" '
	elif title == 'Link Review':
                body += ' onload="document.getElementById(\'Parent\').focus();" '
	elif title[:23] == 'Make/Remove a Pseudonym':
                body += ' onload="document.getElementById(\'ParentName\').focus();" '
	elif title == 'Make Variant Title':
                body += ' onload="document.getElementById(\'Parent\').focus();" '
	elif title == 'Add Variant Title':
                body += ' onload="document.getElementById(\'title_title\').focus();" '
	elif title == 'Link Award':
                body += ' onload="document.getElementById(\'title_id\').focus();" '
        body += '>'
        print body

        print '<div id="wrap">'
        print '<a class="topbanner" href="http:/%s/index.cgi"></a>' % (HTFAKE)
        print '<div id="statusbar">'
        print '<h2>%s</h2>' % (title)
        print '</div>'
        if (title != "Title Search") and (title != "Author Search") and (title != "Pub Search"):
                # The "<noscript>" part will only be executed if Javascript is not enabled on the browser side
                print '<noscript><h1>Your browser does not support JavaScript. Javascript is required to edit ISFDB.'
                print '<a href="http:/%s/index.cgi">Click here</a> to return to browsing ISFDB.</h1></noscript>' % (HTFAKE)

def JSscript(script_name):
        print '<script type="text/javascript" src="http://%s/%s.js"></script>' % (HTMLLOC, script_name)
        # For pages with publication data, include a function which returns an array of external
        # identifier types likes ASINs and LCCNs
        if script_name == 'edit_pub':
                identifier_types = SQLLoadIdentifierTypes()
                print '<script type="text/javascript">'
                print 'function ExternalIdentifiers() {'
                output = ' var identifiers = ['
                for identifier_type in sorted(identifier_types, key = identifier_types.get):
                        output += '{"id":%d, "name":"%s"}, ' % (identifier_type, identifier_types[identifier_type][0])
                print '%s];' % output[:-2]
                print ' return identifiers;'
                print '}'
                print '</script>'


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
                print "</table>\n"
	if mergeform:
		print "<hr />\n"
		print "<p>"
		print "<input TYPE=\"SUBMIT\" VALUE=\"Merge Selected Records\">"
		print "</form>"
	if printed == 100:
		print "<hr />\n"
		print "<a href=\"http://"+DBASEHOST+"/cgi-bin/edit/"+executable+".cgi?"+subsequent+"\">[Records: %s]</a>" % (records)

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
	print "<table cellpadding=0 BGCOLOR=\"#FFFFFF\">"
	print "<tr align=left bgcolor=\"#d6d6d6\">"
	print "<td><b>Merge</b></td>"
	print "<td><b>Year</b></td>"
	print "<td><b>Type</b></td>"
	print "<td><b>Length</b></td>"
	print "<td><b>Variant</b></td>"
	print "<td><b>Language</b></td>"
	print "<td><b>Title</b></td>"
	print "<td><b>Authors</b></td>"
	print "<td><b>Note</b></td>"
 	print "</tr>"

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
                                        print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/tv_merge.cgi\">"
                                        PrintDuplicateTableColumns()
                                        PrintDuplicateTitleRecord(title, 0, title_authors)
                                        first = 0
                                PrintDuplicateTitleRecord(target, 0, target_authors)

        if first == 0:
                print "</table>"
                print "<input TYPE=\"SUBMIT\" VALUE=\"Merge Selected Records\">"
                print "</form>"
                print "<p>"
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

                # If the user is a moderator and there is no override preference,
                # redirect him to the review/approval page
                if not self.user.display_post_submission and SQLisUserModerator(self.user.id):
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
                
                # If the user is a moderator, let him go straight to the approval page
                if SQLisUserModerator(self.user.id):
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

def reportsDict():
        reports = {}
        reports[1] = ("Titles without Authors")
        reports[2] = ("Variant Title-Pseudonym Mismatches")
        reports[3] = ("Titles without Pubs")
        reports[4] = ("Mismatched Double Quotes")
        reports[5] = ("Mismatched Angle Brackets")
        reports[6] = ("Authors with Invalid Family Names")
        reports[7] = ("Author Names with Invalid Data or an Unrecognized Suffix")
        reports[8] = ("Authors That Exist Only Due to Reviews")
        reports[9] = ("Variant Titles in Series")
        reports[10] = ("Pseudonyms with Canonical Titles")
        reports[11] = ("Prolific Authors without a Defined Language")
        reports[12] = ("EDITOR Records not in a Series")
        reports[13] = ("Variant EDITOR Records in a Series")
        reports[14] = ("Missing EDITOR Records")
        reports[15] = ("Publications with Extra EDITOR Records")
        reports[16] = ("Empty Series")
        reports[17] = ("Series with Duplicate Numbers")
        reports[18] = ("Titles with Bad Ellipses")
        reports[19] = ("Interviews of Pseudonyms")
        reports[20] = ("Variant Titles of Variant Titles")
        reports[21] = ("Variant Titles of Missing Titles")
        reports[22] = ("SERIALs without a Parent Title")
        reports[23] = ("Awards Associated with Invalid Titles")
        reports[24] = ("Suspect Untitled Awards")
        reports[25] = ("Empty Award Types")
        reports[26] = ("Empty Award Categories")
        reports[27] = ("Series with Chapbooks")
        reports[28] = ("Chapbooks with Synopses")
        reports[29] = ("Chapbooks without Contents Titles")
        reports[30] = ("Chapbooks with Mismatched Variant Types")
        reports[31] = ("Pre-2005 ISBN-13s and post-2007 ISBN-10s")
        reports[32] = ("Duplicate Publication Tags")
        reports[33] = ("Publication Authors That Are Not the Title Author")
        reports[34] = ("Publications Without Titles")
        reports[35] = ("Invalid Publication Formats")
        reports[36] = ("Pubs with Images We Don't Have Permission to Link to")
        reports[37] = ("Omnibuses without Contents Titles")
        reports[38] = ("Publications with Duplicate Titles")
        reports[39] = ("Publications with Bad Ellipses")
        reports[40] = ("Reviews without Reviewed Authors")
        reports[41] = ("Reviews not Linked to Titles")
        reports[42] = ("Reviews of Uncommon Title Types")
        reports[43] = ("Publishers with Identical Names")
        reports[44] = ("Publishers with Similar Names")
        reports[45] = ("Variant Title Type Mismatches")
        reports[46] = ("EDITOR records not in MAGAZINE/FANZINE publications")
        reports[47] = ("Title Dates after Publication Dates")
        reports[48] = ("Series with Numbering Gaps")
        reports[49] = ("Publications with Invalid Catalog IDs")
        reports[50] = ("Publications with Invalid ISBNs")
        reports[51] = ("Publications with Identical ISBNs and Different Titles")
        reports[52] = ("Publication-Title Type Mismatches")
        reports[53] = ("Authors with Duplicate Pseudonyms")
        reports[54] = ("Container Titles in Publications with no Contents")
        reports[55] = ("Title records with HTML in Titles")
        reports[56] = ("Publications with HTML in Titles")
        reports[57] = ("Invalid SFE3 Image Links")
        reports[58] = ("Suspected Dutch Authors without a Language Code")
        reports[59] = ("Suspected French Authors without a Language Code")
        reports[60] = ("Suspected German Authors without a Language Code")
        reports[61] = ("Suspected Other Non-English Authors without a Language Code")
        reports[62] = ("Titles with Invalid Length Values")
        reports[63] = ("Genre/Non-Genre Mismatches")
        reports[64] = ("Series with EDITOR and non-EDITOR Titles")
        reports[65] = ("Publishers with Invalid Unicode Characters")
        reports[66] = ("Publication Series with Invalid Unicode Characters")
        reports[67] = ("Series with Invalid Unicode Characters")
        reports[68] = ("Authors with Invalid Unicode Characters")
        reports[69] = ("Titles with Invalid Unicode Characters")
        reports[70] = ("Publications with Invalid Unicode Characters")
        reports[71] = ("Forthcoming Titles")
        reports[72] = ("Forthcoming Publications")
        reports[73] = ("Publishers with Suspect Unicode Characters")
        reports[74] = ("Titles with Suspect Unicode Characters")
        reports[75] = ("Publications with Suspect Unicode Characters")
        reports[76] = ("Series with Suspect Unicode Characters")
        reports[77] = ("Publication Series with Suspect Unicode Characters")
        reports[78] = ("Authors with Suspect Unicode Characters")
        reports[79] = ("Novel Publications with Fewer Than 80 Pages")
        reports[80] = ("Duplicate SHORTFICTION in Magazines/Fanzines")
        reports[81] = ("Series with Slashes and No Spaces")
        reports[82] = ("Invalid Record URLs in Notes")
        reports[83] = ("Serials without Standard Parenthetical Disambiguators")
        reports[84] = ("Serials with Potentially Unnecessary Disambiguation")
        reports[85] = ("Non-Latin Authors with Latin Characters in Legal Names")
        reports[86] = ("Primary-Verified Publications with Unknown Format")
        reports[87] = ("Author/Title Language Mismatches")
        reports[88] = ("Pubs with Multiple COVERART Titles")
        reports[89] = ("Authors with Invalid Birthplaces")
        reports[90] = ("Duplicate Sub-series Numbers within a Series")
        reports[91] = ("Non-Art Titles by Non-English Authors without a Language")
        reports[92] = ("Primary-Verified Anthologies and Collections without Contents Titles")
        reports[93] = ("Publication Title-Reference Title Mismatches")
        reports[94] = ("Authors Without Titles")
        reports[95] = ("Authors With Dangling Publications")
        reports[96] = ("COVERART Titles with a 'Cover:' Prefix")
        reports[97] = ("Publication Series with Latin Names and Non-Latin Titles")
        reports[98] = ("Publication Series with Identical Names")
        reports[99] = ("Publishers with Latin Names and Non-Latin Titles")
        reports[100] = ("Publications with Invalid Prices")
        reports[101] = ("Publications with Wiki pages")
        reports[102] = ("Publications with Talk pages")
        reports[103] = ("Publication Wiki pages not linked to Publication records")
        reports[104] = ("Publication Talk Wiki pages not linked to Publication records")
        reports[105] = ("Series with Wiki pages")
        reports[106] = ("Series with Talk pages")
        reports[107] = ("Series Wiki pages not linked to Series records")
        reports[108] = ("Series Talk Wiki pages not linked to Series records")
        reports[109] = ("Publishers with Wiki pages")
        reports[110] = ("Publishers with Talk pages")
        reports[111] = ("Publisher Wiki pages not linked to Publisher records")
        reports[112] = ("Publisher Talk Wiki pages not linked to Publisher records")
        reports[113] = ("Magazines with Wiki pages")
        reports[114] = ("Magazines with Talk pages")
        reports[115] = ("Magazine Wiki pages not linked to Magazine records")
        reports[116] = ("Magazine Talk Wiki pages not linked to Magazine records")
        reports[117] = ("Fanzines with Wiki pages")
        reports[118] = ("Fanzines with Talk pages")
        reports[119] = ("Fanzine Wiki pages not linked to Fanzine records")
        reports[120] = ("Fanzine Talk Wiki pages not linked to Fanzine records")
        reports[121] = ("Publication Series with non-Latin Names without Transliterated Names")
        reports[122] = ("Publishers with non-Latin Names without Transliterated Names")
        reports[123] = ("Authors with Transliterated Legal Names and no Legal Names")
        reports[124] = ("Bulgarian Titles without Transliterated Titles")
        reports[125] = ("Chinese Titles without Transliterated Titles")
        reports[126] = ("Czech Titles without Transliterated Titles")
        reports[127] = ("English Titles with non-Latin characters and without Transliterated Titles")
        reports[128] = ("Greek Titles without Transliterated Titles")
        reports[129] = ("Hungarian Titles without Transliterated Titles")
        reports[130] = ("Japanese Titles without Transliterated Titles")
        reports[131] = ("Lithuanian Titles without Transliterated Titles")
        reports[132] = ("Polish Titles without Transliterated Titles")
        reports[133] = ("Romanian Titles without Transliterated Titles")
        reports[134] = ("Russian Titles without Transliterated Titles")
        reports[135] = ("Serbian Titles without Transliterated Titles")
        reports[136] = ("Turkish Titles without Transliterated Titles")
        reports[137] = ("Other Titles without Transliterated Titles")
        reports[138] = ("Bulgarian Titles with Latin characters")
        reports[139] = ("Chinese Titles with Latin characters")
        reports[140] = ("Greek Titles with Latin characters")
        reports[141] = ("Japanese Titles with Latin characters")
        reports[142] = ("Russian Titles with Latin characters")
        reports[143] = ("Other Non-Latin Language Titles with Latin characters")
        reports[144] = ("Series Names That May Need Disambiguation")
        reports[145] = ("Romanian titles with s-cedilla or t-cedilla")
        reports[146] = ("Pubs with Romanian titles with s-cedilla or t-cedilla")
        reports[147] = ("Pubs with fullwidth yen signs")
        reports[148] = ("Bulgarian Publications without Transliterated Titles")
        reports[149] = ("Chinese Publications without Transliterated Titles")
        reports[150] = ("Czech Publications without Transliterated Titles")
        reports[151] = ("English Publications with non-Latin characters and without Transliterated Titles")
        reports[152] = ("Greek Publications without Transliterated Titles")
        reports[153] = ("Hungarian Publications without Transliterated Titles")
        reports[154] = ("Japanese Publications without Transliterated Titles")
        reports[155] = ("Lithuanian Publications without Transliterated Titles")
        reports[156] = ("Polish Publications without Transliterated Titles")
        reports[157] = ("Romanian Publications without Transliterated Titles")
        reports[158] = ("Russian Publications without Transliterated Titles")
        reports[159] = ("Serbian Publications without Transliterated Titles")
        reports[160] = ("Turkish Publications without Transliterated Titles")
        reports[161] = ("Other Publications without Transliterated Titles")
        reports[162] = ("Bulgarian Publications with Latin characters")
        reports[163] = ("Chinese Publications with Latin characters")
        reports[164] = ("Greek Publications with Latin characters")
        reports[165] = ("Japanese Publications with Latin characters")
        reports[166] = ("Russian Publications with Latin characters")
        reports[167] = ("Other Non-Latin Language Publications with Latin characters")
        reports[168] = ("Authors with Author Data and One Non-Latin Title")
        reports[169] = ("Bulgarian Authors without Transliterated Names")
        reports[170] = ("Chinese Authors without Transliterated Names")
        reports[171] = ("Czech Authors without Transliterated Names")
        reports[172] = ("English Authors with non-Latin characters and without Transliterated Names")
        reports[173] = ("Greek Authors without Transliterated Names")
        reports[174] = ("Hungarian Authors without Transliterated Names")
        reports[175] = ("Japanese Authors without Transliterated Names")
        reports[176] = ("Lithuanian Authors without Transliterated Names")
        reports[177] = ("Polish Authors without Transliterated Names")
        reports[178] = ("Romanian Authors without Transliterated Names")
        reports[179] = ("Russian Authors without Transliterated Names")
        reports[180] = ("Serbian Authors without Transliterated Names")
        reports[181] = ("Turkish Authors without Transliterated Names")
        reports[182] = ("Other Authors without Transliterated Names")
        reports[183] = ("Bulgarian Titles with a Latin Author Name")
        reports[184] = ("Chinese Titles with a Latin Author Name")
        reports[185] = ("Greek Titles with a Latin Author Name")
        reports[186] = ("Japanese Titles with a Latin Author Name")
        reports[187] = ("Russian Titles with a Latin Author Name")
        reports[188] = ("Other Non-Latin Language Titles with a Latin Author Name")
        reports[189] = ("Authors with Non-Latin Family Names")
        reports[190] = ("Awards with Invalid IMDB Links")
        reports[191] = ("Invalid HREFs in Publication Notes")
        reports[192] = ("Authors without a Working Language")
        reports[193] = ("Multilingual Publications")
        reports[194] = ("Titles without a Language")
        reports[195] = ("Invalid Title Content Values")
        reports[196] = ("Juvenile/Non-Juvenile Mismatches")
        reports[197] = ("Novelization/Non-Novelization Mismatches")
        reports[198] = ("Author/Pseudonym Language Mismatches")
        reports[199] = ("Author Notes to be Migrated from ISFDB 1.0")
        reports[200] = ("Authors with 'Author' Wiki pages")
        reports[201] = ("Authors with 'Author Talk' Wiki pages")
        reports[202] = ("Author Wiki pages not linked to Author records")
        reports[203] = ("Author Talk pages not linked to Author records")
        reports[204] = ("Authors with 'Bio' Wiki pages")
        reports[205] = ("Authors with 'Bio Talk' Wiki pages")
        reports[206] = ("Bio pages not linked to Author records")
        reports[207] = ("Bio Talk pages not linked to Author records")
        reports[208] = ("Publications with unsupported HTML in Notes")
        reports[209] = ("Titles with unsupported HTML in Notes")
        reports[210] = ("Publishers with unsupported HTML in Notes")
        reports[211] = ("Series with unsupported HTML in Notes")
        reports[212] = ("Publication Series with unsupported HTML in Notes")
        reports[213] = ("Awards with unsupported HTML in Notes")
        reports[214] = ("Award Types with unsupported HTML in Notes")
        reports[215] = ("Award Categories with unsupported HTML in Notes")
        reports[216] = ("Titles with unsupported HTML in Synopses")
        reports[217] = ("Authors with unsupported HTML in Notes")
        reports[218] = ("Publications with ASINs in Notes")
        reports[219] = ("Publications with British library IDs in Notes")
        reports[220] = ("Publications with direct SFBG links in Notes")
        reports[221] = ("Publications with direct Deutsche Nationalbibliothek links in Notes (first 500)")
        reports[222] = ("Publications with direct FantLab links in Notes")
        reports[223] = ("Publications with direct Amazon links in Notes")
        reports[224] = ("Publications with direct BNF links in Notes")
        reports[225] = ("Publications with direct Library of Congress links in Notes (first 500)")
        reports[226] = ("Publications with direct OCLC/WorldCat links in Notes (first 500)")
        reports[227] = ("Titles with mismatched parentheses")
        reports[228] = ("ISBN-less e-pubs without an ASIN")
        reports[229] = ("Mismatched HTML tags in Publication Notes")
        reports[230] = ("Mismatched OCLC URLs in Publication Notes")
        reports[231] = ("Invalid Smashwords Image Links")
        reports[232] = ("Award Years with Month/Day Data")
        reports[233] = ("Potential Duplicate E-book Publications")
        reports[234] = ("Publications with direct De Nederlandse Bibliografie links in Notes")
        reports[9999] = ("Suspected Duplicate Authors (monthly)")

        sections = [('Authors', (6, 7, 8, 10, 53, 68, 78, 89, 94, 95, 198, 199, 9999)), ]
        sections.append(('Magazines', (12, 13, 14, 15, 46)), )
        sections.append(('Publications', (32, 33, 31, 34, 35, 36, 37, 38, 39,
                                          49, 50, 51, 52, 56, 57, 70, 75, 79,
                                          86, 88, 92, 93, 100, 193, 228, 231,
                                          233)), )
        sections.append(('Series', (16, 17, 48, 64, 67, 76, 81, 90, 144)), )
        sections.append(('Titles', (19, 1, 3, 18, 47, 54, 55, 62, 63, 69, 74, 80, 87,
                                    91, 96, 194, 195, 196, 197, 227)), )
        sections.append(('Variant Titles', (20, 21, 9, 2, 45)), )
        sections.append(('Chapbooks', (27, 28, 29, 30)), )
        sections.append(('Serials', (22, 83, 84)), )
        sections.append(('Awards', (23, 24, 25, 26, 190, 232)), )
        sections.append(('Notes/Synopses', (4, 5, 82, 191, 217, 208, 209, 216, 210, 211,
                                            212, 213, 214, 215, 218, 219, 220, 221, 222,
                                            223, 224, 225, 226, 229, 230, 234)), )
        sections.append(('Reviews', (40, 41, 42)), )
        sections.append(('Publishers', (43, 44, 65, 73)), )
        sections.append(('Publication Series', (66, 77, 98)), )
        sections.append(('Authors: Languages', (192, 11, 58, 59, 60, 61, 168, 183, 184, 185,
                                                186, 187, 188, 189)), )
        sections.append(('Author Names: Transliteration', (169, 170, 171, 172, 173, 174,
                                                           175, 176, 177, 178, 179, 180,
                                                           181, 182)), )
        sections.append(('Legal Names: Transliteration', (85, 123)), )
        sections.append(('Publishers: Transliteration', (99, 122)), )
        sections.append(('Publication Series: Transliteration', (97, 121)), )
        sections.append(('Titles: Transliteration', (124, 125, 126, 127, 128,
                                              129, 130, 131, 132, 133, 134, 135, 136,
                                              137, 138, 139, 140, 141, 142, 143, 145)), )
        sections.append(('Publications: Transliteration', (148, 149, 150, 151, 152, 153,
                                                         154, 155, 156, 157, 158, 159, 160, 161,
                                                         162, 163, 164, 165, 166, 167, 146, 147)), )
        sections.append(('Wiki Cleanup', (101, 102, 103, 104, 105, 106, 107, 108, 109,
                                          110, 111, 112, 113, 114, 115, 116, 117, 118,
                                          119, 120, 200, 201, 202, 203, 204, 205, 206, 207)), )
        sections.append(('Forthcoming Books', (71, 72)), )

        # A tuple of report IDs which non-moderators are allowed to view
        non_moderator = (1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 14, 15, 16, 19,
                         20, 22, 29, 33, 34, 38, 41, 46, 48, 49, 54, 58, 59,
                         60, 61, 71, 72, 82, 83, 84, 85, 86, 87, 88,
                         91, 92, 93, 95, 97, 99,
                         100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                         110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
                         120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
                         130, 131, 132, 133, 134, 135, 136, 137, 138, 139,
                         140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
                         150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
                         160, 161, 162, 163, 164, 165, 166, 167, 168, 169,
                         170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
                         180, 181, 182, 183, 184, 185, 186, 187, 188, 189,
                         190, 191, 192, 193, 194, 195, 196, 197, 199, 200,
                         201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
                         211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
                         221, 222, 223, 224, 225, 226, 227, 228, 229, 230,
                         232, 233, 234, 9999)
        
        return (reports, sections, non_moderator)
