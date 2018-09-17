#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import string
import sys
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *

def doError():
        print '<h3>Bad argument</h3>'
        sys.exit(0)

def PrintTableColumns(columns, user):
	print '<table class="generic_table">'
	print '<tr class="table2">'
	for column in columns:
                if not column:
                        data = '&nbsp;'
                else:
                        data = column
                # Skip 'Ignore' and 'Resolve' columns if the user is not a moderator
                if ('Ignore' in column or 'Resolve' in column) and not user.moderator:
                        continue
                print "<td><b>%s</b></td>" % data
 	print '</tr>'

if __name__ == '__main__':

	PrintPreSearch("Anthologies and Collections with no Fiction Titles")
	PrintNavBar('edit/empty_container_table.cgi', 0)

        # If the script was called with no arguments, then it's an error
        if len(sys.argv) == 1:
                doError()
        try:
                report_type = sys.argv[1]
                date_range = int(sys.argv[2])
                if report_type == 'decade':
                        display_range = '%s0s' % date_range
                elif report_type == 'year':
                        display_range = date_range
                elif report_type == 'month':
                        display_range = '%s-%s' % (str(date_range)[:4], str(date_range)[4:6])
                elif report_type == 'unknown':
                        display_range = '0000-00'
                else:
                        raise
                print '<h3>Date range: %s</h3>' % display_range
        except:
                doError()

        query = """select c.cleanup_id, p.pub_id, p.pub_title,
                p.pub_year, p.pub_ctype, p.note_id
                from pubs p, cleanup c
                where c.resolved IS NULL
                and c.report_type = 240
                and c.record_id_2 like '%d%%'
                and c.record_id = p.pub_id
                order by pub_title""" % date_range
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print 'No eligible Anthology or Collection publications for the specified date range'
                sys.exit(0)

        user = User()
        user.load()
        user.load_moderator_flag()

        PrintTableColumns(('', 'Title', 'Authors', 'Date', 'Pub. Type', 'Note', 'Ignore'), user)
        record = result.fetch_row()
        count = 1
        bgcolor = 1
        while record:
                cleanup_id = record[0][0]
                pub_id = record[0][1]
                pub_title = record[0][2]
                pub_date = record[0][3]
                pub_type = record[0][4]
                note_id = record[0][5]
                note_note = SQLgetNotes(note_id)
                authors = SQLPubBriefAuthorRecords(pub_id)
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink("pl.cgi", pub_id, pub_title)
                print '<td>%s</td>' % LIBbuildRecordList('author', authors)
                print '<td>%s</td>' % pub_date
                print '<td>%s</td>' % pub_type
                print '<td>%s</td>' % note_note
                if user.moderator:
                        print '<td><a href="http:/%s/mod/resolve_cleanup.cgi?%d+1+240">Ignore</a></td>' % (HTFAKE, cleanup_id)
                print '</tr>'
                count += 1
                bgcolor ^= 1
                record = result.fetch_row()
	
        PrintPostSearch(0, 0, 0, 0, 0)
