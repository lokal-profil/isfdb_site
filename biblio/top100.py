#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

	try:
		type = sys.argv[1]
	except:
		PrintHeader("Bad Argument")
		PrintNavbar('top100', 0, 0, 'top100.cgi', 0)
		PrintTrailer('top100', 0, 0)
		sys.exit(0)

	if type == 'novel':
		ttype = 'NOVEL'
		ltype = "Novels"
	elif type == 'short':
		ttype = 'SHORTFICTION'
		ltype = 'Shortfiction'
	else:
		PrintHeader("Bad Type")
		PrintNavbar('top100', 0, 0, 'top100.cgi', 0)
		PrintTrailer('top100', 0, 0)
		sys.exit(0)

	PrintHeader("Top 100 "+ltype)
	PrintNavbar('top100', 0, 0, 'top100.cgi', 0)

	print '<h3>Top 100 %s as voted by ISFDB users</h3>' % ltype
	query = """select t.title_id, t.title_title, t.title_copyright, AVG(v.rating)
                from titles t, votes v
                where t.title_id = v.title_id
                and t.title_ttype = '%s'
                group by t.title_id
                having COUNT(v.rating)>5
                order by AVG(v.rating) desc limit 100""" % ttype
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()

	print '<table class="generic_table">'
	print '<tr class="generic_table_header">'
	print '<th>Rank</th>'
	print '<th>Rating</th>'
	print '<th>Title</th>'
	print '<th>Year</th>'
	print '<th>Author(s)</th>'
	print '</tr>'
	counter = 1
	color = 1
	while record:
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
		print '<td>%d</td>' % counter
		print '<td>%2.2f</td>' % record[0][3]
		print '<td>%s</td>' % ISFDBLink('title.cgi', record[0][0], record[0][1])
		print '<td>%s</td>' % record[0][2][:4]
		authors = SQLTitleBriefAuthorRecords(int(record[0][0]))
		print '<td>'
		displayAuthorList(authors)
		print '</td>'
		print '</tr>'
		record = result.fetch_row()
		counter += 1
		color = color ^ 1

	print '</table>'
	print '<p>'

	PrintTrailer('top100', 0, 0)
