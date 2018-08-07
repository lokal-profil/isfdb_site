#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2018   Al von Ruff, Bill Longley and Ahasuerus
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

class Stats:
        def __init__(self):
                self.headers = {
                                1: 'Top Moderators',
                                2: 'Top Verifiers',
                                4: 'ISFDB Statistics',
                                5: 'Titles by Year of First Publication',
                                6: 'Publications by Year',
                                7: 'Titles by Author Age'}

        def params(self):
                try:
                        self.report_id = int(sys.argv[1])
                        self.header = self.headers[self.report_id]
                except:
                        PrintHeader('Invalid Argument')
                        PrintNavbar('stats', 0, 0, 'stats.cgi', 0)
                        print '<h3>Invalid Argument</h3>'
                        PrintTrailer('frontpage', 0, 0)
                        sys.exit(0)

        def output(self):
                query = 'select report_data from reports where report_id = %d' % stats.report_id
                db.query(query)
                result = db.store_result()
                if result.num_rows():
                        record = result.fetch_row()
                        print record[0][0]
                else:
                        print '<h3>This report is currently unavailable. It will be regenerated overnight.</h3>'

if __name__ == '__main__':

        stats = Stats()
        stats.params()
	PrintHeader(stats.header)
	PrintNavbar('stats', 0, 0, 'stats.cgi', 0)
	stats.output()
	PrintTrailer('frontpage', 0, 0)
