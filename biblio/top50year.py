#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2016   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.7 $
#     Date: $Date: 2016/08/09 22:19:41 $


import sys
import os
import string
from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

	PrintHeader('ISFDB - Top 50 Forthcoming Novels of Interest')
	PrintNavbar('stats', 0, 0, 'top50year.cgi', 0)

	print "<h3>The following forthcoming novels are those with the most interest as generated"
	print "by the users of the ISFDB.</h3>"
	print "<p>"

        query = """select title_views, title_title, title_id, title_copyright
                from titles where title_ttype='NOVEL' and title_views > 0
                and title_copyright>NOW() and YEAR(title_copyright)<(YEAR(CURDATE())+5)
                order by title_views desc limit 50"""

	db.query(query)
	result = db.store_result()
	record = result.fetch_row()

	print '<table>'
	print '<tr>'
	print '<th>Rank</th>'
	print '<th>Title</th>'
	print '<th>Author(s)</th>'
	print '<th>Date</th>'
	print '</tr>'
        bgcolor = 1
        title_count = 1
	while record:
                if bgcolor:
                        line = '<tr align=left class="table1">'
                else:
                        line = '<tr align=left class="table2">'
                line += '<td>%d</td>' % title_count
		line += '<td>%s</td>' % ISFDBLink('title.cgi', record[0][2], record[0][1])

		authors = SQLTitleBriefAuthorRecords(int(record[0][2]))
		author_count = 0
                line += '<td>'
		for author in authors:
			if author_count > 0:
				line += ', '
			line += ISFDBLink('ea.cgi', author[0], author[1])
			author_count += 1
		line += '</td>'

		line += '<td>%s</td>' % record[0][3]
                line += '</tr>'
		print line
		record = result.fetch_row()
                bgcolor ^= 1
                title_count += 1

	print "</table>"

	PrintTrailer('frontpage', 0, 0)
