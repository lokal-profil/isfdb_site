#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2018   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

	PrintHeader('Top Moderators')
	PrintNavbar('top', 0, 0, 'topmods.cgi', 0)
	query = 'select report_data from reports where report_id = 1'
	db.query(query)
        result = db.store_result()
        if result.num_rows():
                record = result.fetch_row()
                print record[0][0]
        else:
                print '<h3>This report is currently unavailable. It will be regenerated overnight.</h3>'
	PrintTrailer('top', 0, 0)

