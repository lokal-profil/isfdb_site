#
#     (C) COPYRIGHT 2013-2018   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import os
import re
from isfdb import *
from library import *
from xml.dom import minidom
from xml.dom import Node


class award_cat:
	def __init__(self):
                self.used_cat_id = 0
                self.used_cat_name = 0
                self.used_cat_type_id = 0
                self.used_cat_order = 0
		self.used_note = 0
		self.used_note_id = 0
		self.used_webpages = 0

		self.award_cat_id = ''
		self.award_cat_name = ''
		self.award_cat_type_id = ''
		self.award_cat_order = ''
		self.award_cat_note_id = ''
		self.award_cat_note = ''
		self.award_cat_webpages = []

		self.error = ''

	def load(self):
                if not self.award_cat_id:
                        return
                award_cat = SQLGetAwardCatById(self.award_cat_id)
                if not award_cat:
                        self.error = "Award Category doesn't exist"
                        return
                if award_cat[AWARD_CAT_ID]:
                        self.award_cat_id = award_cat[AWARD_CAT_ID]
                        self.used_cat_id = 1
                if award_cat[AWARD_CAT_NAME]:
                        self.award_cat_name = award_cat[AWARD_CAT_NAME]
                        self.used_cat_name = 1
                if award_cat[AWARD_CAT_TYPE_ID]:
                        self.award_cat_type_id = award_cat[AWARD_CAT_TYPE_ID]
                        self.used_cat_type_id = 1
                if award_cat[AWARD_CAT_ORDER]:
                        self.award_cat_order = award_cat[AWARD_CAT_ORDER]
                        self.used_cat_order = 1
                if award_cat[AWARD_CAT_NOTE]:
                        note = SQLgetNotes(award_cat[AWARD_CAT_NOTE])
                        if note:
                                self.award_cat_note_id = award_cat[AWARD_CAT_NOTE]
                                self.used_note_id = 1
                                self.award_cat_note = note
                                self.used_note = 1

                self.award_cat_webpages = SQLloadAwardCatWebpages(award_cat[AWARD_CAT_ID])
                if self.award_cat_webpages:
                        self.used_webpages = 1

	def cgi2obj(self):
		sys.stderr = sys.stdout
		self.form = cgi.FieldStorage()
		if self.form.has_key('award_cat_id'):
			self.award_cat_id = int(self.form['award_cat_id'].value)
			self.used_cat_id = 1

		try:
			self.award_cat_type_id = int(self.form['award_cat_type_id'].value)
			self.used_cat_type_id = 1
			award_type = SQLGetAwardTypeById(self.award_cat_type_id)
			if not award_type:
                                raise
		except:
                        self.error = 'Valid award type is required for award categories'
                        return

		try:
                        self.award_cat_name = XMLescape(self.form['award_cat_name'].value)
                        self.used_cat_name = 1
                        if not self.award_cat_name:
                                raise
                        # Unescape the award category name to ensure that the lookup finds it in the database
                        current_award_cat = SQLGetAwardCatByName(XMLunescape(self.award_cat_name), self.award_cat_type_id)
                        if current_award_cat:
                                if (self.award_cat_type_id == int(current_award_cat[AWARD_CAT_TYPE_ID])) and (self.award_cat_id != int(current_award_cat[AWARD_CAT_ID])) and (current_award_cat[AWARD_CAT_NAME] == XMLunescape(self.award_cat_name)):
                                        self.error = 'Entered award category name is aready associated with another category for this award type'
                                        return
		except:
                        self.error = 'Award category name is required'
                        return

		if self.form.has_key('award_cat_order'):
			self.award_cat_order = XMLescape(self.form['award_cat_order'].value)
			self.used_cat_order = 1
                        if not re.match(r'^[1-9]{1}[0-9]{0,8}$', self.award_cat_order):
                                self.error = 'Display Order must be an integer greater than 0 and must contain 1-9 digits'
                                return

		if self.form.has_key('award_cat_note'):
                        value = XMLescape(self.form['award_cat_note'].value)
                        if value:
                                self.award_cat_note = value
                                self.used_note = 1

		for key in self.form:
                        if key[:18] == 'award_cat_webpages':
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.award_cat_webpages:
                                                continue
                                        if not validateURL(value):
                                                self.error = 'Invalid Web page URL'
                                                return
                                        self.award_cat_webpages.append(value)
                                        self.used_webpages = 1


        def PrintAwardCatSummary(self, win_nom):
                from awardtypeClass import award_type
                from awards import PrintOneList
                from common import PrintWebPages
                from login import User
                awardType = award_type()
                awardType.award_type_id = self.award_cat_type_id
                awardType.load()
                print '<ul>'
                print '<li><b>Award Category: </b> %s' % self.award_cat_name

                #Retrieve this user's data
                user = User()
                user.load()
                printRecordID('Award Category', self.award_cat_id, user.id, user)

                print '<li><b>Award Name: </b> <a href="http:/%s/awardtype.cgi?%s">%s</a>' % (HTFAKE, awardType.award_type_id, awardType.award_type_name)
                if self.award_cat_order:
                        print '<li><b>Display Order: </b> %s' % self.award_cat_order

                # Webpages
                if self.award_cat_webpages:
                        PrintWebPages(self.award_cat_webpages)

                # Note
                if self.award_cat_note:
                        print '<li>'
                        print FormatNote(self.award_cat_note, 'Note', 'short', self.award_cat_id, 'AwardCat')
                print '</ul>'

                years = SQLloadAwardsForCat(self.award_cat_id, win_nom)
                if win_nom == 0:
                        if years:
                                print 'Displaying '
                        else:
                                print 'No '
                        print 'wins for this category. '
                        print 'You can also <a href="http:/%s/award_category.cgi?%d+%d">view all awards and nominations</a> in this category.' % (HTFAKE, self.award_cat_id, 1)
                else:
                        if not years:
                                print 'No wins or nominations for this category.'
                                return
                        print 'Displaying all wins and nominations for this category. '
                        print 'You can also limit the list to <a href="http:/%s/award_category.cgi?%d+%d">wins</a> in this category.' % (HTFAKE, self.award_cat_id, 0)
                print '<p>'
        	print '<table>'
        	for year in sorted(years.keys()):
                        print '<tr>'
                        print '<td colspan=3> </td>'
                        print '</tr>'
                        print '<tr>'
                        print '<td colspan=3><b><a href="http:/%s/ay.cgi?%d+%s">%s</a></b></td>' % (HTFAKE, awardType.award_type_id, year[:4], year[:4])
                        print '</tr>'
                        PrintOneList(years[year])
        	print '</table>'
