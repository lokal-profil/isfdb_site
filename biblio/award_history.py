#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020-2021   Ahasuerus
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
        PrintHeader('Unknown Award Record')
        PrintNavbar(0, 0, 0, 'award_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('award_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		award_id = int(sys.argv[1])
	except:
                DoError('Invalid Award ID specified')

	PrintHeader('Award Edit History')
	PrintNavbar('award_history', 0, 0, 'award_history.cgi', award_id)

        print """<h3>The list below displays the following types of submissions: Add Award,
                Edit Award, Delete Award, Link Award. The submission which created this
                award is displayed if the award was created after 2016-10-24.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (award_id, MOD_AWARD_NEW, MOD_AWARD_UPDATE, MOD_AWARD_DELETE, MOD_AWARD_LINK)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this award.</h3>'
        else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('award_history', 0, 0)

