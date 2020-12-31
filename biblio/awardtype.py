#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2020   Ahasuerus
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
from awardtypeClass import *
from SQLparsing import SQLloadAwardTypeWebpages, SQLgetNotes
from common import *

def DoError(message):
        PrintHeader('Unknown Award Type Record')
        PrintNavbar('award_type', '', 0, 'awardtype.cgi', '')
        print """<h3>%s</h3>""" % message
        PrintTrailer('award_type', '', 0)
        sys.exit(0)


if __name__ == '__main__':

        try:
                award_type_id = int(sys.argv[1])
	except:
		DoError('Unknown Award Type Record')

        award_type = award_type()
        award_type.award_type_id = award_type_id
        award_type.load()
        if not award_type.award_type_name:
		if SQLDeletedAwardType(award_type_id):
                        DoError('This award type has been deleted. See %s for details.' % ISFDBLink('awardtype_history.cgi', award_type_id, 'Edit History'))
                else:
                        DoError('Unknown Award Type Record')

	title = 'Overview of %s' % award_type.award_type_name
	PrintHeader(title)
	PrintNavbar('award_type', award_type.award_type_id, 0, 'awardtype.cgi', award_type.award_type_id)

	print '<ul>'

        if award_type.award_type_short_name:
                print '<li><b>Short Name:</b>', award_type.award_type_short_name

        #Retrieve this user's data
        user = User()
        user.load()
        printRecordID('Award Type', award_type.award_type_id, user.id, user)

        if award_type.award_type_name:
                print '<li><b>Full Name:</b>', award_type.award_type_name

        if award_type.award_type_for:
                print '<li><b>Awarded For:</b>', award_type.award_type_for

        if award_type.award_type_by:
                print '<li><b>Awarded By:</b>', award_type.award_type_by

        if award_type.award_type_poll:
                print '<li><b>Poll:</b>', award_type.award_type_poll

        if award_type.award_type_non_genre:
                print '<li><b>Covers more than just SF:</b>', award_type.award_type_non_genre

	# Webpages
	webpages = SQLloadAwardTypeWebpages(award_type.award_type_id)
	PrintWebPages(webpages)

	# Note
	if award_type.award_type_note:
		print '<li>'
		print FormatNote(award_type.award_type_note, 'Note', 'short', award_type.award_type_id, 'AwardType')

	print "</ul>"

	print "<p>"
                
        # Display a grid of all years when the award was given
        award_type.display_table_grid()
        # Display a list of all categories for this award
        award_type.display_categories()

	PrintTrailer('award_type', award_type.award_type_id, award_type.award_type_id)
