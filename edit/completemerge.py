#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2014   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/01/17 05:24:43 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *


#################################################################
# mergeto   = The record updates are to be written to
# record1   = SQL record #1
# record2   = SQL record #2
# userec    = Which record to use for this field
#################################################################
def MergeAuthor(db, mergeto, record1, record2, userec):

	# XXX - Need to handle pub_content table

	title_id1 = record1[0][TITLE_PUBID]
	title_id2 = record2[0][TITLE_PUBID]
	if userec == mergeto:
		if userec == '1':
			query = "delete from canonical_author where title_id=%d" % (title_id2)
		else:
			query = "delete from canonical_author where title_id=%d" % (title_id1)
		print query
		db.query(query)
	else:
		if mergeto == '1':
			query = "delete from canonical_author where title_id=%d" % (title_id1)
			print query
			db.query(query)
			query = "update canonical_author set title_id=%d where title_id=%d" % (title_id1, title_id2)
			print query
			db.query(query)
		else:
			query = "delete from canonical_author where title_id=%d" % (title_id2)
			print query
			db.query(query)
			query = "update canonical_author set title_id=%d where title_id=%d" % (title_id2, title_id1)
			print query
			db.query(query)

#################################################################
# mergeto   = The record updates are to be written to
# record1   = SQL record #1
# record2   = SQL record #2
# field     = SQL record offset
# fieldname = SQL field name
# userec    = Which record to use for this field
#################################################################
def Merge(db, mergeto, record1, record2, field, fieldname, userec):
	if record1[0][field] != record2[0][field]:
		query = "update titles set " +fieldname+ "=" 
		if userec == "1":
			if mergeto == '2':
				if record1[0][field]:
					query += "'" +escape_quotes(record1[0][field])+ "' where title_id=" + str(record2[0][TITLE_PUBID])
				else:
					query += "NULL where title_id=" + str(record2[0][TITLE_PUBID])
				print query
				db.query(query)
				print '<tr align=left bgcolor="c0ffc0">'
				print '<td><b>' +fieldname+ '</b> (updated)</td>' 
				if record2[0][field]:
					print '<td>' +str(record1[0][field])+ '</td>'
				else:
					print '<td>NULL</td>'
				print '</tr>'
			else:
				print '<tr align=left bgcolor="ececec">'
				print '<td><b>' +fieldname+ '</b> (no update)</td>' 
				if record1[0][field]:
					print '<td>' +str(record1[0][field])+ '</td>'
				else:
					print '<td>NULL</td>'
				print '</tr>'
		else:
			if mergeto == '1':
				if record2[0][field]:
					query += "'" +escape_quotes(record2[0][field])+ "' where title_id=" + str(record1[0][TITLE_PUBID])
				else:
					query += "NULL where title_id=" + str(record1[0][TITLE_PUBID])
				print query
				db.query(query)
				print '<tr align=left bgcolor="c0ffc0">'
				print '<td><b>' +fieldname+ '</b> (updated)</td>' 
				if record2[0][field]:
					print '<td>' +str(record2[0][field])+ '</td>'
				else:
					print '<td>NULL</td>'
				print '</tr>'
			else:
				print '<tr align=left bgcolor="ececec">'
				print '<td><b>' +fieldname+ '</b> (no update)</td>' 
				if record2[0][field]:
					print '<td>' +str(record2[0][field])+ '</td>'
				else:
					print '<td>NULL</td>'
				print '</tr>'
		return
	print '<tr align=left bgcolor="ececec">'
	print '<td><b>' +fieldname+ '</b> (no update)</td>' 
	if record1[0][field]:
		print '<td>' +record1[0][field]+ '</td>'
	else:
		print '<td>NULL</td>'
	print '</tr>'


