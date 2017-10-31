#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff and Ahasuerus
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
from library import *
from SQLparsing import *

def printreference(record, index):
        if record:
        	print '<tr>'
                print '<td>%d<input name="ref_id%d" size="5" value="%s" type="HIDDEN"></td>' % (record[0], record[0], record[0])
                print '<td><input name="ref_label%d" size="15" value="%s" READONLY class="displayonly"></td>' % (record[0], record[1])
                print '<td><input name="ref_fullname%d" size="60" value="%s" READONLY class="displayonly"></td>' % (record[0], record[2])
##		if record[3]:
##                print '<td><input name="ref_pub%d" size="5" value="%s" READONLYclass="displayonly"></td>' % (record[0], record[3])
##		else:
##                	print '<td><input name="ref_pub%d" size="5" READONLY class="displayonly"></td>' % (record[0])
##		if record[4]:
                print '<td><input name="ref_url%d" size="60" value="%s" READONLY class="displayonly"></td>' % (record[0], record[4])
##		else:
##                	print '<td><input name="ref_url%d" size="15" READONLY class="displayonly"></td>' % (record[0])
        else:
        	print '<tr>'
                print '<td>%d<input name="ref_id%d" value="%d" size="5" type="HIDDEN"></td>' % (index, index, index)
                print '<td><input name="ref_label%d" size="15" READONLY class="displayonly"></td>' % (index)
                print '<td><input name="ref_fullname%d" size="60" READONLY class="displayonly"></td>' % (index)
##                print '<td><input name="ref_pub%d" size="5" READONLY class="displayonly"></td>' % (index)
                print '<td><input name="ref_url%d" size="60" READONLY class="displayonly"></td>' % (index)
        print '</tr>'

if __name__ == '__main__':

	PrintPreMod("ISFDB Bibliographic Reference Table Editor")
	PrintNavBar()

	query = "select * from reference"
	db.query(query)
	result = db.store_result()

##	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/mod/submitref.cgi">'

        print '<h2>Bibliographic References</h2>'
        print 'Editing temporarily disabled.<hr>'
##	print "WARNING: While you may modify the label, title, url, and publication id, do not change"
##	print "the order of the entries. A book's verification information is tied to those reference"
##	print "numbers. Changing the order would cause a book to have different verficiations.<hr>"
        print '<table border="0" id="metadata">'
        print '<tbody id="pubBody">'

	print '<tr>'
	print '<th>ID</th>'
	print '<th>Label</th>'
	print '<th>Full Title</th>'
##	print '<th>Pub Id</th>'
	print '<th>URL</th>'
	print '</tr>'

	index = 1
        record = result.fetch_row()
	while record:
		printreference(record[0], record[0][0])
		index = int(record[0][0]) + 1
        	record = result.fetch_row()

	counter = 0
	while counter < 5:
		printreference(0, index)
		counter += 1
		index += 1

        print '</tbody>'
##	print '<hr>'
##	print '<input TYPE="SUBMIT" VALUE="Submit Data">'
##	print '</form>'

	PrintPostMod()

