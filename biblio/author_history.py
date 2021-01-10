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
        PrintHeader('Author Edit History error')
        PrintNavbar(0, 0, 0, 'author_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('author_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		author_id = int(sys.argv[1])
	except:
                DoError('Invalid Author ID specified')

	user = User()
	user.load()
	if not user:
                DoError('Only ISFDB moderators can view author edit history at this time')
        user.load_moderator_flag()
        if not user.moderator:
                DoError('Only ISFDB moderators can view author edit history at this time')

	PrintHeader('Author Edit History')
	PrintNavbar('author_history', 0, 0, 'author_history.cgi', author_id)

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d)
                order by sub_reviewed desc
                """ % (author_id, MOD_AUTHOR_UPDATE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this author</h3>'
		PrintTrailer('author_history', 0, 0)
		sys.exit(0)

        print """<h3>The list below displays Edit Author submissions only.
                Note that author records are created and deleted automatically when
                publications and titles are created/edited/deleted; related
                submissions are not displayed on this page.</h3>"""
        ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('author_history', 0, 0)

