#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2017   Al von Ruff, Bill Longley and Ahasuerus
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
from login import *
from seriesClass import *


def DoError(text):
        PrintHeader("Series Error")
        PrintNavbar('seriesName', 0, 0, 'pe.cgi', 0)
        print '<h2>Error: %s.</h2>' % text
        PrintTrailer('series', 0, 0)
        sys.exit(0)

#########################################################
# printSeries is a recursive function that outputs the
# titles attached to the given series, then finds all
# of its children and calls itself with each child.
#########################################################
def printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                variantTitles, variantSerials, parentsWithPubs,
                variantAuthors, translit_titles, translit_authors, ser, user):
        output = '<li>'
	if ser.series_parentposition > 0:
		output += '%s ' % ser.series_parentposition
        output += '<a href="http:/%s/pe.cgi?%s" dir="ltr">%s</a>' % (HTFAKE, ser.series_id, ser.series_name)
        print output
        magazine_found = 0
        for ser_id in seriesTitles:
                # If any of the Titles in this series or its sub-series is
                # an EDITOR title, display a link to the magazine's issue grid
                for title in seriesTitles[ser_id]:
                        if title[TITLE_TTYPE] == 'EDITOR':
                                print '<a href="http:/%s/seriesgrid.cgi?%s" dir="ltr"> (View Issue Grid)</a>' % (HTFAKE, ser.series_id)
                                magazine_found = 1
                                break
                if magazine_found:
                        break
        print "<ul>"
        if ser.series_id in seriesTitles:
                for title in seriesTitles[ser.series_id]:
                        # Display the series number
                        output = '<li>'
                        if title[TITLE_SERIESNUM] is not None:
                                output += '%s' % title[TITLE_SERIESNUM]
                        if title[TITLE_SERIESNUM_2] is not None:
                                output += '.%s' % title[TITLE_SERIESNUM_2]
                        print output
                        # The "non-genre" parameter is set to 0 because for series biblios the
                        # non-genre flag is always displayed
                        displayTitle(title, 0, parentAuthors, SERIES_TYPE_UNKNOWN, variantTitles,
                                     variantSerials, parentsWithPubs, variantAuthors, translit_titles,
                                     translit_authors, user)
	print "</ul>"

	children = seriesTree[ser.series_id]
	if children:
		print "<ul>"
		for child_id in children:
                        ser1 = seriesData[child_id]
			printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                                    variantTitles, variantSerials, parentsWithPubs,
                                    variantAuthors, translit_titles, translit_authors,
                                    ser1, user)
		print "</ul>"

if __name__ == '__main__':

	#############################################
	# Get the series argument. May be a series 
	# name or a record number
	#############################################
	try:
		argument = unescapeLink(sys.argv[1])
	except:
                DoError('No series specified')

	################################################
	# Translate name to a series number if necessary
	################################################
	try:
		seriesId = int(argument)
		seriesName = SQLFindSeriesName(seriesId)
		if not seriesName:
                        raise
	except:
		try:
			seriesName = argument
			seriesId = SQLFindSeriesId(argument)
			if not seriesId:
                                raise
		except:
                        DoError('Series not found')

        ser = series(db)
        ser.load(seriesId)

        user = User()
        user.load()

        # Check if the user is trying to change the default settings for translations
        try:
                translations = sys.argv[2]
                user.translation_cookies(translations)
        except:
                pass

	PrintHeader("Series: %s" % seriesName)
	PrintNavbar('series', seriesId, 0, 'pe.cgi', ser.series_id)

        (seriesData, seriesTitles, seriesTree, parentAuthors,
         seriesTags, variantTitles, variantSerials, parentsWithPubs,
         variantAuthors, translit_titles, translit_authors) = ser.BuildTreeData(user)

        ser.PrintMetaData(user, 'brief', seriesTags, 'series')

        print '<div class="ContentBox">'
        if seriesData:
                print user.translation_message('series', ser)
                # Traverse and print series tree
                print "<ul>"
                printSeries(seriesData, seriesTitles, seriesTree, parentAuthors,
                            variantTitles, variantSerials, parentsWithPubs,
                            variantAuthors, translit_titles, translit_authors,
                            ser, user)
                print "</ul>"
        else:
                print '<p><b>This series is empty and will be deleted.</b>'

        print '</div>'

	PrintTrailer('series', 0, 0)
