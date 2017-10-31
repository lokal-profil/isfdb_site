#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2017   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string

from isfdb import *
from SQLparsing import *
from common import *
from awards import PrintOneList
from awardtypeClass import *


def AllAwards(award_Type, year):
        # Display a grid of all years when the award was given
        award_Type.display_table_grid(year)

	all_awards = SQLloadAwardsForYearType(award_Type.award_type_id, year)

	if len(all_awards) == 0:
		print "<h2>No awards available for %s</h2>" % (year)
		return

	print '<table>'

	while all_awards:
                # Get the name of the category of the first award in the list;
                # it will be the category that we will be processing in this iteration of the while loop
		name = all_awards[0][AWARD_NOTEID+1]
		counter = 0
		# Create a list of awards for the current category only
		awards_for_category = []
		while counter < len(all_awards):
			if all_awards[counter][AWARD_NOTEID+1] == name:
				awards_for_category.append(all_awards[counter])
				del all_awards[counter]
			else:
				counter += 1
		if awards_for_category:
                        # Print awards for one category
                        print '<tr>'
                        print '<td colspan=3> </td>'
                        print '</tr>'
                        print '<tr>'
                        print '<td colspan=3><b><a href="http:/%s/award_category.cgi?%s+0">%s</a></b></td>' \
                              % (HTFAKE, awards_for_category[0][AWARD_CATID], awards_for_category[0][AWARD_NOTEID+1])
                        print '</tr>'
                        PrintOneList(awards_for_category)

	print '</table>'


if __name__ == '__main__':

        award_Type = award_type()
	try:
                # If there were 2 arguments passed, then it's Award Type ID+YYYY
                if len(sys.argv) == 3:
                        year = int(sys.argv[2])
                        award_Type.award_type_id = int(sys.argv[1])
                        award_Type.load()
                        if not award_Type.award_type_name:
                                raise
                # If there was only one argument passed, then it must be ZzYYYY where 'Zz' is the award code
                elif len(sys.argv) == 2:
                        year = int(sys.argv[1][2:])
                        award_Type.award_type_code = sys.argv[1][:2]
                        award_Type.load()
                        if not award_Type.award_type_id:
                                raise
                else:
                        raise
	except:
		PrintHeader('Award Error')
        	PrintNavbar('award', 0, 0, 'ay.cgi', 0)
		print "<h3>Specified award type does not exist</h3>"
        	PrintTrailer('award', 0, 0)
		sys.exit(0)

        title = '%s %s' % (year, award_Type.award_type_name)
        PrintHeader(title)
	PrintNavbar('award', 0, award_Type.award_type_id, 'ay.cgi', 0)
	AllAwards(award_Type, year)
	print '<p>'
	PrintTrailer('award', 0, 0)

