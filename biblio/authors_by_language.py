#!_PYTHONLOC
#
#     (C) COPYRIGHT 2016-2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2017/06/24 16:20:37 $


import sys
import os
import string
from SQLparsing import *
from biblio import *

if __name__ == '__main__':

	PrintHeader('Authors by Working Language')
	PrintNavbar('authors_by_language', 0, 0, 'authors_by_language.cgi', 0)

        query = "select author_language, count(*) cnt from authors group by author_language"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	rows = []
	total = 0
	while record:
		lang_id = record[0][0]
                if lang_id == 0:
                        language = 'Undefined'
                elif not lang_id:
                        language = 'To Be Assigned'
                else:
                        language = LANGUAGES[lang_id]
		lang_count = -record[0][1]
		total += record[0][1]
		row = (lang_count, language)
		rows.append(row)
		record = result.fetch_row()

        print '<h4>Total authors: %d</h4>' % total
        print '<p>'
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th>Working Language</th>'
        print '<th>Count</th>'
        print '<th>Percent</th>'
        print '</tr>'
        bgcolor = 1
        for row in sorted(rows):
                print '<tr class="table%d">' % bgcolor
                count = -row[0]
                language = row[1]
                print '<td>%s</td>' % language
                print '<td>%d</td>' % count
                print '<td>% 3.2f</td>' % (count*100/float(total))
                print '</tr>'
                bgcolor ^= 1
        print '</table>'

	PrintTrailer('frontpage', 0, 0)
