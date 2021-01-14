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
        PrintHeader('Unknown Award Category Record')
        PrintNavbar(0, 0, 0, 'award_category_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('award_category_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		award_category_id = int(sys.argv[1])
	except:
                DoError('Invalid Award Category ID specified')

	PrintHeader('Award Category Edit History')
	PrintNavbar('award_category_history', 0, 0, 'award_category_history.cgi', award_category_id)

        print """<h3>The list below displays the following types of submissions: New Award Category,
                Edit Award Category, Delete Award Category. The submission which created this award category is displayed
                if the award category was created after 2016-10-24.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d)
                order by sub_reviewed desc
                """ % (award_category_id, MOD_AWARD_CAT_NEW, MOD_AWARD_CAT_UPDATE, MOD_AWARD_CAT_DELETE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this award category.</h3>'
	else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('award_category_history', 0, 0)

