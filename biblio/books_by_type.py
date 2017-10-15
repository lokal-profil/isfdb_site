#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2015   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2015/02/13 04:45:05 $


import sys
import os
import string
from SQLparsing import *
from biblio import *
from operator import itemgetter
from library import outputGraph
from collections import defaultdict


def oneType(type, startyear, bytype):
        results = []
        for year in bytype[type]:
                percent = bytype[type][year] * 100 / total[year]
                tuple = (int(year) - startyear, percent)
                results.append(tuple)
        return results

if __name__ == '__main__':

	PrintHeader('Percent of Books by Type by Year')
	PrintNavbar('books_by_type', 0, 0, 'books_by_type.cgi', 0)

        print '<h3>Legend: Red - novels, Blue - collections, Green - anthologies, Yellow - omnibuses, Orange - chapbooks</h3>'
	# Set the start year to 1900
	startyear = 1900
	# Set the end year to the current year
	endyear = localtime()[0]

        # Retrieve the data from the database
        query = 'select YEAR(title_copyright),title_ttype,count(*) from titles where YEAR(title_copyright)>%d' % (startyear-1)
        query += ' and YEAR(title_copyright)<%d and (title_ttype="ANTHOLOGY" or title_ttype="NOVEL" or' % (endyear+1)
        query += ' title_ttype="COLLECTION" or title_ttype="CHAPBOOK" or title_ttype="OMNIBUS") and title_parent=0 group by'
        query += ' YEAR(title_copyright),title_ttype'
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
	total = AutoVivification()
        bytype = AutoVivification()
        while record:
            year = record[0][0]
            type = record[0][1]
            count = record[0][2]
            if not total[year]:
                    total[year] = 0
            total[year] += count
            if not bytype[type][year]:
                    bytype[type][year] = 0
            bytype[type][year] += count
            record = result.fetch_row()

        # Add any missing years
        for type in bytype.keys():
                for year in range(startyear,endyear+1):
                        if year not in bytype[type]:
                                bytype[type][year] = 0

        results_dict = {}
        results_dict['red'] = oneType('NOVEL', startyear, bytype)
        results_dict['blue'] = oneType('COLLECTION', startyear, bytype)
        results_dict['green'] = oneType('ANTHOLOGY', startyear, bytype)
        results_dict['yellow'] = oneType('OMNIBUS', startyear, bytype)
        results_dict['orange'] = oneType('CHAPBOOK', startyear, bytype)

        minimum = 0
        maximum = 100

	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(maximum-minimum)
	outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

	PrintTrailer('frontpage', 0, 0)
