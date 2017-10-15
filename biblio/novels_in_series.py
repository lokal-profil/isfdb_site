#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/02/15 07:12:23 $


import sys
import os
import string
from SQLparsing import *
from biblio import *
from operator import itemgetter
from library import outputGraph


def oneType(title_type, startyear, endyear):
        query = 'select substring(title_copyright,1,4),count(*) as total, count(series_id>0)'
        query += ' as in_series, count(series_id>0)/count(*)*100 as ratio from titles where'
        query += ' title_ttype="%s" and substring(title_copyright,1,4)>%d and' % (title_type, startyear-1)
        query += ' substring(title_copyright,1,4)<%d and title_parent=0 group by substring(title_copyright,1,4)' % (endyear+1)

        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
	results = []
        while record:
            year = record[0][0]
            percent = record[0][3]
            tuple = (int(year)-startyear, int(round(float(percent))))
            results.append(tuple)
            record = result.fetch_row()
        return results

if __name__ == '__main__':

	PrintHeader('Percent of Titles in Series by Year')
	PrintNavbar('novels_in_series', 0, 0, 'novels_in_series.cgi', 0)

        print '<h3>Legend: Red - novels, Blue - short fiction</h3>'
	# Set the start year to 1900
	startyear = 1900
	# Set the end year to the current year
	endyear = localtime()[0]

        results_dict = {}
        results_dict['red'] = oneType('NOVEL', startyear, endyear)
        results_dict['blue'] = oneType('SHORTFICTION', startyear, endyear)

        minimum = 0
        maximum = 100

	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(maximum-minimum)
	outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

	PrintTrailer('frontpage', 0, 0)
