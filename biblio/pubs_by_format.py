#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


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

	PrintHeader('Percent of Publications by Format by Year')
	PrintNavbar('pubs_by_format', 0, 0, 'pubs_by_format.cgi', 0)

        print '<h3>Legend:'
        print 'Red - %s, ' % ISFDBPubFormat('pb')
        print 'Blue - %s, ' % ISFDBPubFormat('tp')
        print 'Green - %s, ' % ISFDBPubFormat('hc')
        print 'Yellow - %s, ' % ISFDBPubFormat('pulp')
        print 'Orange - %s, ' % ISFDBPubFormat('digest')
        print 'Pink - %s, ' % ISFDBPubFormat('ebook')
        print 'Black - all other formats'
	# Set the start year to 1900
	startyear = 1900
	# Set the end year to the last year (current year may not have enough data points)
	endyear = localtime()[0]-1
	# Define recognize formats
	recognized = ('pb','tp','hc','pulp','digest','ebook')

        # Retrieve the data from the database
        query = """select YEAR(pub_year), pub_ptype, count(*)
                   from pubs where YEAR(pub_year)>%d
                   and YEAR(pub_year)<%d and pub_ptype!="unknown"
                   group by pub_ptype, YEAR(pub_year)""" % (startyear-1, endyear+1)
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
            if type not in recognized:
                    type = 'other'
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
        results_dict['red'] = oneType('pb', startyear, bytype)
        results_dict['blue'] = oneType('tp', startyear, bytype)
        results_dict['green'] = oneType('hc', startyear, bytype)
        results_dict['yellow'] = oneType('pulp', startyear, bytype)
        results_dict['orange'] = oneType('digest', startyear, bytype)
        results_dict['black'] = oneType('other', startyear, bytype)
        results_dict['pink'] = oneType('ebook', startyear, bytype)

        minimum = 0
        maximum = 100

	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(maximum-minimum)
	outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

	PrintTrailer('frontpage', 0, 0)
