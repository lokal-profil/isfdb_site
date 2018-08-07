#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2018   Al von Ruff and Ahasuerus
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


def displayCharts(report_id):
	query = 'select report_data from reports where report_id = %d' % report_id
	db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                print record[0][0]
        else:
                print '<h3>This report is currently unavailable. It will be regenerated overnight.</h3>'

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
                displayCharts(5)

        elif sys.argv[1] == "Publications":
                displayCharts(6)

        elif sys.argv[1] == "Age":
                displayCharts(7)

	PrintTrailer('frontpage', 0, 0)