def Concat(db, mergeto, record1, record2, field, fieldname, concat):
	if record1[0][field] and record2[0][field]:
		newfield = record1[0][field] +concat+ record2[0][field]
	elif record1[0][field]:
		newfield = record1[0][field]
	elif record2[0][field]:
		newfield = record2[0][field]
	else:
		print '<tr align=left bgcolor="ececec">'
		print '<td><b>' +fieldname+ '</b> (no update)</td>' 
		print '<td>NULL</td>'
		print '</tr>'
		return

	query = "update titles set " +fieldname+ "='" +escape_quotes(newfield)+ "' where title_id="
	if mergeto == '1':
		if record1[0][field] != newfield:
			query += str(record1[0][TITLE_PUBID])
		else:
			print '<tr align=left bgcolor="ececec">'
			print '<td><b>' +fieldname+ '</b> (no update)</td>' 
			print '<td>' +record1[0][field]+ '</td>'
			print '</tr>'
			return
	else:
		if record2[0][field] != newfield:
			query += str(record2[0][TITLE_PUBID])
		else:
			print '<tr align=left bgcolor="ececec">'
			print '<td><b>' +fieldname+ '</b> (no update)</td>' 
			print '<td>' +record2[0][field]+ '</td>'
			print '</tr>'
			return
	print query
	db.query(query)
	print '<tr align=left bgcolor="c0ffc0">'
	print '<td><b>' +fieldname+ '</b> (updated)</td>' 
	print '<td>' +newfield+ '</td>'
	print '</tr>'


def ConcatNote(db, mergeto, record1, record2, field, fieldname, concat):
	if record1[0][field] and record2[0][field]:
		# We actually have to do some work in this case
		pass
	elif record1[0][field]:
		if mergeto == '2':
			query = "update titles set " +fieldname+ "='" 
			query += str(record1[0][field])+ "' where title_id=" 
			query += str(record2[0][TITLE_PUBID])
			print query
			db.query(query)
			print '<tr align=left bgcolor="c0ffc0">'
			print '<td><b>' +fieldname+ '</b> (updated)</td>' 
			print '<td>' +str(record2[0][field])+ '</td>'
			print '</tr>'
		else:
			print '<tr align=left bgcolor="ececec">'
			print '<td><b>' +fieldname+ '</b> (no update)</td>' 
			print '<td>' +str(record2[0][field])+ '</td>'
			print '</tr>'
		return
	elif record2[0][field]:
		if mergeto == '1':
			query = "update titles set " +fieldname+ "='" 
			query += str(record2[0][field])+ "' where title_id=" 
			query += str(record1[0][TITLE_PUBID])
			print query
			db.query(query)
			print '<tr align=left bgcolor="c0ffc0">'
			print '<td><b>' +fieldname+ '</b> (updated)</td>' 
			print '<td>' +str(record1[0][field])+ '</td>'
			print '</tr>'
		else:
			print '<tr align=left bgcolor="ececec">'
			print '<td><b>' +fieldname+ '</b> (no update)</td>' 
			print '<td>' +str(record1[0][field])+ '</td>'
			print '</tr>'
		return
	else:
		return

	search = "select note from notes where note_id = "+ str(record1[0][field])
	db.query(search)
	res1 = db.store_result()
	note1 = res1.fetch_row()

	search = "select note from notes where note_id = "+ str(record2[0][field])
	db.query(search)
	res2 = db.store_result()
	note2 = res2.fetch_row()

	newnote = escape_quotes(note1[0][0] +concat+ note2[0][0])
	query = "update titles set " +fieldname+ "='" 
	query += newnote+ "' where title_id=" 
	if mergeto == '1':
		query += str(record1[0][TITLE_PUBID])
	else:
		query += str(record2[0][TITLE_PUBID])
	print query
	db.query(query)
	print '<tr align=left bgcolor="c0ffc0">'
	print '<td><b>' +fieldname+ '</b> (updated)</td>' 
	print '<td>' +newnote+ '</td>'
	print '</tr>'



##################################################################
# Output the leading HTML stuff
##################################################################
PrintTitle("Merge Results")

##################################################################
# Gather the form input
##################################################################
sys.stderr = sys.stdout
form = cgi.FieldStorage()
if form.has_key('record1'):
	recno1 = form['record1'].value
