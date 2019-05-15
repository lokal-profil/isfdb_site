#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *

def doError():
	PrintPreSearch("Containers with no Fiction Titles")
	PrintNavBar('edit/empty_container_table.cgi', 0)
        print '<h3>Bad argument</h3>'
        PrintPostSearch(0, 0, 0, 0, 0)
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
                report_id = int(sys.argv[3])
                if report_id not in (240, 241):
                        raise
        except:
                doError()

        if report_id == 240:
                container_names = 'Anthologies and Collections'
        else:
                container_names = 'Magazines'
	PrintPreSearch("%s with no Fiction Titles" % container_names)
	PrintNavBar('edit/empty_container_table.cgi', 0)

        print '<h3>Date range: %s</h3>' % display_range
        query = """select c.cleanup_id, p.*
                from pubs p, cleanup c
                where c.resolved IS NULL
                and c.report_type = %d
                and c.record_id_2 like '%d%%'
                and c.record_id = p.pub_id
                and p.pub_year != '8888-00-00'
                and NOT EXISTS
                        (select 1 from pub_content pc, titles t
                        where p.pub_id=pc.pub_id 
                        and pc.title_id=t.title_id
                        and t.title_ttype in ('NOVEL', 'SHORTFICTION', 'POEM', 'SERIAL')
                        )
                order by pub_title""" % (report_id, date_range)
        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print 'No eligible publications for the specified date range'
                sys.exit(0)

        user = User()
        user.load()
        user.load_moderator_flag()

        if report_id == 240:
                PrintTableColumns(('', 'Title', 'Authors', 'Pub. Date', 'Type', '1st Edition', 'Publisher', 'Note', 'Ignore'), user)
        else:
                PrintTableColumns(('', 'Title', 'Editors', 'Pub. Date', 'Publisher', 'Note', 'Ignore'), user)
        record = result.fetch_row()
        count = 1
        bgcolor = 1
        while record:
                cleanup_id = record[0][0]
                pub_data = record[0][1:]
                pub_id = pub_data[PUB_PUBID]
                pub_title = pub_data[PUB_TITLE]
                pub_date = pub_data[PUB_YEAR]
                pub_type = pub_data[PUB_CTYPE]
                publisher_id = pub_data[PUB_PUBLISHER]
                note_id = pub_data[PUB_NOTE]
                note_note = SQLgetNotes(note_id)
                authors = SQLPubBriefAuthorRecords(pub_id)
                publisher = SQLGetPublisher(publisher_id)
                referral_id = SQLgetTitleReferral(pub_id, pub_data[PUB_CTYPE])
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>%d</td>' % count
                print '<td>%s</td>' % ISFDBLink("pl.cgi", pub_id, pub_title)
                print '<td>%s</td>' % LIBbuildRecordList('author', authors)
                print '<td>%s</td>' % pub_date
                if report_id == 240:
                        print '<td>%s</td>' % pub_type[:4]

                        referral_column = 0
                        if referral_id:
                                referral_title = SQLloadTitle(referral_id)
                                if referral_title[TITLE_YEAR] != pub_date:
                                        print '<td>%s</td>' % referral_title[TITLE_YEAR]
                                        referral_column = 1
                        if not referral_column:
                                print '<td>&nbsp;</td>'

                if publisher:
                        print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME])
                else:
                        print '<td>&nbsp;</td>'
                print '<td>%s</td>' % FormatNote(note_note)
                if user.moderator:
                        print '<td><a href="http:/%s/mod/resolve_cleanup.cgi?%d+1+%d">Ignore</a></td>' % (HTFAKE, cleanup_id, report_id)
                print '</tr>'
                count += 1
                bgcolor ^= 1
                record = result.fetch_row()
	
        PrintPostSearch(0, 0, 0, 0, 0)
