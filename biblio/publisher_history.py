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
        PrintHeader('Unknown Publisher Record')
        PrintNavbar(0, 0, 0, 'publisher_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('publisher_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		publisher_id = int(sys.argv[1])
	except:
                DoError('Invalid Publisher ID specified')

	PrintHeader('Publisher Edit History')
	PrintNavbar('publisher_history', 0, 0, 'publisher_history.cgi', publisher_id)

        print """<h3>The list below displays Edit Publisher and Publisher Merge submissions for this publisher.
                Note that publisher records are created and deleted automatically when
                publications are created/edited/deleted; related
                submissions are not displayed on this page.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d)
                order by sub_reviewed desc
                """ % (publisher_id, MOD_PUBLISHER_UPDATE, MOD_PUBLISHER_MERGE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this publisher.</h3>'
	else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('publisher_history', 0, 0)

