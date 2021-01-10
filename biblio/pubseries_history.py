#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2019-12-01 19:57:53 -0400 (Tue, 31 Oct 2017) $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node


def DoError(message):
        PrintHeader('Unknown Publication Series Record')
        PrintNavbar(0, 0, 0, 'pubseries_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('pubseries_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		pubseries_id = int(sys.argv[1])
	except:
                DoError('Invalid Publication Series ID specified')

	PrintHeader('Publication Series Edit History')
	PrintNavbar('pubseries_history', 0, 0, 'pubseries_history.cgi', pubseries_id)

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d)
                order by sub_reviewed desc
                """ % (pubseries_id, MOD_PUB_SERIES_UPDATE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this publication series</h3>'
		PrintTrailer('pubseries_history', 0, 0)
		sys.exit(0)

        print """<h3>The list below displays Edit Publication Series submissions for this publication series.
                Note that publication series records are created and deleted automatically when
                publications are created/edited/deleted; related
                submissions are not displayed on this page.</h3>"""
        ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('pubseries_history', 0, 0)

