#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
from SQLparsing import *
from biblio import *
from common import PrintAllAuthors
from library import convertYear
import operator

def doError():
	PrintHeader("Highest Ranked Titles by Awards and Nominations")
	PrintNavbar('top', 0, 0, 'most_popular.cgi', 0)
        print '<h3>Bad argument</h3>'
	PrintTrailer('top', 0, 0)
        sys.exit(0)


def printTableBody(final, span):
	bgcolor = 0
        eligible = 0
        for record in sorted(final, reverse=True):
                score = record[0]
                year = record[1]
                title_id = record[2]
                print '<tr align=left class="table%d">' % (bgcolor+1)
                print '<td>%d</td>' % (eligible+1)
                print '<td>%d</td>' % score
                # Display the year of the title unless we are displaying the data for just one year
                if span != 'year':
                        display_year = unicode(year)
                        if display_year == '0':
                                display_year = '0000'
                        print '<td>%s</td>' % convertYear(display_year)
                # Retrieve this record's title and type
                title_data = SQLloadTitle(title_id)
                print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_data[TITLE_TITLE])
                print '<td>%s</td>' % title_data[TITLE_TTYPE]
                print '<td>'
                PrintAllAuthors(title_id)
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
                        title_type = 'Titles'
                elif type == 1:
                        title_type = 'Novels'
                elif type == 2:
                        title_type = 'Short Fiction'
                elif type == 3:
                        title_type = 'Collections'
                elif type == 4:
                        title_type = 'Anthologies'
                elif type == 5:
                        title_type = 'Non-Fiction'
                elif type == 6:
                        title_type = 'Other Title Types'
                else:
                        raise
        except:
                doError()

        try:
                span = sys.argv[2]
                if span == 'all':
                        header = 'Highest Ranked %s of All Time' % title_type
                elif span == 'decade':
                        decade = int(sys.argv[3])
                        header = 'Highest Ranked %s of the %ds' % (title_type, decade)
                elif span == 'year':
                        display_year = int(sys.argv[3])
                        header = 'Highest Ranked %s published in %s' % (title_type, display_year)
                elif span == 'pre1950':
                        header = 'Highest Ranked %s Prior to 1950' % title_type
                else:
                        raise
        except:
                doError()

	PrintHeader(header)
	PrintNavbar('top', 0, 0, 'most_popular.cgi', 0)

        titles = TitlesSortedByAwards(type, span, decade, display_year)

        if not titles:
                print '<h3>No awards or nominations for the specified period</h3>'
        else:
                print '<b>Note</b>: Some recent awards are yet to be integrated into the database.<br>'
                print '<b>Scoring</b>: Wins are worth 50 points, nominations and second places are worth 35 points. For polls, third and lower places are worth (33-poll position) points.'
                # Print the table headers        
                print '<table class="seriesgrid">'
                print '<tr>'
                print '<th>Place</th>'
                print '<th>Score</th>'
                if span != 'year':
                        print '<th>Year</th>'
                print '<th>Title</th>'
                print '<th>Type</th>'
                print '<th>Authors</th>'
                print '</tr>'
                printTableBody(titles, span)
                print '</table>'
	
	PrintTrailer('top', 0, 0)

