#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2009   Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node

debug = 1


def dropCanonicalPubs(db, DropId):
	delete = "delete from canonical_author where title_id='%d'" % (int(DropId))
	print "<li> ", delete
	if debug == 0:
		db.query(delete)

def dropPubPubs(db, KeepId, DropId):
	update = "update pub_content set title_id=%d where title_id=%d" % (int(KeepId), int(DropId))
	print "<li> ", update
	if debug == 0:
		db.query(update)

######################

def deletePub(db, id):
	delete = "delete from pubs where pub_id='%d'" % (int(id))
	print "<li> ", delete
	if debug == 0:
		db.query(delete)

def movePubColumn(db, column, keep, drop):
	query = "select %s from pubs where pub_id='%d'" % (column, int(drop))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	value = record[0][0]
	update = "update pubs set %s='%s' where pub_id='%d'" % (column, db.escape_string(str(value)), int(keep))
	print "<li> ", update
	if debug == 0:
		db.query(update)

########################################################################

def PubMerge(db, recno, doc):
	merge = doc.getElementsByTagName('PubMerge')
	KeepId = GetElementValue(merge, 'KeepId')
	DropId = GetElementValue(merge, 'DropId')

	print "<li> ", "KeepId: ", KeepId
	print "<li> ", "DropId: ", DropId

	id = GetElementValue(merge, 'Title')
	if id and id != KeepId:
		movePubColumn(db, 'pub_title', KeepId, DropId)

	id = GetElementValue(merge, 'Year')
	if id and id != KeepId:
		movePubColumn(db, 'pub_year', KeepId, DropId)

	id = GetElementValue(merge, 'Tag')
	if id and id != KeepId:
		movePubColumn(db, 'pub_tag', KeepId, DropId)

	id = GetElementValue(merge, 'Isbn')
	if id and id != KeepId:
		movePubColumn(db, 'pub_isbn', KeepId, DropId)

	id = GetElementValue(merge, 'Price')
	if id and id != KeepId:
		movePubColumn(db, 'pub_price', KeepId, DropId)

	id = GetElementValue(merge, 'Publisher')
	if id and id != KeepId:
		movePubColumn(db, 'pub_publisher', KeepId, DropId)

	id = GetElementValue(merge, 'Binding')
	if id and id != KeepId:
		movePubColumn(db, 'pub_ptype', KeepId, DropId)

	id = GetElementValue(merge, 'Type')
	if id and id != KeepId:
		movePubColumn(db, 'pub_ctype', KeepId, DropId)

	# AUTHORS
	# canonical authors is still messed up
	dropCanonicalPubs(db, DropId)
	dropPubPubs(db, KeepId, DropId)
	deletePub(db, DropId)


if __name__ == '__main__':

	PrintPreMod('Pub Merge - SQL Statements')
        PrintNavBar()

	try:
		recno = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

	xml = SQLloadXML(recno)
	doc = minidom.parseString(XMLunescape2(xml))
	merge = doc.getElementsByTagName('PubMerge')
	if merge:
		PubMerge(db, recno, doc)

		submitter = GetElementValue(merge, 'Submitter')
        	markIntegrated(db, recno)

	print "</ul>"
	print "<hr>"
	print '[<a href="http:/' +HTFAKE+ '/mod/list.cgi?N">Submission List</a>]'
	print "<hr>"


	PrintPostMod()
