#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.11 $
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
		PrintPreSearch("Import Content")
		PrintNavBar("edit/importcontent.cgi", 0)
		print '<h3>Missing or invalid publication ID</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	PrintPreSearch("Import Content - %s" % pub_data[PUB_TITLE])
	PrintNavBar("edit/importcontent.cgi", pub_id)

	print '<div id="HelpBox">'
        print '<a href="http://%s/index.php/Help:Screen:ImportContent">Help on importing content</a><p>' % (WIKILOC)
	print '</div>'

	print '<hr class="divider">'
	print '<p>'
	print '<h2>Option 1</h2>'
	print "<p>"

	print "Enter the publication ID/record number you would like to import from:"

	print '<form class="topspace" id="data" METHOD="POST" ACTION="/cgi-bin/edit/clonecontent.cgi">'
	print '<table>'
	
	print '<tr>'
	print '<td><b>Import From:</b></td>'
	print '<td><INPUT NAME="ExportFrom" id="ExportFrom" SIZE="20"></td>'
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
	
	print '<input NAME="ExportTo" VALUE="%d" TYPE="HIDDEN">' % pub_id
	print '<input TYPE="SUBMIT" VALUE="Import Content">'
	print '</form>'

	print '<hr class="divider">'
	print '<p>'
	print '<h2>Option 2</h2>'
	print "<p>"

	print "<p>Enter the title ID(s) you would like to import. Use commas as record separators:"

	print '<form class="topspace" id="singledata" METHOD="POST" ACTION="/cgi-bin/edit/clonecontent.cgi">'
	print '<table>'
	print '<tr>'
	print '<td><b>Individual Titles:</b></td>'
	print '<td><INPUT NAME="ImportTitles" id="ExportTitles" SIZE="20"></td>'
	print '</tr>'
	print '</table>'
	print '<p>'
	print '<input NAME="ExportTo" VALUE="%d" TYPE="HIDDEN">' % pub_id
	print '<input TYPE="SUBMIT" VALUE="Import Titles">'
	print '</form>'

	PrintPostSearch(tableclose=False)
