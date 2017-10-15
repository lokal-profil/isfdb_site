#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2016/08/09 22:19:41 $


import string
import sys
from SQLparsing import *
from biblio import *
from common import PrintAllAuthors
import operator

def doError():
	PrintHeader("Highest Ranked Authors by Awards and Nominations")
	PrintNavbar('top', 0, 0, 'popular_authors.cgi', 0)
        print '<h3>Bad argument</h3>'
	PrintTrailer('top', 0, 0)
        sys.exit(0)


def printTableBody(author_dict):
	bgcolor = 0
        eligible = 0
        for author_id in sorted(author_dict, key=author_dict.get, reverse=True):
                score = author_dict[author_id]
                print '<tr align=left class="table%d">' % (bgcolor+1)
                print '<td>%d</td>' % (eligible+1)
                print '<td>%d</td>' % score
                print '<td>'
                author_data = SQLloadAuthorData(author_id)
                print ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author_data[AUTHOR_CANONICAL])
                print '</td>'
                print '</tr>'
                bgcolor = bgcolor ^ 1
                eligible += 1
                # Once we have displayed 500 rows, quit
                if eligible > 499:
                        return


if __name__ == '__main__':

        display_year = 0
        decade = 0
        try:
		type = int(sys.argv[1])
		if type == 0:
                        author_type = 'Authors and Editors'
		elif type == 1:
                        author_type = 'Novel Authors'
                elif type == 2:
                        author_type = 'Short Fiction Authors'
                elif type == 3:
                        author_type = 'Collection Authors'
                elif type == 4:
                        author_type = 'Anthology Editors'
                elif type == 5:
                        author_type = 'Non-Fiction Authors'
                elif type == 6:
                        author_type = 'Other Title Types Authors'
                else:
                        raise
        except:
                doError()

        try:
                span = sys.argv[2]
                if span == 'all':
                        header = 'Highest Ranked %s of All Time' % author_type
                elif span == 'decade':
                        decade = int(sys.argv[3])
                        header = 'Highest Ranked %s of the %ds' % (author_type, decade)
                elif span == 'pre1950':
                        header = 'Highest Ranked %s Prior to 1950' % author_type
                else:
                        raise
        except:
                doError()

	PrintHeader(header)
	PrintNavbar('top', 0, 0, 'popular_authors.cgi', 0)

        titles = TitlesSortedByAwards(type, span, decade, display_year)
        if not titles:
                print '<h3>No %s with awards or nominations for the specified period</h3>' % author_type
                PrintTrailer('top', 0, 0)
                sys.exit(0)

        # Initialize the dictionary which will list scores by title_id
        title_dict = {}
        # Build the SQL IN clause which will be used to find authors for the identified titles
        first = 1
        for title_data in titles:
                title_id = str(title_data[2])
                title_dict[title_id] = title_data[0]
                if first:
                        in_clause = title_id
                        first = 0
                else:
                        in_clause += ',' + str(title_id)

        query = "select title_id, author_id from canonical_author where ca_status=1 and title_id in (%s)" % in_clause
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
        author_dict = {}
	while record:
                title_id = str(record[0][0])
                author_id = record[0][1]
                score = title_dict[title_id]
                author_dict[author_id] = author_dict.get(author_id, 0) + score
        	record = result.fetch_row()

        print '<b>Note</b>: Some recent awards are yet to be integrated into the database. Only title-based awards are used for ranking purposes.<br>'
        print '<b>Scoring</b>: Wins are worth 50 points, nominations and second places are worth 35 points. For polls, third and lower places are worth (33-poll position) points.'
        # Print the table headers        
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th>Place</th>'
        print '<th>Score</th>'
        if type != 4:
                print '<th>Author</th>'
        else:
                print '<th>Editor</th>'
        print '</tr>'
        printTableBody(author_dict)
        print '</table>'
	
	PrintTrailer('top', 0, 0)

