#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2019   Al von Ruff, Bill Longley and Ahasuerus
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
                                7: 'Titles by Author Age',
                                8: 'Percent of Titles in Series by Year',
                                9: 'Percent of Book Titles by Type by Year',
                                10: 'Percent of Publications by Format by Year',
                                11: 'Submissions per Year',
                                12: 'Top Novels as Voted by ISFDB Users',
                                13: 'Most-Viewed Authors',
                                14: 'Most-Viewed Novels',
                                15: 'Most-Viewed Short Fiction',
                                16: 'Oldest Living Authors',
                                17: 'Oldest Non-Living Authors',
                                18: 'Youngest Living Authors',
                                19: 'Youngest Non-Living Authors',
                                20: 'Authors by Working Language',
                                21: 'Titles by Language',
                                22: 'Top Taggers',
                                23: 'Top Voters',
                                24: 'Top Forthcoming',
                                25: 'Top Short Fiction Titles as Voted by ISFDB Users'
                                }

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
                        print '<h3>This report is generated once a day</h3>'
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
