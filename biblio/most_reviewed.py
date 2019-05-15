#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2018   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
from SQLparsing import *
from biblio import *
from common import PrintAllAuthors
from library import convertYear

def doError():
        print '<h3>Bad argument</h3>'
        sys.exit(0)

if __name__ == '__main__':

	PrintHeader("Most-Reviewed Titles Details")
	PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        display_year = ''
        decade = ''
        # If the module was called with no arguments, then it's an error
        if len(sys.argv) == 1:
                doError()
        elif sys.argv[1] == 'all':
                report_type = 'all'
                print '<h3>Most-Reviewed Titles of All Time</h3>'
        elif sys.argv[1] == 'decade':
                try:
                        report_type = 'decade'
                        decade = int(sys.argv[2])
                except:
                        doError()
                print '<h3>Most-Reviewed Titles of the %ss</h3>' % decade
        elif sys.argv[1] == 'year':
                try:
                        report_type = 'year'
                        display_year = int(sys.argv[2])
                except:
                        doError()
                print '<h3>Most-Reviewed Titles of %s</h3>' % display_year
        elif sys.argv[1] == 'pre1900':
                report_type = 'pre1900'
                print '<h3>Most-Reviewed Titles Prior to 1900</h3>'
        else:
                doError()

        print '<h3>This report is generated once a day</h3>'

        query = 'select title_id, year, reviews from most_reviewed'
        if report_type == 'year':
                query += ' where year=%d' % display_year
        elif report_type == 'decade':
                query += ' where decade=%d' % decade
        elif report_type == 'pre1900':
                query += ' where decade="pre1900"'
        query += ' order by reviews desc limit 500'

        db.query(query)
        result = db.store_result()
        if not result.num_rows():
                print '<h3>This report is currently unavailable. It will be regenerated overnight.</h3>'
        else:
                # Print the table headers        
                print '<table class="seriesgrid">'
                print '<tr>'
                print '<th>Count</th>'
                print '<th>Reviews</th>'
                if report_type != 'year':
                        print '<th>Year</th>'
                print '<th>Title</th>'
                print '<th>Type</th>'
                print '<th>Authors</th>'
                print '</tr>'
                record = result.fetch_row()
                bgcolor = 0
                count = 1
                while record:
                        title_id = record[0][0]
                        year = record[0][1]
                        reviews = record[0][2]
                        print '<tr align=left class="table%d">' % (bgcolor+1)
                        print '<td>%d</td>' % count
                        print '<td>%d</td>' % reviews
                        # Display the year of the title unless we are displaying the data for just one year
                        if report_type != 'year':
                                display_year = unicode(year)
                                if display_year == '0':
                                        display_year = '0000'
                                print '<td>%s</td>' % convertYear(display_year)
                        # Retrieve this record's title and type
                        title_data = SQLloadTitle(title_id)
                        print '<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_data[TITLE_TITLE])
                        print '<td>%s</td>' % title_data[TITLE_TTYPE]
                        print '<td>'
                        PrintAllAuthors(title_id)
                        print '</td>'
                        print '</tr>'
                        record = result.fetch_row()
                        bgcolor = bgcolor ^ 1
                        count += 1
                print '</table>'
	
	PrintTrailer('top', 0, 0)

