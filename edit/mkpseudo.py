#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2013   Al von Ruff, Ahasuerus and Bill Longley
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

if __name__ == '__main__':

	try:
		author_id = int(sys.argv[1])
                author = SQLloadAuthorData(author_id)
                if not author:
                        raise
	except:
		PrintPreSearch("Make/Remove a Pseudonym")
		PrintNavBar("edit/mkpseudo.cgi", 0)
		print '<h3>Missing or invalid author ID</h3>'
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Make/Remove a Pseudonym - %s" % author[AUTHOR_CANONICAL])
	PrintNavBar("edit/mkpseudo.cgi", author_id)

	print '<div id="HelpBox">'
        print "<b>Help on creating pseudonyms: </b>"
        print '<a href="http://%s/index.php/Help:Screen:MakePseudonym">Help:Screen:MakePseudonym</a><p>' % (WIKILOC)
	print '</div>'

	print "Making/removing pseudonyms for <b>%s</b>" % author[AUTHOR_CANONICAL]
	print "<br>"

        #Retrieve a list of current canonical authors for this pseudonym
	parents = SQLgetActualFromPseudo(author_id)
	if parents:
		print 'This name is currently labeled as a pseudonym for the following author(s):'
		print '<table border="1">'
                for parent in parents:
        		print '<tr>'
                        print "<form id='data'"
                        print 'METHOD="POST" ACTION="/cgi-bin/edit/submitrempseudo.cgi">'
                        #Retrieve author details for this parent canonical author
                        parent_data = SQLgetAuthorData(parent[0])
                        print '<td>'
                        print '<a href="http:/%s/ea.cgi?%s">%s</a>' % (HTFAKE, parent_data[AUTHOR_ID], parent[0])
                        print '</td>'
                        print '<td>'
                	print '<input NAME="author_id" VALUE="%d" TYPE="HIDDEN">' % (author_id)
                        print '<input NAME="parent_id" VALUE="%s" TYPE="HIDDEN">' % (parent_data[AUTHOR_ID])
                        print '<input TYPE="SUBMIT" VALUE="Remove">'
                        print '</td>'
		        print '</tr>'
		        print '<tr>'
                        print '<td>'
                	print "<b>Note to Moderator: </b>"
                	print "<br><TEXTAREA name=\"mod_note\" ROWS=1 COLS=45></TEXTAREA>"
                        print '</td>'
                        print '</form>'
		        print '</tr>'
                print '</table>'

	print '<p><hr size="3" />'

	##################################################################
	# Section 1
	##################################################################
	print "Enter the name or the record number of the new parent author below."
	print "The author must already exist in the database."
	print "<p>"

	print "<form id='data' METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitmkpseudo.cgi\">"
	print '<b>Parent Record #:</b>  <INPUT NAME="ParentRec" SIZE=16>'
	print '<br><b>Parent Name:</b>  <INPUT NAME="ParentName" id="ParentName" SIZE=20>'
	print "<br><b>Note to Moderator: </b>"
	print "<br><TEXTAREA name=\"mod_note\" ROWS=4 COLS=45></TEXTAREA>"
	print "<p>"
	print "<input NAME=\"author_id\" VALUE=\"%d\" TYPE=\"HIDDEN\">" % author_id
	print "<input TYPE=\"SUBMIT\" VALUE=\"Submit Data\">"
	print "</form>"

	print "<p>"
	print "<hr>"
	print "<p>"

	PrintPostSearch(0, 0, 0, 0, 0)
