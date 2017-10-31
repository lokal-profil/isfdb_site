#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2013   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from login import *
from SQLparsing import *
	
if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Series Submission")

	try:
		record = int(sys.argv[1])
	except:
		PrintNavBar(0, 0)
		print "<h3>Non-existing or invalid series number.</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
	
	PrintNavBar("edit/deleteseries.cgi", record)

	seriesRecord = SQLget1Series(record)
	if not seriesRecord:
		print "<h3>Specified series does not exist.</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	# Find sub-series of this series
	subseries = SQLFindSeriesChildren(record)
	if len(subseries) > 0:
		print "<h2>Error: Series with sub-series cannot be deleted until all sub-series have been removed.</h2>"
		print "<h2>This series still has %d sub-series.</h2>" % (len(subseries))
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	# Find any titles that belong to this series
	titles = SQLloadTitlesXBS(record)
        if len(titles) > 0:
		print "<h2>Error: Non-empty series can't be deleted.</h2>"
		print "<h2>This series still has %d titles:</h2>" % (len(titles))
		print "<ul>"
		for title in titles:
			print "<li>"
			try:
				print '<a href="http:/%s/title.cgi?%d">%s</a> (%s)' % (HTFAKE, title[TITLE_PUBID], title[TITLE_TITLE], title[TITLE_YEAR])
                        except:
                                continue
		print "</ul>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

        seriesname = SQLgetSeriesName(record)
        print "<b>Request to Delete:</b> <i>%s</i>" % seriesname
        print "<p />"

        print "<form METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submitdelseries.cgi\">"
        print "<b>Deletion Reason</b><br />"
        print '<textarea name="reason" rows="4" cols="45"></textarea>'
        print '<p />'
        print '<input name="series_id" value="%d" type="HIDDEN">' % record
        print '<input name="series_name" value="%s" type="HIDDEN">' % (seriesname)
        print '<input type="SUBMIT" value="Delete">'
        print "</form>"
	
	PrintPostSearch(0, 0, 0, 0, 0)
