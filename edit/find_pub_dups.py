#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from isfdb import *
from isfdblib import *


if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        pub_data = SQLGetPubById(pub_id)
        if not pub_data:
                SESSION.DisplayError('Record Does Not Exist')
        titles = SQLloadTitlesXBT(pub_id)
        if not titles:
                SESSION.DisplayError('Publication Record Contains No Titles')

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
