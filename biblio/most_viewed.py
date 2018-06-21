#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2018   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *


def printTable(type):
        # Print the table headers        
	print '<table class="seriesgrid">'
	print '<tr>'
	print '<th>Rank</th>'
	print '<th>Views</th>'
	print '<th>Title</th>'
	print '<th>Year</th>'
	print '<th>Authors</th>'
	print '</tr>'

        query = """select @rownum:=@rownum+1, title_views, title_id, title_title, title_copyright
                from titles, (SELECT @rownum:=0) as r
                where title_ttype='%s'
                order by title_views
                desc limit 500""" % (db.escape_string(type))

	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	bgcolor = 0
	while record:
                rank = record[0][0]
                views = record[0][1]
                title_id = record[0][2]
                title_title = record[0][3]
                title_year = convertYear(record[0][4])
                print '<tr align=left class="table%d">' % (bgcolor+1)
                print '<td>%d</d>' % rank
                print '<td>%d</td>' % views
                print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                print '<td>%s</td>' % title_year
                print '<td>'
                PrintAllAuthors(title_id)
                print '</td>'
                print '</tr>'
                bgcolor = bgcolor ^ 1
        	record = result.fetch_row()
        print '</table>'
        

if __name__ == '__main__':

        try:
                report_type = sys.argv[1]
                if report_type not in ('authors', 'novels', 'short'):
                        raise
        except:
                PrintHeader('Most-Viewed Data Since 2005')
                PrintNavbar('top', 0, 0, 'most_viewed.cgi', 0)
                print '<h3>Invalid parameter</h3>'
                sys.exit(0)

        if report_type == 'authors':
                query = """select @rownum:=@rownum+1, author_canonical, author_views, author_id
                from authors, (SELECT @rownum:=0) as r
                order by author_views desc
                limit 500"""
                headers = ('Rank', 'Views', 'Author')
                PrintListPage('Most Viewed Authors Since 2005', 'most_viewed', 0, 0, 'most_viewed.cgi', 0, query, AuthorsDisplayFunc, headers)
                sys.exit(0)

        if report_type == 'novels':
                header = 'Novels'
        else:
                header = 'Short Fiction'

	PrintHeader("Most-Viewed %s Since 2005" % header)
	PrintNavbar('top', 0, 0, 'most_viewed.cgi', 0)

        if report_type == 'novels':
                printTable('NOVEL')
        else:
                printTable('SHORTFICTION')
	PrintTrailer('top', 0, 0)
