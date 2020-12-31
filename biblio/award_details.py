#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2020   Ahasuerus
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


def DoError(message):
        PrintHeader('Unknown Award Record')
        PrintNavbar(0, 0, 0, 'award_details.cgi', 0)
        print """<h3>%s</h3>""" % message
        PrintTrailer('award_details', 0, 0)
        sys.exit(0)

if __name__ == '__main__':

        try:
                award_id = int(sys.argv[1])
	except:
                DoError('Bad Argument')

        award = awards(db)
        award.load(award_id)
	if not award.award_id:
		if SQLDeletedAward(award_id):
                        DoError('This award has been deleted. See %s for details.' % ISFDBLink('award_history.cgi', award_id, 'Edit History'))
                else:
                        DoError('Unknown Award Record')

	PrintHeader('Award Details')
	PrintNavbar('award', award.award_id, award.award_type_id, 'award_details.cgi', award.award_id)

        award.PrintAwardSummary()

	print '<p>'

	PrintTrailer('award', award_id, award_id)
