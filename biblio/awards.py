#
#     (C) COPYRIGHT 2004-2019   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string
import urllib

from isfdb import *
from library import ISFDBLink
from SQLparsing import *
from utils import *
from library import SpecialAwards


def PrintOneList(awards):
        # Print the awards for one list, which may be for one category, one year or one category/year
	special_awards = SpecialAwards()
	last_level = 1
	for level in range(1,100):
		for award in awards:
			if int(award[AWARD_LEVEL]) == level:
                                # Skip any records whose level is over 70 and not a recognized "special" level
                                if level > 70 and str(level) not in special_awards:
                                        pass
                                else:
                                        # If this is the first occurrence of a new "special" level, display its special message
                                        if str(level) in special_awards and level != last_level:
                                                print '<tr>'
                                                print '<td colspan=3><i>--- ' + special_awards[str(level)] + ' -------</i></td>'
                                                print '</tr>'
                                        Print1Award(award)
                                last_level = level

def Print1Award(record):
        from awardClass import awards
        award = awards(db)
        award.load(record[AWARD_ID])

	bold = 0
	print '<tr>'
	# Do not display the award level of "special" levels; they are displayed separately as headers
	if int(award.award_level) > 70:
                award_link = '*'
	elif award.award_type_poll == 'Yes':
                award_link = award.award_level
	else:
		if award.award_level == '1':
                        award_link = '<b>Win</b>'
			bold = 1
		else:
                        award_link = 'Nomination'

        print '<td><a href="http:/%s/award_details.cgi?%s">%s</a>' % (HTFAKE, award.award_id, award_link)
        if bold:
                print '</b>'
        print '</td>'
	
	if bold:
		print '<td><b>'
	else:
		print '<td>'

	if award.award_title == 'untitled':
		print '----'
	else:
		if award.title_id:
                        # Retrieve the title data associated with this award
                        title = SQLloadTitle(award.title_id)
			print ISFDBLink("title.cgi", award.title_id, title[TITLE_TITLE])
                        if title[TITLE_PARENT]:
                                parent = SQLloadTitle(title[TITLE_PARENT])
                                if title[TITLE_LANGUAGE] and parent[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != parent[TITLE_LANGUAGE]:
                                        print ' (translation of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE])
                                elif parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                        print ' (variant of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE])
		else:
                        print award.award_title

	if award.award_movie:
                print '(<a href="http://www.imdb.com/title/%s/" target="_blank">IMDB</a>)' % award.award_movie

	if bold:
		bold = 0
		print '</b></td>'
	else:
		print '</td>'
	print '<td>'

        award.PrintAwardAuthors()
 
	print '</td>'
	print '</tr>'
