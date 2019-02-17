#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2019   Al von Ruff and Ahasuerus
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
from awardtypeClass import award_type


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
	award_Type.display_awards_for_year(year)
	print '<p>'
	PrintTrailer('award', 0, 0)

