#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2018   Ahasuerus
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
from common import *


if __name__ == '__main__':

	PrintHeader("Most-Reviewed Titles")
	PrintNavbar('top', 0, 0, 'most_reviewed_table.cgi', 0)

        print '<h3><a href="http:/%s/most_reviewed.cgi?all">Most-Reviewed Titles of All Time</a></h3>' % (HTFAKE)
        print '<h3><a href="http:/%s/most_reviewed.cgi?pre1900">Most-Reviewed Titles Prior to 1900</a></h3>' % (HTFAKE)

        print '<h3>Most-Reviewed Titles Since 1900 by Decade and Year</h3>'
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th>Decade</th>'
        print '<th colspan="10">Years</th>'
        print '</tr>'
        PrintAnnualGrid(1900, 'most_reviewed', 'year+', 1, 'decade+')
	
	PrintTrailer('top', 0, 0)

