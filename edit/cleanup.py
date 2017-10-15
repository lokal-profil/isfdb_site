#!_PYTHONLOC
#
#     (C) COPYRIGHT 2012-2017 Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2017/03/13 14:37:44 $


import string
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *


if __name__ == '__main__':

	PrintPreSearch("ISFDB Data Cleanup Reports")
	PrintNavBar('edit/cleanup.cgi', 0)

        user = User()
        user.load()
        user.load_moderator_flag()

        try:
                all_reports = int(sys.argv[1])
                if all_reports > 1:
                        raise
                if all_reports == 1 and not user.moderator:
                        raise
	except:
                all_reports = 0

        print """<h3>The numbers in parentheses are the numbers of problem records found when each report
                was regenerated overnight; the current numbers may be lower.</h3>"""

        if user.moderator:
                print """Reports that can be viewed by non-moderators have asterisks next to their names.
                        Note that non-moderator can't mark records as "ignored"."""
        else:
                print """Some cleanup reports allow moderators to mark records as "ignored".
                         Note that moderators have access to additional reports. """

        if all_reports:
                print 'Displaying all reports. You can also limit the list to \
                <a href="http:/%s/edit/cleanup.cgi?0">reports with potential problems</a>.</h3>' % HTFAKE
        else:
                if user.moderator:
                        print 'Only reports with identified potential problems are displayed. You can \
                        also view a <a href="http:/%s/edit/cleanup.cgi?1">full list of reports</a>.</h3>' % HTFAKE

        (reports, sections, non_moderator) = reportsDict()

        # Determine the number of outstanding records for each report type that is regenerated every night
	query = "select count(*),report_type from cleanup where resolved is null group by report_type"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
        counts = {}
        for report_type in reports.keys():
                counts[int(report_type)] = 0
                # Report 199 is temporary and not regenerated nightly
                if int(report_type) == 199:
                        counts[int(report_type)] = 589
	while record:
		count = record[0][0]
		report_type = record[0][1]
		if user.moderator or (report_type in non_moderator):
                        counts[report_type] = count
        	record = result.fetch_row()

        for section in sections:
                report_numbers = section[1]
                # If there are no reports with identified problems in this section and
                # the list is limited to reports with identified problems, skip the whole section
                problems = 0
                for report_id in report_numbers:
                        problems += counts[report_id]
                if not problems and not all_reports:
                        continue
                print '<center><b>%s</b></center>' % section[0]
                for report_id in report_numbers:
                        # Skip reports with no identified problem records unless explicitly
                        # requested to display them
                        if not counts[report_id] and not all_reports:
                                continue
                        if user.moderator and report_id in non_moderator:
                                non_mod_flag = ' *'
                        else:
                                non_mod_flag = ''
                        print """<a href="http:/%s/edit/cleanup_report.cgi?%d">
                                <button type="button">%s (%d)%s</button>
                                </a>""" % (HTFAKE, report_id, reports[report_id], counts[report_id], non_mod_flag)
                        print '<p>'
                print '<hr>'

        # Determine the number of outstanding SFE3 URLs
        if user.moderator:
                print '<center><b>Reports That Are Not Regenerated Nightly</b></center>'

                query = "select count(*) from missing_author_urls where resolved=0 and author_id IS NULL"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()

                if int(record[0][0]) or all_reports:
                        print '<a href="http:/%s/mod/missing_author_urls.cgi?1"><button type="button">ISFDB-SFE3 Author Mismatches (%d)</button></a>' % (HTFAKE, int(record[0][0]))
                        print '<p>'

                # Determine the number of suspect pub images
                query = "select count(*) from bad_images"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()

                if int(record[0][0]) or all_reports:
                        print '<a href="http:/%s/mod/bad_images.cgi"><button type="button">Publications with Suspect Images (%d)</button></a>' % (HTFAKE, int(record[0][0]))
                        print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)
