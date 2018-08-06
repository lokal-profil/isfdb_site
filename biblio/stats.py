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

if __name__ == '__main__':

	PrintHeader('ISFDB Statistics')
	PrintNavbar('stats', 0, 0, 'stats.cgi', 0)
	query = 'select report_data from reports where report_id = 4'
	db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                print record[0][0]
        else:
                print '<h3>This report is currently unavailable. It will be regenerated overnight.</h3>'
	PrintTrailer('frontpage', 0, 0)
