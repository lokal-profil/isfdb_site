#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
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
from awardClass import *


if __name__ == '__main__':

        try:
                award_id = int(sys.argv[1])
                award = awards(db)
                award.load(award_id)
                if not award.award_id:
                        raise
	except:
		PrintHeader('Award Error')
		PrintNavbar('award', '', 0, 'award.cgi', '')
                print '<h2>Error: Award not found.</h2>'
		PrintTrailer('award', '', 0)
		sys.exit(0)

	PrintHeader('Award Details')
	PrintNavbar('award', award.award_id, award.award_type_id, 'award_details.cgi', award.award_id)

        award.PrintAwardSummary()

	print '<p>'

	PrintTrailer('award', award_id, award_id)
