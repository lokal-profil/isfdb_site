#
#     (C) COPYRIGHT 2005-2017   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.35 $
#     Date: $Date: 2017/07/11 22:19:53 $

import cgi
import sys
import os
import MySQLdb
import urllib
from isfdb import *
from library import *
from xml.dom import minidom
from xml.dom import Node
from SQLparsing import *



class awards:
	def __init__(self, db):
		self.db = db
		self.used_id         = 0
		self.used_title      = 0
		self.used_year       = 0
		self.used_cat_id     = 0
		self.used_cat_name   = 0
		self.used_level	     = 0
		self.used_movie	     = 0
                self.used_title_id   = 1
		self.num_authors     = 0
                self.used_type_name  = 0
                self.used_type_short_name = 0
                self.used_type_id    = 0
                self.used_type_poll  = 0
                self.used_note_id    = 0
                self.used_note       = 0
                
		self.award_authors    = []
		self.award_id         = ''
		self.title_id         = ''
		self.award_title      = ''
		self.award_year       = ''
		self.award_cat_id     = ''
		self.award_cat_name   = ''
		self.award_level      = ''
		self.award_displayed_level = ''
		self.award_movie      = ''
                self.award_type_name  = ''
                self.award_type_short_name = ''
                self.award_type_id    = ''
                self.award_type_poll  = ''
                self.award_note_id    = ''
                self.award_note       = ''

                self.error = ''

	def authors(self):
		counter = 0
		retval = ''
		while counter < self.num_authors:
			if counter == 0:
				retval = self.award_authors[counter]
			else:
				retval += "+" + self.award_authors[counter]
			counter += 1
		return retval

	def load(self, id):
		self.loadCommon(id, 0)

	def loadXML(self, id):
		self.loadCommon(id, 1)

	def loadCommon(self, id, doXML):
		if id == 0:
			return
                award = SQLloadAwards(id)
		if award:
                        award = award[0]
			if award[AWARD_ID]:
				self.award_id = award[AWARD_ID]
				self.used_id = 1
                                title = SQLloadTitleFromAward(self.award_id)
                                if title:
                                        self.title_id = title[0][TITLE_PUBID]
                                        self.used_title_id = 1
			if award[AWARD_TITLE]:
				self.award_title = award[AWARD_TITLE]
				self.used_title = 1
			if award[AWARD_YEAR]:
				self.award_year = award[AWARD_YEAR]
				self.used_year = 1
			if award[AWARD_TYPEID]:
				self.award_type_id = award[AWARD_TYPEID]
				self.used_type_id = 1
				award_type = SQLGetAwardTypeById(self.award_type_id)
				self.award_type_name = award_type[AWARD_TYPE_NAME]
				self.award_type_short_name = award_type[AWARD_TYPE_SHORT_NAME]
				self.used_type_name = 1
				self.award_type_poll = award_type[AWARD_TYPE_POLL]
				self.used_type_poll = 1
			if award[AWARD_LEVEL]:
				self.award_level = award[AWARD_LEVEL]
                                self.used_level = 1
                                self.award_displayed_level = ''
                                if int(self.award_level) > 70:
                                        special_awards = SpecialAwards()
                                        self.award_displayed_level = special_awards[self.award_level]
                                elif self.award_type_poll == 'Yes':
                                                self.award_displayed_level = self.award_level
                                else:
                                        if int(self.award_level) == 1:
                                                self.award_displayed_level = 'Win'
                                        else:
                                                self.award_displayed_level = 'Nomination'
                        if award[AWARD_CATID]:
                                self.award_cat_id = award[AWARD_CATID]
                                self.used_cat_id = 1
                                self.award_cat_name = SQLGetAwardCatById(self.award_cat_id)[AWARD_CAT_NAME]
                                self.used_cat_name = 1
			if award[AWARD_MOVIE]:
				self.award_movie = award[AWARD_MOVIE]
				self.used_movie = 1
			if award[AWARD_AUTHOR]:
				authors = string.split(award[AWARD_AUTHOR], '+')
				self.num_authors = 0
				for author in authors:
					self.award_authors.append(author)
					self.num_authors += 1
                        if award[AWARD_NOTEID]:
                                note = SQLgetNotes(award[AWARD_NOTEID])
                                if note:
                                        self.award_note_id = award[AWARD_NOTEID]
                                        self.used_note_id = 1
                                        self.award_note = note
                                        self.used_note = 1

		else:
			print "ERROR: award record not found: ", id
			self.error = 'Award record not found'
			return

	def cgi2obj(self):
		self.form = cgi.FieldStorage()
		if self.form.has_key('award_id'):
			self.award_id = self.form['award_id'].value
			self.used_id = 1

                # title_id is only present for Add (as opposed to Edit) Award submissions
		if self.form.has_key('title_id'):
			self.title_id = self.form['title_id'].value
			self.used_title_id = 1
		
		if self.form.has_key('award_title'):
			self.award_title = XMLescape(self.form['award_title'].value)
			self.used_title = 1
                else:
                        self.award_title = 'untitled'
			self.used_title = 1

		self.num_authors = 0
		self.award_authors = []
		counter = 0
		while counter < 100:
			if self.form.has_key('title_author'+str(counter+1)):
				self.award_authors.append(XMLescape(self.form['title_author'+str(counter+1)].value))
				self.num_authors += 1
			counter += 1

		if self.form.has_key('award_year'):
			year = self.form['award_year'].value
			# Take the submitted value and convert it to the standard YYYY-MM-DD format
			self.award_year = normalizeDate(year)
			if self.award_year == '0000-00-00':
				self.error = "Bad YEAR value"
				return
			self.used_year = 1
		else:
                        self.error = "Missing YEAR value"
                        return

		if self.form.has_key('award_type_id'):
			self.award_type_id = self.form['award_type_id'].value
			self.used_type_id = 1
                else:
                        self.error = "Missing Award Type ID"
                        return

		if self.form.has_key('award_cat_id'):
			self.award_cat_id = self.form['award_cat_id'].value
			self.used_cat_id = 1
                else:
                        self.error = "Missing Award Category ID"
                        return

		if self.form.has_key('LEVEL'):
                        special_awards = SpecialAwards()
			if self.form['LEVEL'].value == 'WIN':
				self.award_level = '1'
				self.used_level = 1
			elif self.form['LEVEL'].value == 'NOM':
				self.award_level = '9'
				self.used_level = 1
			elif self.form['LEVEL'].value == 'LEVEL':
				if self.form.has_key('award_level'):
					try:
                                                self.award_level = self.form['award_level'].value
                                                self.used_level = 1
                                                # Check that the entered value is between 1 and 70
                                                if int(self.award_level) > 70 or int(self.award_level) < 1:
                                                        raise
                                        except:
                                                self.error = "Award level must be an integer number between 1 and 70"
                                                return
                                else:
                                        self.error = "Missing award level value"
                                        return
			elif self.form['LEVEL'].value == 'SPECIAL':
				if self.form.has_key('award_special'):
                                        try:
                                                self.award_level = self.form['award_special'].value
                                                self.used_level = 1
                                                # Check that the entered value is a recognized "special" value
                                                if self.award_level not in special_awards:
                                                        raise
                                        except:
                                                self.error = "Only displayed special award levels are supported"
                                                return
                                else:
                                        self.error = "Missing special award level value"
                                        return

		if self.form.has_key('award_movie'):
			self.award_movie = XMLescape(self.form['award_movie'].value)
			if self.award_movie[:2] != 'tt':
                                self.error = "IMDB title codes must start with 'tt'. See mouseover Help for details"
                                return
			self.used_movie = 1

		if self.form.has_key('award_note'):
			self.award_note = XMLescape(self.form['award_note'].value)
			self.used_note = 1

        def PrintAwardRow(self, withtitle, bgcolor, main_title_id = 0):
                special_awards = SpecialAwards()
                print '<tr class="table%d">' % (bgcolor+1)
                
                # Display the award level/place
                print '<td>'
                if int(self.award_level) > 70:
                        level = '<i>%s</i>' % (special_awards[self.award_level])
                elif self.award_type_poll == 'Yes':
                        if int(self.award_level) == 1:
                                level = '<b>1</b>'
                        else:
                                level = self.award_level
                else:
                        if int(self.award_level) == 1:
                                level = '<b>Win</b>'
                        else:
                                level = 'Nomination'
                print '<a href="http:/%s/award_details.cgi?%s">%s</a>' % (HTFAKE, self.award_id, level)
                # For title-based awards given to VTs, display the VT if we are displaying the canonical title
                if not withtitle:
                        if self.title_id and main_title_id != self.title_id:
                                title = SQLloadTitle(self.title_id)
                                #  and self.title_id == title[TITLE_PUBID]
                                if title[TITLE_PARENT]:
                                        parent = SQLloadTitle(title[TITLE_PARENT])
                                        if parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                                print '(as %s)' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])
                print '</td>'
                
                # Display the award year and link it to the annual award page for that year/award
                print '<td><a href="http:/%s/ay.cgi?%s+%s">%s %s</a></td>' % (HTFAKE, self.award_type_id, self.award_year[:4], self.award_year[:4], self.award_type_short_name)
                if withtitle:
                        print '<td>'
                        # For title-based awards, display and hyperlink the work's title
                        if self.title_id:
                                title = SQLloadTitle(self.title_id)
                                print ISFDBLink('title.cgi', self.title_id, title[TITLE_TITLE])
                                if title[TITLE_PARENT]:
                                        parent = SQLloadTitle(title[TITLE_PARENT])
                                        if title[TITLE_LANGUAGE] and parent[TITLE_LANGUAGE] and title[TITLE_LANGUAGE] != parent[TITLE_LANGUAGE]:
                                                print ' (translation of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE])
                                        elif parent[TITLE_TITLE] != title[TITLE_TITLE]:
                                                print ' (variant of %s)' % ISFDBLink('title.cgi', parent[TITLE_PUBID], parent[TITLE_TITLE])
                        else:
                                if self.award_title and (self.award_title != "untitled"):
                                        print self.award_title
                        print '</td>'
                # Display the award's category
                print '<td><a href="http:/%s/award_category.cgi?%s+0">%s</a></td>' % (HTFAKE, self.award_cat_id, self.award_cat_name)
                print '</tr>'

        def PrintAwardSummary(self):
                from login import User
                special_awards = SpecialAwards()

                print '<ul>'
                print '<li><b>Title: </b>'
                title_data = ''
                if self.title_id:
                        title_data = SQLloadTitle(self.title_id)
                        print ISFDBLink("title.cgi", self.title_id, title_data[TITLE_TITLE])
                else:
                        print '%s (<i>no ISFDB title record</i>)' % self.award_title
                
                #Retrieve this user's data
                user = User()
                user.load()
                printRecordID('Award', self.award_id, user.id)

                if self.award_authors:
                        if len(self.award_authors) > 1:
                                print '<li><b>Authors: </b> '
                        else:
                                print '<li><b>Author: </b> '
                        self.PrintAwardAuthors()

                print '<li><b>Award Name: </b> <a href="http:/%s/awardtype.cgi?%s">%s</a>' % (HTFAKE, self.award_type_id, self.award_type_name)
                print '<li><b>Year: </b> <a href="http:/%s/ay.cgi?%s+%s">%s</a>' % (HTFAKE, self.award_type_id, self.award_year[:4], self.award_year[:4])
                print '<li><b>Category: </b> <a href="http:/%s/award_category.cgi?%s+0">%s</a>' % (HTFAKE, self.award_cat_id, self.award_cat_name)

                print '<li><b>Award Level: </b> '
                if int(self.award_level) > 70:
                        print '<i>%s</i>' % special_awards[self.award_level]
                elif self.award_type_poll == 'Yes':
                                print "<i>Poll Place</i>: %s" % self.award_level
                else:
                        if int(self.award_level) == 1:
                                print " Win"
                        else:
                                print " Nomination"

                if self.award_movie:
                        print """<li><b>IMDB record: </b> <a href="http://www.imdb.com/title/%s/"
                                 target="_blank">%s</a>""" % (self.award_movie, self.award_movie)

                if self.award_note:
                        print '<li>'
                        print FormatNote(self.award_note, 'Note', 'short', self.award_id, 'Award')
                print '</ul>'
                
        def PrintAwardAuthors(self):
                counter = 0
                # If the award is title-based, then display that title's authors
                if self.title_id:
                        authors = SQLTitleBriefAuthorRecords(self.title_id)
                        for author in authors:
                                if counter:
                                        print " <b>and</b> "
                                print ISFDBLink("ea.cgi", author[0], author[1])
                                counter += 1
                else:
                        for author in self.award_authors:
                                if counter:
                                        print " <b>and</b> "
                                actual = string.split(author, '^')
                                if string.find(actual[0], '***') > -1:
                                        print '-'
                                elif actual[0] == 'No Award':
                                        print 'No Award'
                                else:
                                        self.displayAuthor(actual[0])
                                counter += 1

        def displayAuthor(self, author):
                author_data = SQLgetAuthorData(author)
                if author_data:
                        print ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author)
                else:
                        print author
