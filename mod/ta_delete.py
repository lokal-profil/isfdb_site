#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2019   Al von Ruff, Bill Longley and Ahasuerus
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
from isfdblib import *
from common import *
from titleClass import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        PrintPreMod('Title Delete - SQL Statements')
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

	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('TitleDelete'):
		merge = doc.getElementsByTagName('TitleDelete')
        	Record = GetElementValue(merge, 'Record')
                title = titles(db)
                title.load(Record)
                success = title.delete()
                if not success:
                        print """<h3>Error: Title couldn't be deleted because
                        it's associated with a publication. You will need to
                        hard reject this submission</h3>"""
                else:
                        submitter = GetElementValue(merge, 'Submitter')
                        markIntegrated(db, submission)

	print "<p>"

	PrintPostMod(0)
