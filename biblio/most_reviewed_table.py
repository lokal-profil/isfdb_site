#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2013/12/18 21:03:57 $


import string
import sys
from SQLparsing import *
from biblio import *


if __name__ == '__main__':

	PrintHeader("Most-Reviewed Titles")
	PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        print '<h3><a href="http:/%s/most_reviewed.cgi?all">Most-Reviewed Titles of All Time</a></h3>' % (HTFAKE)
        print '<h3><a href="http:/%s/most_reviewed.cgi?pre1900">Most-Reviewed Titles Prior to 1900</a></h3>' % (HTFAKE)

        print '<h3>Most-Reviewed Titles Since 1900 by Decade and Year</h3>'
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
        # Display all decades since 1900 in reverse chronological order
        for decade in range(current_decade, 1890, -10):
                print '<tr class="table%d">' % (bgcolor+1)
                print '<td><a href="http:/%s/most_reviewed.cgi?decade+%d">%ds</a></td>' % (HTFAKE, decade, decade)
                for year in range(decade, decade+10):
                        # Skip future years
                        if year > current_year:
                                print '<td>&nbsp;</td>'
                                continue
                        print '<td><a href="http:/%s/most_reviewed.cgi?year+%d">%d</a></td>' % (HTFAKE, year, year)
                print '</tr>'
                bgcolor ^= 1
        print '</table>'
	
	PrintTrailer('top', 0, 0)

