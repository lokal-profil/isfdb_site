#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020   Ahasuerus
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

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d)
                order by sub_reviewed desc
                """ % (title_id, MOD_TITLE_UPDATE, MOD_TITLE_DELETE, MOD_TITLE_MKVARIANT)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this title</h3>'
		PrintTrailer('title_history', 0, 0)
		sys.exit(0)

        print """<h3>The list below displays Edit Title, Make Variant and
                Delete Title submissions for this title record.</h3>"""
        ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('title_history', 0, 0)

