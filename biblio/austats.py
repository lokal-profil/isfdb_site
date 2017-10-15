#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2014   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2014/01/17 05:24:43 $


import sys
import os
import string
from SQLparsing import *
from common import *

limit = 300

if __name__ == '__main__':

	try:
		mode = sys.argv[1]
	except:
		mode = 'total'

	try:
		style = sys.argv[2]
	except:
		style = 'normal'

	PrintHeader('ISFDB - Most Queried Authors')
	PrintNavbar('stats', 0, 0, 'austats.cgi', mode)

        query = "select metadata_counter from metadata"
        db.query(query)
        result = db.store_result()
	record = result.fetch_row()
	print "<ul>"
	print "<li> Total Page Views: ", record[0][0]

	query = "select SUM(author_views) from authors;"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li> Total Author Views: ", record[0][0]

	query = "select COUNT(author_views) from authors where author_views>0;"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li> Number of Authors Viewed: ", record[0][0]
	print "</ul>"

	if mode == 'annual':
		query = "select author_id,author_annualviews,author_canonical from authors where author_annualviews > 0 order by author_annualviews desc limit %d" % limit
	else:
		query = "select author_id,author_views,author_canonical from authors where author_views > 0 order by author_views desc limit %d" % limit

	if style == 'normal':
		print '<ol>'
	else:
		print '<pre>'

	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		if style == 'normal':
                        print "<li>%d - %s" % (record[0][1], record[0][2])
		else:
			print "# [http://%s/cgi-bin/ea.cgi?%s %s] [[Author:%s|ISFDB Wiki]]" % (HTMLHOST, record[0][0], record[0][2], record[0][2])
		record = result.fetch_row()

	if mode == 'normal':
		print '</ol>'
	else:
		print '</pre>'

	PrintTrailer('frontpage', 0, 0)
