#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from common import *
from awardClass import *


if __name__ == '__main__':

        award_id = SESSION.Parameter(0, 'int')

        award = awards(db)
        award.load(award_id)
	if not award.award_id:
		if SQLDeletedAward(award_id):
                        SESSION.DisplayError('This award has been deleted. See %s for details.' % ISFDBLink('award_history.cgi', award_id, 'Edit History'))
                else:
                        SESSION.DisplayError('Award Record Does Not Exist')

	PrintHeader('Award Details')
	PrintNavbar('award', award.award_id, award.award_type_id, 'award_details.cgi', award.award_id)

        award.PrintAwardSummary()

	print '<p>'

	PrintTrailer('award', award_id, award_id)
