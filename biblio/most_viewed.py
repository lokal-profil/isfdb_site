#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2016   Ahasuerus
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
	print '<th>Authors</th>'
	print '</tr>'

        query = "select @rownum:=@rownum+1, title_views, title_id, title_title from titles, "
        query += "(SELECT @rownum:=0) as r where title_ttype='%s' order by title_views desc limit 300" % (db.escape_string(type))

	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	bgcolor = 0
	while record:
                rank = record[0][0]
                views = record[0][1]
                title_id = record[0][2]
                title_title = record[0][3]
                print '<tr align=left class="table%d">' % (bgcolor+1)
                print '<td>%d</d>' % rank
                print '<td>%d</td>' % views
                print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title)
                print '<td>'
                PrintAllAuthors(title_id)
                print '</td>'
                print '</tr>'
                bgcolor = bgcolor ^ 1
        	record = result.fetch_row()
        print '</table>'
        

if __name__ == '__main__':
        if len(sys.argv) < 2:
                PrintHeader("Most-Viewed Data Since 2005")
                PrintNavbar('top', 0, 0, 'most_viewed.cgi', 0)
                print "<h3>No parameter passed</h3>"
                sys.exit(0)

        if sys.argv[1] == 'authors':
                query = "select @rownum:=@rownum+1, author_canonical, author_views, author_id from authors, (SELECT @rownum:=0) as r order by author_views desc limit 500"
                headers = ('Rank', 'Views', 'Author')
                PrintListPage('Most Viewed Authors Since 2005', 'most_viewed', 0, 0, 'most_viewed.cgi', 0, query, AuthorsDisplayFunc, headers)
                sys.exit(0)

        if sys.argv[1] == 'novels':
                header = 'Novels'
        elif sys.argv[1] == 'short':
                header = 'Short Fiction'
        else:
                header = 'Data'

	PrintHeader("Most-Viewed "+ header + " Since 2005")
	PrintNavbar('top', 0, 0, 'most_viewed.cgi', 0)

        if sys.argv[1] == 'novels':
                printTable('NOVEL')
        elif sys.argv[1] == 'short':
                printTable('SHORTFICTION')
        else:
                print '<h3>Bad Argument</h3>'
	PrintTrailer('top', 0, 0)
