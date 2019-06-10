#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2019   Ahasuerus
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
        PrintPreSearch('Duplicate Finder for a Publication')
	PrintNavBar('edit/find_pub_dups.cgi', 0)
        print '<h3>%s.</h3>' % error_text
        PrintPostSearch(0, 0, 0, 0, 0, 0)
        sys.exit(0)

        
if __name__ == '__main__':

	try:
		pub_id = int(sys.argv[1])
		pub_data = SQLGetPubById(pub_id)
                titles = SQLloadTitlesXBT(pub_id)
                if not titles:
                        raise
	except:
		displayError("Missing or non-existing publication ID")

	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch('Duplicate Finder for %s' % pub_data[PUB_TITLE])
	PrintNavBar('edit/find_pub_dups.cgi', pub_id)

	print '<div id="HelpBox">'
	print '<b>Help on merging titles: </b>'
	print '<a href="http://%s/index.php/Editing:Merging_Titles">Editing:Merging_Titles</a><p>' % (WIKILOC)
	print '</div>'

	print '<h3>Note: Unlike the Duplicate Finder for author records, the Duplicate Finder for \
                publication records does not identify potential duplicates with different capitalization. \
                Also, be sure to check the title types and languages carefully before merging.</h3>'
	print '<p>'
	print '<hr>'

        found = 0

        for title in titles:
                if title[TITLE_TTYPE] != 'REVIEW':
                        found += CheckOneTitle(title)

	if not found:
		print '<h2>No duplicate candidates found.</h2>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)
