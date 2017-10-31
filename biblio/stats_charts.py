#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2014   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import os
import string
from SQLparsing import *
from biblio import *


def displayCharts(types):
        for type in types:
                print '<h3>%s</h3>' % (type[1])
		filename = LOCALFILES + "%s.svg" % type[0]
                f = open(filename,"r")
                data = f.read()
                f.close()
                print data
        return

if __name__ == '__main__':

        if sys.argv[1] == 'Titles':
                header = 'Titles by Year'
        elif sys.argv[1] == 'Publications':
                header = 'Publications by Year'
        elif sys.argv[1] == 'Age':
                header = 'Title Distribution by Author Age'
        else:
                header = 'Invalid argument'
	PrintHeader(header)
	PrintNavbar('stats', 0, 0, 'stats_charts.cgi', 0)
	if header == 'Invalid argument':
                print "<h3>Invalid Argument</h3>"
        	PrintTrailer('frontpage', 0, 0)
                sys.exit(0)

        if sys.argv[1] == "Titles":
                types = [('year_novels','Novels')]
                types.append(('year_shortfiction','Short Fiction'),)
                types.append(('year_reviews','Reviews'),)
                displayCharts(types)

        elif sys.argv[1] == "Publications":
                types = [('year_pubs','Publications (without magazines)')]
                types.append(('year_magazines','Magazines'),)
                types.append(('year_verif','Verified Publications in Percent'),)
                displayCharts(types)

        elif sys.argv[1] == "Age":
                types = [('age_all_novels','All Novels')]
                types.append(('age_first_novel','First Novels'),)
                types.append(('age_all_short','All Short Fiction'),)
                types.append(('age_first_short','First Short Fiction'),)
                displayCharts(types)

	PrintTrailer('frontpage', 0, 0)