else:
	print "<h1>Couldn't extract record1 ID</h1>"
	sys.exit(1)
if form.has_key('record2'):
	recno2 = form['record2'].value
else:
	print "<h1>Couldn't extract record2 ID</h1>"
	sys.exit(1)

##################################################################
# Initialize defaults
##################################################################
titlerec       = '1'
authorrec      = '1'
copyrightrec   = '1'
seriesrec      = '1'
superseriesrec = '1'
seriesnumrec   = '1'
storylenrec    = '1'
ttyperec       = '1'

##################################################################
# Get user prefered fields
##################################################################
if form.has_key('title'):
	titlerec = form['title'].value
if form.has_key('author'):
	authorrec = form['author'].value
if form.has_key('copyright'):
	copyrightrec = form['copyright'].value
if form.has_key('series'):
	seriesrec = form['series'].value
if form.has_key('superseries'):
	superseriesrec = form['superseries'].value
if form.has_key('seriesnum'):
	seriesnumrec = form['seriesnum'].value
if form.has_key('storylen'):
	storylenrec = form['storylen'].value
if form.has_key('ttype'):
	ttyperec = form['ttype'].value

##################################################################
# Select target records to update and delete
##################################################################
if int(recno2) < int(recno1):
	targetID = int(recno2)
	deleteID = int(recno1)
	mergeto  = '2'
else:
	targetID = int(recno1)
	deleteID = int(recno2)
	mergeto  = '1'


##################################################################
# Make the SQL queries
##################################################################
myisfdb = ISFDB()
db = dbConnect()
db.select_db(DBASE)
myisfdb.SetDb(db)

query = "select * from titles where title_id = "+recno1
db.query(query)
result = db.store_result()
record1 = result.fetch_row()

query = "select * from titles where title_id = "+recno2
db.query(query)
result = db.store_result()
record2 = result.fetch_row()


##################################################################
# TITLE
##################################################################

print '<table cellpadding=0 width="90%" BGCOLOR="#FFFFFF">'
print '<tr align=left bgcolor="ececec">'
print '<td><b>Merge Record</b></td>' 
if mergeto == '1':
	print '<td>' +str(record1[0][TITLE_PUBID])+ '</td>'
	pubcontent = "update pub_content set title_id=%d where title_id=%d" % (record1[0][TITLE_PUBID], record2[0][TITLE_PUBID])
else:
	print '<td>' +str(record2[0][TITLE_PUBID])+ '</td>'
	pubcontent = "update pub_content set title_id=%d where title_id=%d" % (record2[0][TITLE_PUBID], record1[0][TITLE_PUBID])
print '</tr>'

Merge(db, mergeto, record1, record2, TITLE_TITLE,     "title_title",       titlerec)
Merge(db, mergeto, record1, record2, TITLE_YEAR,      "title_copyright",   copyrightrec)
Merge(db, mergeto, record1, record2, TITLE_SERIES,    "title_series",      seriesrec)
Merge(db, mergeto, record1, record2, TITLE_SERIESNUM, "title_seriesnum",   seriesnumrec)
Merge(db, mergeto, record1, record2, TITLE_STORYLEN,  "title_storylen",    storylenrec)
Merge(db, mergeto, record1, record2, TITLE_TTYPE,     "title_ttype",       ttyperec)

MergeAuthor(db, mergeto, record1, record2, authorrec)

Concat(db, mergeto, record1, record2, TITLE_XLATE, "translator", ";")

ConcatNote(db, mergeto, record1, record2, TITLE_SYNOP, "synopsis", " ")
ConcatNote(db, mergeto, record1, record2, TITLE_NOTE,  "note", " ")

print '</table>'


delstring = "delete from titles where title_id = "+str(deleteID)
print delstring
db.query(delstring)
print pubcontent
db.query(pubcontent)

print "<p>"
print "<b>Delete record:</b> " + str(deleteID)

print "<hr>"

#
# Close the HTML page
print "</body>\n"
print "</html>\n"

