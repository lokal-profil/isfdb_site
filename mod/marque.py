#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2006   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2009/05/28 00:20:01 $


import sys
import os
import string
from SQLparsing import *
from isfdblib import *
from library import *


if __name__ == '__main__':

        PrintPreMod('ISFDB - Set Marque Authors')
        PrintNavBar()

	#################################
	# Calculate top 2 percent
	#################################
        query = "select count(author_id) from authors;"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
	total_authors = record[0][0]
	maxauthors = total_authors / 50

	update = "update authors set author_marque='0'"
	db.query(update)

	query = "select author_id,author_views,author_canonical from authors where author_views > 0 order by author_views desc limit %d" % maxauthors
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<ol>"

	while record:
		print "<li>%d - %s" % (record[0][1], record[0][2])
		update = "update authors set author_marque='1' where author_id=%s" % (record[0][0])
		db.query(update)
		record = result.fetch_row()

	print "</ol>"
	PrintPostMod()
