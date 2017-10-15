#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006   Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2008/04/24 10:31:20 $

	
import cgi
import string
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
	
def escape_quotes(input):
        if input:
                return string.strip(repr(input+'"')[1:-2])
        else:
                return ''

	
if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
        PrintPreMod("ISFDB Control Panel Submission")
        PrintNavBar()
	
	##################################################################
	# Get database record
	##################################################################
        query = "select * from metadata"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()

        oldVersion = record[0][0]
        oldDbOnline = record[0][2]
        oldEditOnline = record[0][3]

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

	print '<pre>'
	changes = 0
        if form.has_key('VERSION'):
		newVersion = escape_quotes(form['VERSION'].value)
		if newVersion != oldVersion:
			query = "update metadata set metadata_schemaversion='%s'" % newVersion
			print query
        		db.query(query)
			changes += 1

        if form.has_key('ONLINE'):
		newDbOnline = int(form['ONLINE'].value)
		if newDbOnline != oldDbOnline:
			query = "update metadata set metadata_dbstatus='%d'" % newDbOnline
			print query
        		db.query(query)
			changes += 1

        if form.has_key('EDITING'):
		newEditOnline = int(form['EDITING'].value)
		if newEditOnline != oldEditOnline:
			query = "update metadata set metadata_editstatus='%d'" % newEditOnline
			print query
        		db.query(query)
			changes += 1

	print "%d changes made." % changes
	print '</pre>'

	PrintPostMod()
