#!_PYTHONLOC
#
#     (C) COPYRIGHT 2012-2019 Bill Longley and Ahasuerus
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
from cleanup_lib import reportsDict
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *
from sfe3 import Sfe3


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

        print '<b>Legend:</b>'
        print '<ul>'
        print """<li>The numbers in parentheses show how many problem records were found when each report
                was last regenerated; the current numbers may be lower."""

        if user.moderator:
                print """<li>Reports that can be viewed by non-moderators have asterisks next to their names.
                        <li>Note that non-moderators can't mark records as "ignored".
                        <li>For an explanation of the "ignore" functionality see
                        <a href="http://%s/index.php/Help:Screen:IgnoreCleanupRecords">this Help page.</a>""" % WIKILOC
        else:
                print """<li>Some cleanup reports allow moderators to mark records as "ignored".
                         Note that moderators have access to additional reports. """

        if all_reports:
                print """<li>Displaying all reports. You can also limit the list to 
                <a href="http:/%s/edit/cleanup.cgi?0">reports with identified potential problems</a>.""" % HTFAKE
        else:
                if user.moderator:
                        print """<li>Only reports with identified potential problems are displayed. You can 
                        also view a <a href="http:/%s/edit/cleanup.cgi?1">full list of reports</a>.""" % HTFAKE
        print '</ul>'

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
                print '<h3 class="centered">%s</h3>' % section[0]
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

        print '<h3 class="centered">Reconciliation with Other Sources</h3>'
        sfe3 = Sfe3()
        print """<a href="http:/%s/edit/sfe3_authors.cgi"><button type="button">
                SFE3 Author Articles without Matching ISFDB Author Records (%d)</button></a>""" % (HTFAKE, sfe3.count_of_unresolved())
        print '<p>'
        print '<hr>'

        print '<h3 class="centered">Reports That Are Not Regenerated Nightly</h3>'

        if user.moderator:
                # Determine the number of suspect pub images
                query = "select count(*) from bad_images"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()

                if int(record[0][0]) or all_reports:
                        print '<a href="http:/%s/mod/bad_images.cgi"><button type="button">Publications with Suspect Images (%d)</button></a>' % (HTFAKE, int(record[0][0]))
                        print '<p>'

        print '<a href="http:/%s/edit/numeric_external_id_ranges.cgi"><button type="button">View Ranges of Numeric External Identifiers</button></a>' % HTFAKE
        print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0, 0)
