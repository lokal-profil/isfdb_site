#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import sys
import os
import string
from SQLparsing import *
from common import *
from awardcatClass import *
from awardtypeClass import *


if __name__ == '__main__':

        try:
                cat = award_cat()
                cat.award_cat_id = int(sys.argv[1])
                cat.load()
                if not cat.award_cat_name:
                        raise
                awardType = award_type()
                awardType.award_type_id = cat.award_cat_type_id
                awardType.load()
                if not awardType.award_type_name:
                        raise
                year = int(sys.argv[2])
	except:
		PrintHeader('Award Category Error')
		PrintNavbar('award_category_year', '', 0, 'award_category_year.cgi', '')
                print '<h2>Error: Invalid award category or year specified.</h2>'
		PrintTrailer('award_category_year', '', 0)
		sys.exit(0)

	PrintHeader('Award Category: %d %s (%s)' % (year, cat.award_cat_name, awardType.award_type_name))
	PrintNavbar('award_cat', cat.award_cat_id, cat.award_cat_id, 'award_category.cgi', cat.award_cat_id)

        cat.PrintAwardCatYear(year)

	PrintTrailer('award_category_year', cat.award_cat_id, cat.award_cat_id)
