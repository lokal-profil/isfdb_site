#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2019   Al von Ruff, Ahasuerus and Dirk Stoecker
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
from library import *
from xml.dom import minidom
from xml.dom import Node


if __name__ == '__main__':

	PrintHeader("Recent Edits")
	PrintNavbar('recent', 0, 0, 'recent.cgi', 0)

	try:
		start = int(sys.argv[1])
	except:
		start = 0

	if start:
		query = "select * from submissions use index (sub_reviewed) where sub_state='I' order by sub_reviewed desc limit %d,200;" % (start)
	else:
		query = "select * from submissions use index (sub_reviewed) where sub_state='I' order by sub_reviewed desc limit 200;"
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>No submissions present</h3>'
		PrintTrailer('recent', 0, 0)
		sys.exit(0)

        ISFDBprintSubmissionTable(result, 'I')
	print '<p> [<a href="http:/%s/recent.cgi?%d">MORE</a>]' % (HTFAKE, start+200)

	PrintTrailer('recent', 0, 0)

