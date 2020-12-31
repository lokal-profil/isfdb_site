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
from awardcatClass import *
from awardtypeClass import *

def DoError(message):
        PrintHeader('Unknown Award Category Record')
        PrintNavbar('award_cat', '', 0, 'award_category.cgi', '')
        print """<h3>%s</h3>""" % message
        PrintTrailer('award_cat', '', 0)
        sys.exit(0)

if __name__ == '__main__':

        try:
                cat = award_cat()
                cat.award_cat_id = int(sys.argv[1])
                # 0 stands for 'Win' and 1 stands for 'All awards and nominations'. The default is 0
                if len(sys.argv) == 2:
                        win_nom = 0
                else:
                        win_nom = int(sys.argv[2])
                        if win_nom < 0 or win_nom > 1:
                                raise
	except:
                DoError('Error: Invalid award category or invalid win/nomination status requested')

        cat.load()
        if not cat.award_cat_name:
		if SQLDeletedAwardCategory(cat.award_cat_id):
                        DoError('This award category has been deleted. See %s for details.' % ISFDBLink('award_category_history.cgi', cat.award_cat_id, 'Edit History'))
                else:
                        DoError('Unknown Award Category Record')

        awardType = award_type()
        awardType.award_type_id = cat.award_cat_type_id
        awardType.load()
        if not awardType.award_type_name:
                DoError('Invalid award category')

	PrintHeader('Award Category: %s (%s)' % (cat.award_cat_name, awardType.award_type_name))
	PrintNavbar('award_cat', cat.award_cat_id, cat.award_cat_id, 'award_category.cgi', cat.award_cat_id)

        cat.PrintAwardCatSummary(win_nom)

	PrintTrailer('award_cat', cat.award_cat_id, cat.award_cat_id)
