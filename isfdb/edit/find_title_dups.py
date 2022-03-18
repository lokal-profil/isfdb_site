#!_PYTHONLOC
#
#     (C) COPYRIGHT 2015-2021   Ahasuerus
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

        if not SESSION.parameters:
                SESSION.DisplayError('Record Does Not Exist')
        titles = []
        for counter, parameter in enumerate(SESSION.parameters):
                title_id = SESSION.Parameter(counter, 'int')
                title = SQLloadTitle(title_id)
                if not title:
                        SESSION.DisplayError('Record Does Not Exist')
                titles.append(title_id)

	PrintPreSearch('Duplicate Finder for one or more Titles')
	PrintNavBar('edit/find_title_dups.cgi', 0)

	print '<div id="HelpBox">'
	print '<b>Help on merging titles: </b>'
	print '<a href="%s://%s/index.php/Help:How to merge titles">Help:How to merge titles</a><p>' % (PROTOCOL, WIKILOC)
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
