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
        PrintHeader('Unknown Title Record')
        PrintNavbar(0, 0, 0, 'title_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('title_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		title_id = int(sys.argv[1])
	except:
                DoError('Invalid Title ID specified')

	PrintHeader('Title Edit History')
	PrintNavbar('title_history', 0, 0, 'title_history.cgi', title_id)

        print """<h3>The list below displays all Edit Title, Make Variant, 
                Delete Title, Title Unmerge and Link Review submissions for this title record.
                Add Variant Title submissions are listed if approved after 2021-01-11.
                Note that title records are created automatically when
                publications are created/edited; related
                submissions are not displayed on this page.</h3>"""

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d, %d, %d, %d)
                order by sub_reviewed desc
                """ % (title_id, MOD_TITLE_UPDATE, MOD_TITLE_DELETE,
                       MOD_TITLE_MKVARIANT, MOD_REVIEW_LINK,
                       MOD_VARIANT_TITLE, MOD_TITLE_UNMERGE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this title.</h3>'
        else:
                ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('title_history', 0, 0)

