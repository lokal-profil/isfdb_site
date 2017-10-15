#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2017   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.8 $
#     Date: $Date: 2017/03/14 00:09:37 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *


if __name__ == '__main__':

	try:
		pub_id = int(sys.argv[1])
		pub_data = SQLGetPubById(pub_id)
		if not pub_data:
                        raise
	except:
                PrintPreSearch("Export Content")
		PrintNavBar("edit/exportcontent.cgi", 0)
		print '<h3>Missing or non-existent publication ID</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	PrintPreSearch("Export Content - %s" % pub_data[PUB_TITLE])
	PrintNavBar("edit/exportcontent.cgi", pub_id)

	print '<div id="HelpBox">'
        print '<a href="http://%s/index.php/Help:Screen:ExportContent">Help on exporting content</a><p>' % (WIKILOC)
	print '</div>'

	print "Enter the publication ID/record number you would like to export into:"
	print "<p>"

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/clonecontent.cgi">'
	print '<table>'
	print '<tr>'
	print '<td><b>Export Into:</b></td>'
	print '<td><INPUT NAME="ExportTo" id="ExportTo" SIZE="20"></td>'
	print '</tr>'

	print '<tr>'
        print '<td><b>Include COVERART title(s)?</b></td>'
        print '<td><input type="checkbox" NAME="IncludeCoverArt" value="on" checked></td>'
	print '</tr>'
	
	print '<tr>'
        print '<td><b>Include INTERIORART titles?</b></td>'
        print '<td><input type="checkbox" NAME="IncludeInteriorArt" value="on" checked></td>'
	print '</tr>'

	print '<tr>'
        print '<td><b>Include page numbers?</b></td>'
        print '<td><input type="checkbox" NAME="IncludePages" value="on" checked></td>'
	print '</tr>'
	print '</table>'
	print '<p>'
	print '<input NAME="ExportFrom" VALUE="%d" TYPE="HIDDEN">' % pub_id
	print '<input TYPE="SUBMIT" VALUE="Export Content">'
	print '</form>'

	PrintPostSearch(tableclose=False)
