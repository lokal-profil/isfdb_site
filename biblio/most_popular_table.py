#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2014/03/09 21:12:16 $


import string
import sys
from SQLparsing import *
from biblio import *


def ErrorBox(message):
	PrintHeader("Titles Ranked by Awards and Nominations")
	PrintNavbar('top', 0, 0, 'most_popular_table.cgi', 0)
        print '<div id="ErrorBox">'
        print "<h3>%s.</h3>" % (message)
        print '</div>'
        PrintTrailer('most_popular_table', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

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
                ErrorBox("Invalid title type")

	PrintHeader("%s Ranked by Awards and Nominations" % title_type)
	PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        print '<h3><a href="http:/%s/most_popular.cgi?%d+all">Highest Ranked %s of All Time</a></h3>' % (HTFAKE, type, title_type)
        print '<h3><a href="http:/%s/most_popular.cgi?%d+pre1950">Highest Ranked %s Prior to 1950</a></h3>' % (HTFAKE, type, title_type)

        print '<h3>Highest Ranked %s Since 1950 by Decade and Year</h3>' % title_type
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th>Decade</th>'
        print '<th colspan="10">Years</th>'
        print '</tr>'
        # Get the current year based on system time
        current_year = localtime()[0]
        # Determine the current decade - Python division returns integers by default
        current_decade = current_year/10*10
        bgcolor = 0
        # Display all decades since 1950 in reverse chronological order
        for decade in range(current_decade, 1940, -10):
                print '<tr class="table%d">' % (bgcolor+1)
                print '<td><a href="http:/%s/most_popular.cgi?%d+decade+%d">%ds</a></td>' % (HTFAKE, type, decade, decade)
                for year in range(decade, decade+10):
                        # Skip future years
                        if year > current_year:
                                print '<td>&nbsp;</td>'
                                continue
                        print '<td><a href="http:/%s/most_popular.cgi?%d+year+%d">%d</a></td>' % (HTFAKE, type, year, year)
                print '</tr>'
                bgcolor ^= 1
        print '</table>'
	
	PrintTrailer('top', 0, 0)

