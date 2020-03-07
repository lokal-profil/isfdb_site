#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019-2020   Ahasuerus
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
        PrintHeader('Unknown Publication Record')
        PrintNavbar(0, 0, 0, 'pub_history.cgi', 0)
        print '<h3>%s</h3>' % message
        PrintTrailer('pub_history', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

	try:
		pub_id = int(sys.argv[1])
	except:
                DoError('Invalid Publication ID specified')

	PrintHeader('Publication Edit History')
	PrintNavbar('pub_history', 0, 0, 'pub_history.cgi', pub_id)

        query = """select * from submissions
                where affected_record_id = %d
                and sub_type in (%d, %d, %d)
                order by sub_reviewed desc""" % (pub_id, MOD_PUB_NEW, MOD_PUB_CLONE, MOD_PUB_UPDATE)
	db.query(query)
	result = db.store_result()
	if not result.num_rows():
		print '<h3>No submission data on file for this publication</h3>'
		PrintTrailer('pub_history', 0, 0)
		sys.exit(0)

        print """<h3>At this time the list below displays ALL submissions which edited
                this publication or imported titles into it. The submission which created
                this publication is displayed for publications created after 2016-10-24.</h3>"""
        ISFDBprintSubmissionTable(result, 'I')

	PrintTrailer('pub_history', 0, 0)

