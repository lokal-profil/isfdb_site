#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/01/20 15:59:43 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        PrintPreMod('Series Delete - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if NotApprovable(submission):
                sys.exit(0)

	xml = SQLloadXML(submission)
	doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('SeriesDelete'):
		merge = doc.getElementsByTagName('SeriesDelete')
        	Record = GetElementValue(merge, 'Record')
        	
                #Check if the series has already been deleted
                seriesRecord = SQLget1Series(int(Record))
                if seriesRecord == 0:
                        print '<div id="ErrorBox">'
                        print "<h3>Error: This series no longer exists.</h3>"
                        print '<h3>Please <a href="http:/%s/mod/hardreject.cgi?%s">use Hard Reject</a> to reject it.</h3>' % (HTFAKE, sys.argv[1])
                        print '</div>'
                        PrintPostMod()
                        sys.exit(0)

                # Check if sub-series have been added to this series since the time the submission was created
                subseries = SQLFindSeriesChildren(int(Record))
                if len(subseries) > 0:
                        print '<div id="ErrorBox">'
                        print "<h2>Error: At least one sub-series has been added to this Series since the time this submission was created.</h2>"
                        print "<h2>This series can't be deleted until all sub-series are removed.</h2>"
                        print '<h3>If you do not want to remove the sub-series, please <a href="http:/%s/mod/hardreject.cgi?%s">use Hard Reject</a> to reject the submission.</h3>' % (HTFAKE, sys.argv[1])
                        print '</div>'
                        PrintPostMod()
                        sys.exit(0)

                # Check if titles have been added to this series since the time the submission was created
                titles = SQLloadTitlesXBS(int(Record))
                if len(titles) > 0:
                        print '<div id="ErrorBox">'
                        print "<h2>Error: At least one title has been added to this series since the time this submission was created.</h2>"
                        print "<h2>This series can't be deleted until all titles are removed.</h2>"
                        print '<h3>If you do not want to remove the titles, please <a href="http:/%s/mod/hardreject.cgi?%s">use Hard Reject</a> to reject the submission.</h3>' % (HTFAKE, sys.argv[1])
                        print '</div>'
                        PrintPostMod()
                        sys.exit(0)

		##########################################################
		# Delete the series
		##########################################################
        	print "<h1>SQL Updates:</h1>"
        	print "<hr>"
        	print "<ul>"
		update = "delete from series where series_id=%d" % (int(Record))
		print "<li> ", update
		db.query(update)
		update = "delete from webpages where series_id=%d" % (int(Record))
		print "<li> ", update
		db.query(update)
		if seriesRecord[SERIES_NOTE]:
                        update = "delete from notes where note_id=%d" % (int(seriesRecord[SERIES_NOTE]))
                        print "<li> ", update
                        db.query(update)
                        
		submitter = GetElementValue(merge, 'Submitter')
		markIntegrated(db, submission)

	print "</ul>"
	print "<hr>"
	print '[<a href="http:/' +HTFAKE+ '/mod/list.cgi?N">Submission List</a>]'
	print "<p>"

	PrintPostMod()
