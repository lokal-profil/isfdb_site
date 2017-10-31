#
#     (C) COPYRIGHT 2004-2017   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
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


def TitlesSortedByAwards(requested_type, span, decade, display_year):

        #####################################################################
        # STEP 1 - Retrieve all award types to see which ones are "polls"
        #####################################################################

        poll_awards = list_of_poll_awards()

        #####################################################################
        # STEP 2 - Calculate the award scores for ALL award-related title IDs
        #####################################################################
        
        # Initialize the dictionary which will hold award scores for title IDs
        scores = {}
        
        # Get a list of awards considered "repeating"
        repeating_awards = list_of_repeating_awards()
        # Initilialize the dictionary of "repeating" nominations -- see below for handling details
        repeating = {}
        
        query = "select ta.title_id, a.award_level, a.award_type_id from title_awards as ta, awards as a where ta.award_id=a.award_id"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
	while record:
                title_id = record[0][0]
                award_level = int(record[0][1])
                award_type_id = int(record[0][2])
                score = 0
                # Wins and 1st places get 50 points
                if award_level == 1:
                        score = 50
                # "Special" awards get 1 point
                elif award_level > 70:
                        score = 1
                # Nominations for non-poll awards get 35 points
                elif award_type_id not in poll_awards:
                        score = 35
                # For polls, use 35 for the second place and "33-place" for third and lower places with a minimum of 1 point
                else:
                        if award_level == 2:
                                score = 35
                        else:
                                score = 33 - award_level
                                if score < 1:
                                        score = 1
                # For "repeating" awards, only record the highest score for this title ID
                if award_type_id in repeating_awards:
                        if title_id not in repeating:
                                repeating[title_id] = score
                        elif score > repeating[title_id]:
                                repeating[title_id] = score
                # For all other awards, simply add this award's score to the cumulative score for the title
                else:
                        scores[title_id] = scores.get(title_id, 0) + score
        	record = result.fetch_row()


        # Add "repeating" scores for each title
        for title_id in repeating:
                scores[title_id] = scores.get(title_id, 0) + repeating[title_id]

        ##################################################################
        # STEP 3 - Retrieve title data and delete wrong title types
        ##################################################################

        # Build a string of all retrieved title IDs to be used in an SQL IN clause
        list_of_ids = []
        for key in scores.keys():
                list_of_ids.append(str(key))
        string_of_ids = ','.join(list_of_ids)
        # Initialize the dictionary that will hold year data
        years = {}
        # Initialize the list of parent title IDs
        parents = {}
        query = "select title_id, YEAR(title_copyright), title_ttype, title_parent from titles where title_id in (%s)" % string_of_ids
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
	while record:
                title_id = record[0][0]
                year = record[0][1]
                ttype = record[0][2]
                parent_id = record[0][3]
                # Check if this title has the requested title type
                if EligibleTitleType(requested_type, ttype):
                        # Preserve this title's year; later we will compare it with the year of its parent
                        years[title_id] = year
                        # If this title is a VT, add its parent to the list of parents to be retrieved later
                        if parent_id:
                                if parent_id not in scores:
                                        scores[parent_id] = 0
                                if parent_id not in parents:
                                        parents[parent_id] = [title_id]
                                else:
                                        parents[parent_id].append(title_id)
                else:
                        del scores[title_id]
        	record = result.fetch_row()

        ##################################################################
        # STEP 4 - Retrieve and merge parents and variants
        ##################################################################

        list_of_parents = []
        for key in parents.keys():
                list_of_parents.append(str(key))
        string_of_parents = ','.join(list_of_parents)
        # Retrieve the parents of currently selected titles which are VTs
        query = "select title_id, YEAR(title_copyright) from titles where title_id in (%s)" % string_of_parents
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()
	while record:
                parent_id = record[0][0]
                parent_year = record[0][1]
                for variant_id in parents[parent_id]:
                        variant_year = years[variant_id]
                        # Check all variants and find the earliest year for this title
                        if variant_year < parent_year:
                                parent_year = variant_year
                        # Add the variant's score to the parent's if the parent and variant are of the requedted type
                        if parent_id in scores and variant_id in scores:
                                scores[parent_id] += scores[variant_id]
                        # Delete the variant's score
                        del scores[variant_id]
                years[parent_id] = parent_year
        	record = result.fetch_row()

        ###################################################################
        # STEP 5 - Delete titles that do not match the requested date range
        ###################################################################

        # Initialize the list which will hold the title IDs, years and scores to display
        final = []
        for title_id in scores:
                # Check that this title ID's title record exists in case we have a dangling record in title_awards
                year = years.get(title_id, '')
                if not year:
                        continue
                score = scores[title_id]
                if span == 'all':
                        final.append((score, year, title_id))
                elif span == 'pre1950':
                        if year < 1950:
                                final.append((score, year, title_id))
                elif span == 'decade':
                        if (year/10) == (decade/10):
                                final.append((score, year, title_id))
                elif span == 'year':
                        if year == display_year:
                                final.append((score, year, title_id))
        return final

def EligibleTitleType(requested_type, current_type):
        # Returns 1 if the title's type makes it eligible for display given the user's request, 0 otherwise
        if requested_type == 0:
                return 1
        types = {}
        types[1] = 'NOVEL'
        types[2] = 'SHORTFICTION'
        types[3] = 'COLLECTION'
        types[4] = 'ANTHOLOGY'
        types[5] = 'NONFICTION'
        if requested_type in types and types[requested_type] == current_type:
                return 1
        if requested_type == 6:
                for type in types:
                        if types[type] == current_type:
                                return 0
                return 1
        return 0

def list_of_poll_awards():
        polls = []
        query = "select award_type_id, award_type_poll from award_types where award_type_poll='Yes'"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                award_type_id = record[0][0]
                award_type_poll = record[0][1]
                polls.append(award_type_id)
                record = result.fetch_row()
        return polls

def list_of_repeating_awards():
        # Some awards are a special case since titles can be nominated many times before they win. We
        # will record them in a separate dictionary and count them once per title (wins trump nominations.)
        # At this time, the only "repeating" award is Prometheus Hall of Fame

        repeating_awards = []
        query = "select award_type_id from award_types where award_type_name='Prometheus Award'"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                award_type_id = record[0][0]
                repeating_awards.append(award_type_id)
                record = result.fetch_row()
        return repeating_awards

def PrintOneList(awards):
        # Print the awards for one list, which may be for one category or for one year
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
