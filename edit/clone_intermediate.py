#!_PYTHONLOC
#
#     (C) COPYRIGHT 2015-2018   Ahasuerus
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
from library import *

def DisplayError(error):
        PrintPreSearch("Clone Publication")
        PrintNavBar("edit/clonecover.cgi", 0)
        print '<h3>Error: %s</h3>' % error
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
		pub_id = int(sys.argv[1])
		pub_data = SQLGetPubById(pub_id)
		if not pub_data:
                        raise
	except:
                DisplayError("Missing or invalid publication ID")

        if pub_data[PUB_CTYPE] in ('MAGAZINE', 'FANZINE'):
                DisplayError("Magazines and Fanzines can't be cloned at this time")

	PrintPreSearch("Clone Publication - %s" % pub_data[PUB_TITLE])
	PrintNavBar("edit/clonecover.cgi", pub_id)

	print '<div id="HelpBox">'
        print '<a href="http://%s/index.php/Help:Screen:ClonePub">Help on cloning publications</a><p>' % (WIKILOC)
	print '</div>'

	print '<form class="topspace" id="data" METHOD="POST" ACTION="/cgi-bin/edit/clonepub.cgi">'
	print '<table>'
	if pub_data[PUB_IMAGE]:
                print '<tr class="scan">'
                print '<td><b>Current image:</b></td>'
                if "|" in pub_data[PUB_IMAGE]:
                        image = pub_data[PUB_IMAGE].split("|")[0]
                        link = pub_data[PUB_IMAGE].split("|")[1]
                else:
                        image = pub_data[PUB_IMAGE]
                        link = pub_data[PUB_IMAGE]
                print '<td><a href="%s"><img src="%s" alt="picture" class="scan"></a></td>' % (link, image)
                print '</tr>'

	print '<tr>'
        print '<td><b>Reuse COVERART title(s) and image URL?</b></td>'
        print '<td><input type="checkbox" NAME="ReuseCoverArt" value="on" checked></td>'
	print '</tr>'
	
	print '<tr>'
        print '<td><b>Reuse INTERIORART titles?</b></td>'
        print '<td><input type="checkbox" NAME="ReuseInteriorArt" value="on" checked></td>'
	print '</tr>'
	
	print '<tr>'
        print '<td><b>Reuse page numbers?</b></td>'
        print '<td><input type="checkbox" NAME="ReusePageNumbers" value="on" checked></td>'
	print '</tr>'

	print '<tr>'
        print '<td><b>Reuse external IDs?</b></td>'
        print '<td><input type="checkbox" NAME="ReuseExternalIDs" value="on"></td>'
	print '</tr>'

	print '</table>'
	print '<p>'
	print '<input NAME="CloneTo" VALUE="%d" TYPE="HIDDEN">' % pub_id
	print '<input TYPE="SUBMIT" VALUE="Clone Publication">'
	print '</form>'

	PrintPostSearch(tableclose=False)
