#!_PYTHONLOC
#
#     (C) COPYRIGHT 2015-2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string
import MySQLdb
from isfdb import *
from isfdblib import *


def displayError(error_text):
        PrintPreSearch('Duplicate Finder for one or more Titles')
	PrintNavBar('edit/find_title_dups.cgi', 0)
        print '<h3>%s.</h3>' % error_text
        PrintPostSearch(0, 0, 0, 0, 0, 0)
        sys.exit(0)

        
if __name__ == '__main__':

	try:
                # Parse the list of arguments that was passed in
                arguments = sys.argv[1:]
                titles = []
                for argument in arguments:
                        title_id = int(argument)
                        title = SQLloadTitle(title_id)
                        if not title:
                                raise
                        titles.append(title_id)
	except:
		displayError("Missing or non-existing title ID")

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch('Duplicate Finder for one or more Titles')
	PrintNavBar('edit/find_title_dups.cgi', 0)

	print '<div id="HelpBox">'
	print '<b>Help on merging titles: </b>'
	print '<a href="http://%s/index.php/Editing:Merging_Titles">Editing:Merging_Titles</a><p>' % (WIKILOC)
	print '</div>'

	print """<h3>Note: Unlike the Duplicate Finder for author records, the Duplicate Finder for
                title records does not identify potential duplicates with different capitalization. 
                Also, be sure to check the title types and languages carefully before merging.</h3>"""
	print '<p><hr>'

        found = 0
        for title_id in titles:
                title = SQLloadTitle(title_id)
                if title[TITLE_TTYPE] != 'REVIEW':
                        found += CheckOneTitle(title)

	if not found:
		print '<h2>No duplicate candidates found.</h2>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)
