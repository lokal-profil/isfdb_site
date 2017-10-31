#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2016   Ahasuerus
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
from library import AutoVivification, convertYear
import operator

def doError():
        print '<h3>Bad argument</h3>'
        sys.exit(0)

def printTableBody(reviews, type, display_year, decade):
	bgcolor = 0
        eligible = 0
        for count in sorted(reviews.keys(), reverse=True):
                for year in sorted(reviews[count].keys(), reverse=True):
                        for title_id in reviews[count][year].keys():
                                print '<tr align=left class="table%d">' % (bgcolor+1)
                                print '<td>%d</td>' % count
                                # Display the year of the title unless we are displaying the data for just one year
                                if type != 'year':
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
                                bgcolor = bgcolor ^ 1
                                eligible += 1
                                # Once we have displayed 500 rows, quit
                                if eligible > 499:
                                        return


if __name__ == '__main__':

	PrintHeader("Most-Reviewed Titles Details")
	PrintNavbar('top', 0, 0, 'most_reviewed.cgi', 0)

        display_year = ''
        decade = ''
        # If the module was called with no arguments, then it's an error
        if len(sys.argv) == 1:
                doError()
        elif sys.argv[1] == 'all':
                type = 'all'
                print '<h3>Most-Reviewed Titles of All Time</h3>'
        elif sys.argv[1] == 'decade':
                try:
                        type = 'decade'
                        decade = int(sys.argv[2])
                except:
                        doError()
                print '<h3>Most-Reviewed Titles of the %ss</h3>' % decade
        elif sys.argv[1] == 'year':
                try:
                        type = 'year'
                        display_year = int(sys.argv[2])
                except:
                        doError()
                print '<h3>Most-Reviewed Titles of %s</h3>' % display_year
        elif sys.argv[1] == 'pre1900':
                type = 'pre1900'
                print '<h3>Most-Reviewed Titles Prior to 1900</h3>'
        else:
                doError()

        # Initialize the dictionary which will hold review counts for title IDs
        counts = {}
        # Initialize the dictionary which will hold years for title IDs
        years = {}
        # Initialize the list of parent title IDs
        parents = []
        # Retrieve all reviewed title IDs, their dates and IDs of their parent titles
        query = "select t.title_id,t.title_parent,YEAR(t.title_copyright) from title_relationships as r, titles as t where r.title_id=t.title_id"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	while record:
                title_id = record[0][0]
                parent_id = record[0][1]
                year = record[0][2]
                # If this title is a VT, add its parent to the list of parents to be retrieved later
                if parent_id != 0:
                        title_id = parent_id
                        if str(parent_id) not in parents:
                                parents.append(str(parent_id))
                # Increment the count of reviews for this title ID
                counts[title_id] = counts.get(title_id, 0) +1
                years[title_id] = year
        	record = result.fetch_row()
        # Convert the list of parent IDs to a string in the SQL IN clause format
        parents_string = ','.join(parents)

        # Retrieve dates of parent titles
        query = "select title_id, YEAR(title_copyright) from titles where title_id in (%s)" % (db.escape_string(parents_string))
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	while record:
                title_id = record[0][0]
                year = record[0][1]
                # If the parent's year is less than the variant's, use the parent' year
                if (years[title_id] == 0) or (year < years[title_id]):
                        years[title_id] = year
        	record = result.fetch_row()

        # Created a sorted list of count/title tuples starting with the most-reviewed title
        sorted_counts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)

        # Populate an auto-vivified dictionary which will be used for display purposes
        reviews = AutoVivification()
        for tuple in sorted_counts:
                title_id = tuple[0]
                count = tuple[1]
                year = years[title_id]
                if type == 'all':
                        pass
                elif type == 'pre1900':
                        if year > 1899:
                                continue
                elif type == 'year':
                        if year != display_year:
                                continue
                elif type == 'decade':
                        if year/10*10 != decade:
                                continue
                else:
                        print "type: ",type
                        print tuple
                        raise
                reviews[count][year][title_id] = ''

        # Print the table headers        
	print '<table class="seriesgrid">'
	print '<tr>'
	print '<th>Reviews</th>'
	if type != 'year':
                print '<th>Year</th>'
	print '<th>Title</th>'
	print '<th>Type</th>'
	print '<th>Authors</th>'
	print '</tr>'
        printTableBody(reviews, type, display_year, decade)
	print '</table>'
	
	PrintTrailer('top', 0, 0)

