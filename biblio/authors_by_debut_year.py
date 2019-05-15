#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2018   Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *

if __name__ == '__main__':

        header = 'Authors By Debut Year'
        try:
                year = int(sys.argv[1])
                if year > 1899:
                        header += ' - %d' % year
                else:
                        header += ' - Prior to 1900'
                        year = 0
        except:
                year = 0
	PrintHeader(header)
	PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        print '<h3>Includes authors with at least 6 novels, short fiction, poems or collections:</h3>'
	print '<table class="generic_table">'
	print '<tr align=left class="table1">'
	print '<th>Debut Year</th>'
	print '<th>Author</th>'
	print '<th>Number of Titles</th>'
	print '</tr>'

        if year:
                year_selector = '= %d' % year
        else:
                year_selector = '< 1900'
        query = """select ad.debut_year, ad.author_id, a.author_canonical, ad.title_count
                from authors_by_debut_date ad, authors a
                where ad.debut_year %s
                and ad.author_id = a.author_id
                order by debut_year, a.author_lastname, a.author_canonical""" % db.escape_string(year_selector)
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
	color = 0
	while record:
                debut_year = record[0][0]
                author_id = record[0][1]
                author_name = record[0][2]
                title_count = record[0][3]
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
		print '<td>%s</td>' % debut_year
		print '<td>%s</td>' % ISFDBLink('ea.cgi', author_id, author_name)
		print '<td>%d</td>' % title_count
		print '</tr>'
		color = color ^ 1
                record = result.fetch_row()
	print '</table><p>'

	PrintTrailer('frontpage', 0, 0)
