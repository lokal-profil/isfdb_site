#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2017   Ahasuerus and Dirk Stoecker
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
from common import *
from seriesClass import *
from library import ISFDBLink

def BuildDictionary(titles, arr):
        """Add all pubs for a given list of titles to the nested dictionary"""
	for title in titles:
                # Retrieve all pubs for this EDITOR title, including the parent title's pubs
                pubs = SQLGetPubsByTitle(title[TITLE_PUBID])
                for pub in pubs:
                        year = pub[PUB_YEAR][0:4]
                        month = pub[PUB_YEAR][5:7]
                        day = pub[PUB_YEAR][8:10]
                        arr[year][month][day][pub[PUB_PUBID]]=pub
        return

def OneYear(year, arr, bgcolor):
        print '<tr align=center class="table%d">' % (bgcolor+1)
        print '<th class="year">%s</th>' % convertYear(year)
        for month in list_months:
                if not arr[year].has_key(unicode(month)):
                        print '<td>-</td>'
                        continue
                # Create a nested table
                print '<td class="seriesgridinner"><table class="seriesgridinner">'
                for day in sorted(arr[year][month]):
                        for pub_id in sorted(arr[year][month][day]):
                                # Retrieve the publication record
                                pub = arr[year][month][day][pub_id]
                                # Retrieve the full title of the publication and save it off
                                # in case the stipping algorithm strips all text
                                title = pub[PUB_TITLE]
                                original_title = title
                                # Find the first place where a comma occurs
                                comma = title.find(',')
                                if comma != -1:
                                        # If we found a comma, then strip everything up to it
                                        title = title[comma+1:]
                                # Convert the title to a list
                                list_title = title.split()
                                # 
                                # Extract the last word from the title
                                last_word = list_title[len(list_title)-1]
                                # Check if the last word in the title is the same as the pub year
                                # If it is, then strip it
                                if last_word == year:
                                        title = title[0:len(title)-4]
                                # Strip leading and trailing punctuation
                                title = StripLeadingTrailing(title)
                                # If the stipping algorithm stripped all text, restore the original title
                                if not title:
                                        title = original_title
                                # Get the verification status: 0 - not verified, 1 - primary, 2 - secondary
                                verified = SQLVerificationStatus(pub[PUB_PUBID])
                                color = "notverified"
                                if verified == 1:
                                        color = "verifiedprimary"
                                elif verified == 2:
                                        color = "verifiedsecondary"
                                print '<tr class="seriesgridinner">'
                                print '<td class="%s">%s</td>' % (color, ISFDBLink("pl.cgi", pub[PUB_PUBID], title))
                                print '</tr>'
                # Close the nested table
                print '</table></td>'
        print '</tr>'
        return

def StripLeadingTrailing(title):
        # Check every character in the string starting with 1
        count = -1
        for char in title:
                count += 1
                # If we found a non-punctuation character, stop
                if char not in ' ,.':
                        break
        title = title[count:len(title)]
        
        count = -1
        # Check every character in the reversed string
        for char in title[::-1]:
                count += 1
                if char not in ' ,.':
                        break
        title = title[0:len(title)-count]
        # Handle single character strings
        if title in ' ,.':
                title = ''
        return title


if __name__ == '__main__':

	#############################################
	# Get the series argument. May be a series 
	# name or a record number
	#############################################
	try:
		series_arg = unescapeLink(sys.argv[1])
	except:
		sys.exit(1)

        # Get the Display Order.
        # 1 is "descending", i.e. latest year is dispayed first
        # 0 is "ascending", i.e. first year is displayed first
        # The default is descending
	try:
                displayOrder = int(unescapeLink(sys.argv[2]))
        except:
                displayOrder=1

	#############################################
	# Translate name to a series number if
	# necessary
	#############################################
	try:
		seriesId = int(series_arg)
		seriesName = SQLFindSeriesName(seriesId)
	except:
		try:
			seriesName = series_arg
			seriesId = SQLFindSeriesId(series_arg)
		except:
			PrintHeader("Series Error")
			PrintNavbar('seriesgrid', 0, 0, 'pe.cgi', sys.argv[1])
			print '<h2>Error: Series not found.</h2>'
			PrintTrailer('series', 0, 0)
			sys.exit(1)

	try:
		seriesParent = SQLFindSeriesParent(seriesId)
		seriesParentId = int(seriesParent)
	except:
                pass

        ser = series(db)
        ser.load(seriesId)

        user = User()
        user.load()

	title = "Issue Grid: %s" % seriesName
	PrintHeader(title)
	PrintNavbar('seriesgrid', seriesId, 0, 'pe.cgi', sys.argv[1])

        (seriesData, seriesTitles, seriesTree, parentAuthors,
         seriesTags, variantTitles, variantSerials, parentsWithPubs,
         variantAuthors, translit_titles, translit_authors) = ser.BuildTreeData(user)

        ser.PrintMetaData(user, 'brief', seriesTags, 'grid')

        print '<div class="ContentBox">'
	print '<b>Legend:</b> Unverified issues are gold, secondary verifications are light blue.'

	print '<p class="textindent">%s &#8226; ' % ISFDBLink("pe.cgi", seriesId, "View this magazine as a series")

	if displayOrder:
                print ISFDBLink("seriesgrid.cgi", "%s+0" % seriesId, "Show earliest year first")
        else:
                print ISFDBLink("seriesgrid.cgi", "%s+1" % seriesId, "Show last year first")

        # Retrieve all EDITOR titles for this magazine
	titles = SQLFindSeriesTitles(seriesName)
	arr = AutoVivification()
	BuildDictionary(titles, arr)

        # Retrieve all child series and add them to the array
        children = SQLFindSeriesChildren(seriesId)
        for child in children:
                seriesName=SQLgetSeriesName(child)
        	titles = SQLFindSeriesTitles(seriesName)
        	BuildDictionary(titles, arr)

        print '<table class="seriesgrid">'
        print '<tr><th>&nbsp;</th>'
        for month in sorted(monthmap.keys()):
                print '<th>%s</th>' % (monthmap[month])
        print '<th>No month</th></tr>'
        bgcolor = 0
        list_months = ['01','02','03','04','05','06','07','08','09','10','11','12','00']
        for year in sorted(arr.keys(), reverse=displayOrder):
                bgcolor ^= 1
                OneYear(year, arr, bgcolor)
        
        print '</table>'
        print '</div>'

	PrintTrailer('series', 0, 0)
