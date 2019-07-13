#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2019   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from authorClass import *
from library import *
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        PrintPreMod('Make Alternate Name - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
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

	submitter = ''
	try:
		xml = SQLloadXML(submission)
		doc = minidom.parseString(XMLunescape2(xml))
        	if doc.getElementsByTagName('MakePseudonym'):
			merge = doc.getElementsByTagName('MakePseudonym')
        		Record = GetElementValue(merge, 'Record')
        		submitter = GetElementValue(merge, 'Submitter')
       			if TagPresent(merge, 'Parent'):
        			parent = GetElementValue(merge, 'Parent')
				insert = "insert into pseudonyms(author_id, pseudonym) values(%d,%d)" % (int(parent), int(Record))
                                print "<li> ", insert
                                if debug == 0:
                                        db.query(insert)
                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission)
	except:
		submitter = 'unknown'

	print '[<a href="http:/' +HTFAKE+ '/ea.cgi?%d">View Canonical Name</a>]' % int(parent)
	print '[<a href="http:/' +HTFAKE+ '/ea.cgi?%d">View Alternate Name</a>]' % int(Record)
        print "<p>"

        PrintPostMod(0)
