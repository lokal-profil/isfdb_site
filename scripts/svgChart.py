#!/usr/bin/python
#    (C) COPYRIGHT 2008   Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#

import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *


def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)


def outputGraph(height, startyear, xscale, yscale, years, max, results):

	xoffset = 15
	yoffset = 10

	print '<svgcode width="%d" height="%d" version="1.1">' % (xoffset+40+(years*xscale), height+30+yoffset)
	print '<svg width="100%" height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg">'

	###################################################
	# Output the grid and labels - Horizontal Lines
	###################################################
	y = 0
	increment = max/4
	value = increment * 4
	while y <= height:
		print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:gray;stroke-width:1"/>' % (xoffset, y+yoffset, xoffset+5+(years*xscale), y+yoffset)
		print '<text x="%d" y="%d" font-size="10">%d</text>' % (xoffset+10+(years*xscale), y+5+yoffset, value)
		value -= increment
		y = y + 50

	###################################################
	# Output the grid and labels - Vertical Lines
	###################################################
	x = 0
	while x < years:
		print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:gray;stroke-width:1"/>' % (xoffset+(xscale*x), yoffset, xoffset+(xscale*x), height+10+yoffset)
		print '<text x="%d" y="%d" font-size="10">%d</text>' % ((xscale*x)-12+xoffset, height+20+yoffset, x+startyear)
		x += 10

	###################################################
	# Output the data
	###################################################
	#print results
	index = 0
	last = (0, 0)
	while index < years:
		if index:
			print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:black;stroke-width:2"/>' % (xoffset+(xscale * last[0]), yoffset+(int(yscale * float(last[1]))), xoffset+(xscale * results[index][0]), yoffset+(int(yscale * float(max-results[index][1]))))
		last = (results[index][0], max-results[index][1])
		index += 1

	print '</svg>'
	print '</svgcode>'


def doVerifiedPubs(startyear, endyear):

	results = []
	year = startyear
	max = 100
	min = 0
	while year <= endyear:

		################################################
		# Obtain the total number of pubs that year
		################################################
		query = "select count(*) from pubs where YEAR(pub_year)='%d'" % year
		db.query(query)
		result = db.store_result()
		record = result.fetch_row()
		pubs = record[0][0]

		################################################
		# Obtain the number of verified pubs that year
		################################################
		query = "select count(verification.verification_id) from verification,pubs where verification.reference_id='1' and verification.ver_status='1' and verification.pub_id=pubs.pub_id and YEAR(pubs.pub_year)='%d'" % year
		db.query(query)
		result = db.store_result()
		record = result.fetch_row()
		verified_pubs = record[0][0]
		if pubs:
			average = (100 * verified_pubs) / pubs
		else:
			average = 0

		tuple = (year-startyear, average)
		#print verified_pubs, pubs, tuple
		results.append(tuple)
		year += 1

	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(max-min)
	outputGraph(height, startyear, xscale, yscale, years, max, results)


def doEverythingElse(startyear, endyear):
	results = []
	year = startyear
	max = 0
	min = 999999
	while year <= endyear:
		if sys.argv[1] == "novels":
			query = "select COUNT(*) from titles where title_ttype='NOVEL' and YEAR(title_copyright)='%d'" % year
		elif sys.argv[1] == "shortfiction":
			query = "select COUNT(*) from titles where title_ttype='SHORTFICTION' and YEAR(title_copyright)='%d'" % year
		elif sys.argv[1] == "reviews":
			query = "select COUNT(*) from titles where title_ttype='REVIEW' and YEAR(title_copyright)='%d'" % year
		elif sys.argv[1] == "pubs":
			query = "select COUNT(*) from pubs where YEAR(pub_year)='%d' and pub_ctype<>'MAGAZINE'" % year
		elif sys.argv[1] == "magazines":
			query = "select COUNT(*) from pubs where YEAR(pub_year)='%d' and pub_ctype='MAGAZINE'" % year
		else:
			print "Bad argument"
			sys.exit(0)

		db.query(query)
		result = db.store_result()
		record = result.fetch_row()
		if record[0][0] > max:
			max = record[0][0]
		if record[0][0] < min:
			min = record[0][0]
		tuple = (year-startyear, record[0][0])
		results.append(tuple)
		year += 1

	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(max-min)
	outputGraph(height, startyear, xscale, yscale, years, max, results)


if __name__ == '__main__':

	db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
	db.select_db(DBASE)

	startyear = 1910
	endyear   = 2010

	if sys.argv[1] == "verif":
		doVerifiedPubs(startyear, endyear)
	else:
		doEverythingElse(startyear, endyear)

	db.close()
