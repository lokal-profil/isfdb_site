#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2017/03/30 18:40:53 $


from SQLparsing import *
from common import *
from library import *
from seriesClass import *


if __name__ == '__main__':

	try:
		series_id = int(sys.argv[1])
        	series_name = SQLFindSeriesName(series_id)
        	if not series_name:
                        raise
	except:
		PrintHeader("Invalid or non-existing series ID")
		PrintNavbar('seriestags', 0, 0, 'seriestags.cgi', 0)
		PrintTrailer('seriestags', 0, 0)
		sys.exit(0)

	PrintHeader("All Tags for Series %s" % series_name)
	PrintNavbar('seriestags', 0, 0, 'seriestags.cgi', series_id)

        ser = series(db)
        ser.load(series_id)

        user = User()
        user.load()

        (seriesData, seriesCanonicalTitles, seriesTree, parentAuthors,
                        seriesTags, variantTitles, variantSerials, parentsWithPubs, variantAuthors,
                        translit_titles, translit_authors) = ser.BuildTreeData(user)

        ser.PrintMetaData(user, 'full', seriesTags, 'tags')

	PrintTrailer('seriestags', series_id, series_id)
