#
#     (C) COPYRIGHT 2005-2021   Al von Ruff and Ahasuerus
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
import time
import MySQLdb
from SQLparsing import *
from isfdb import *
from isfdblib import *
from library import *
from xml.dom import minidom
from xml.dom import Node


def normAuthor(value):
        # Convert double quotes to single quotes
        value = string.replace(value,'"',"'")
        # Strip plus signs because they are used as delimiters
        # in the body of the submission (to be changed later)
        value = string.replace(value,'+','')
        # Strip all leading, trailing and double spaces
        return string.join(string.split(value))

def lastRecord(form, field,counter):
        # Determine if the current field is the last field of its type
        # (title, review or interview) in the submitted form
        for next in range(counter, counter+30):
                key = field + str(next+1)
                if form.has_key(key):
                        return 0
        return 1

class titleEntry:
	def __init__(self):
		self.page = ''
		self.title = ''
		self.date = ''
		self.type = ''
		self.length = ''
		self.authors = ''
		self.next = ''
		self.id = 0
		self.oldtitle = 0

	def setPage(self, page):
		self.page = XMLescape(page)
	def setTitle(self, title):
		self.title = XMLescape(title)
	def setID(self, id):
		if int(id) > 0:
			self.id = int(id)
	def setDate(self, date):
                self.date = normalizeDate(date)
	def setType(self, type):
		self.type = XMLescape(type)
	def setLength(self, length):
                if length == None:
                        length = ''
		self.length = XMLescape(length)
	def setAuthors(self, authors):
		self.authors = XMLescape(authors)
	def setOldTitle(self, oldtitle):
		self.oldtitle = oldtitle

	def xmlTitle(self):
		if self.id:
			needstart = 1
			retval = ''
			if self.title != self.oldtitle.title:
				if needstart:
					needstart = 0
					retval += '<ContentTitle>\n'
					retval += '\t<Record>%s</Record>\n' % self.id
				retval += '  <cTitle>%s</cTitle>\n' % self.title
			if self.date != self.oldtitle.date:
				if needstart:
					needstart = 0
					retval += '<ContentTitle>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cDate>%s</cDate>\n' % self.date
			if str(self.page) != str(self.oldtitle.page):
				if needstart:
					needstart = 0
					retval += '<ContentTitle>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cPage>%s</cPage>\n' % self.page
			if self.type != self.oldtitle.type:
				if needstart:
					needstart = 0
					retval += '<ContentTitle>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cType>%s</cType>\n' % self.type
			if self.length != self.oldtitle.length:
                                if needstart:
                                        needstart = 0
                                        retval += '<ContentTitle>\n'
                                        retval += '  <Record>%s</Record>\n' % self.id
                                retval += '  <cLength>%s</cLength>\n' % self.length
			if self.authors != self.oldtitle.authors:
				if needstart:
					needstart = 0
					retval += '<ContentTitle>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cAuthors>%s</cAuthors>\n' % self.authors
			if needstart == 0:
				retval += '</ContentTitle>\n'
		else:
			retval = ''
			retval += '<ContentTitle>\n'
			retval += '  <cTitle>%s</cTitle>\n' % self.title
			retval += '  <cAuthors>%s</cAuthors>\n' % self.authors
			retval += '  <cDate>%s</cDate>\n' % self.date
			if self.page != '':
				retval += '  <cPage>%s</cPage>\n' % self.page
			if self.type != '':
				retval += '  <cType>%s</cType>\n' % self.type
			if self.length != '':
                                retval += '  <cLength>%s</cLength>\n' % self.length
			retval += '</ContentTitle>\n'
		return retval

	def xmlCloneTitle(self):
		retval = ''
		retval += '<ContentTitle>\n'
		retval += '  <Record>%s</Record>\n' % self.id
		retval += '  <cTitle>%s</cTitle>\n' % self.title
		retval += '  <cAuthors>%s</cAuthors>\n' % self.authors
		retval += '  <cDate>%s</cDate>\n' % self.date
		if self.page != '':
			retval += '  <cPage>%s</cPage>\n' % self.page
		if self.type != '':
			retval += '  <cType>%s</cType>\n' % self.type
		if self.length != '':
                        retval += '  <cLength>%s</cLength>\n' % self.length
		retval += '</ContentTitle>\n'
		return retval

	def printTitle(self):
		print self.xmlTitle()

class reviewEntry:
	def __init__(self):
		self.page = ''
		self.title = ''
		self.date = ''
		self.bookauthors = ''
		self.reviewers = ''
		self.next = ''
		self.oldreview = 0
		self.id = 0

	def setPage(self, page):
		self.page = XMLescape(page)
	def setTitle(self, title):
		self.title = XMLescape(title)
	def setID(self, id):
		if int(id) > 0:
			self.id = int(id)
	def setDate(self, date):
		self.date = normalizeDate(date)
	def setBookAuthors(self, authors):
		self.bookauthors = XMLescape(authors)
	def setReviewers(self, authors):
		self.reviewers = XMLescape(authors)
	def setOldReview(self, oldreview):
		self.oldreview = oldreview
	def xmlTitle(self):
		if self.id:
			needstart = 1
			retval = ''
			if self.title != self.oldreview.title:
				if needstart:
					needstart = 0
					retval += '<ContentReview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cTitle>%s</cTitle>\n' % self.title
			if self.date != self.oldreview.date:
				if needstart:
					needstart = 0
					retval += '<ContentReview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cDate>%s</cDate>\n' % self.date
			if str(self.page) != str(self.oldreview.page):
				if needstart:
					needstart = 0
					retval += '<ContentReview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cPage>%s</cPage>\n' % self.page
			if self.bookauthors != self.oldreview.bookauthors:
				if needstart:
					needstart = 0
					retval += '<ContentReview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cBookAuthors>%s</cBookAuthors>\n' % self.bookauthors
			if self.reviewers != self.oldreview.reviewers:
				if needstart:
					needstart = 0
					retval += '<ContentReview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cReviewers>%s</cReviewers>\n' % self.reviewers
			if needstart == 0:
				retval += '</ContentReview>\n'
		else:
			retval = ''
			retval += '<ContentReview>\n'
			retval += '  <cTitle>%s</cTitle>\n' % self.title
			retval += '  <cBookAuthors>%s</cBookAuthors>\n' % self.bookauthors
			retval += '  <cReviewers>%s</cReviewers>\n' % self.reviewers
			retval += '  <cDate>%s</cDate>\n' % self.date
			if self.page != '':
				retval += '  <cPage>%s</cPage>\n' % self.page
			retval += '</ContentReview>\n'
		return retval

	def xmlCloneTitle(self):
		retval = ''
		retval += '<ContentReview>\n'
		retval += '  <Record>%s</Record>\n' % self.id
		retval += '  <cTitle>%s</cTitle>\n' % self.title
		retval += '  <cBookAuthors>%s</cBookAuthors>\n' % self.bookauthors
		retval += '  <cReviewers>%s</cReviewers>\n' % self.reviewers
		retval += '  <cDate>%s</cDate>\n' % self.date
		if self.page != '':
			retval += '  <cPage>%s</cPage>\n' % self.page
		retval += '</ContentReview>\n'
		return retval

	def printTitle(self):
		print self.xmlTitle()

class interviewEntry:
	def __init__(self):
		self.page = ''
		self.title = ''
		self.date = ''
		self.interviewees = ''
		self.interviewers = ''
		self.next = ''
		self.id = 0
		self.oldinterview = 0

	def setPage(self, page):
		self.page = XMLescape(page)
	def setTitle(self, title):
		self.title = XMLescape(title)
	def setID(self, id):
		if int(id) > 0:
			self.id = int(id)
	def setDate(self, date):
		self.date = normalizeDate(date)
	def setInterviewees(self, authors):
		self.interviewees = XMLescape(authors)
	def setInterviewers(self, authors):
		self.interviewers = XMLescape(authors)
	def setOldInterview(self, oldinterview):
		self.oldinterview = oldinterview
	def xmlTitle(self):
		if self.id:
			needstart = 1
			retval = ''
			if self.title != self.oldinterview.title:
				if needstart:
					needstart = 0
					retval += '<ContentInterview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cTitle>%s</cTitle>\n' % self.title
			if self.date != self.oldinterview.date:
				if needstart:
					needstart = 0
					retval += '<ContentInterview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cDate>%s</cDate>\n' % self.date
			if str(self.page) != str(self.oldinterview.page):
				if needstart:
					needstart = 0
					retval += '<ContentInterview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cPage>%s</cPage>\n' % self.page
			if self.interviewees != self.oldinterview.interviewees:
				if needstart:
					needstart = 0
					retval += '<ContentInterview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cInterviewees>%s</cInterviewees>\n' % self.interviewees
			if self.interviewers != self.oldinterview.interviewers:
				if needstart:
					needstart = 0
					retval += '<ContentInterview>\n'
					retval += '  <Record>%s</Record>\n' % self.id
				retval += '  <cInterviewers>%s</cInterviewers>\n' % self.interviewers
			if needstart == 0:
				retval += '</ContentInterview>\n'
		else:
			retval = ''
			retval += '<ContentInterview>\n'
			retval += '  <cTitle>%s</cTitle>\n' % self.title
			retval += '  <cInterviewees>%s</cInterviewees>\n' % self.interviewees
			retval += '  <cInterviewers>%s</cInterviewers>\n' % self.interviewers
			retval += '  <cDate>%s</cDate>\n' % self.date
			if self.page != '':
				retval += '  <cPage>%s</cPage>\n' % self.page
			retval += '</ContentInterview>\n'
		return retval

	def xmlCloneTitle(self):
		retval = ''
		retval += '<ContentInterview>\n'
		retval += '  <cTitle>%s</cTitle>\n' % self.title
		retval += '  <Record>%s</Record>\n' % self.id
		retval += '  <cInterviewees>%s</cInterviewees>\n' % self.interviewees
		retval += '  <cInterviewers>%s</cInterviewers>\n' % self.interviewers
		retval += '  <cDate>%s</cDate>\n' % self.date
		if self.page != '':
			retval += '  <cPage>%s</cPage>\n' % self.page
		retval += '</ContentInterview>\n'
		return retval

	def printTitle(self):
		print self.xmlTitle()

class pubs:
	def __init__(self, db):
		self.db = db
		self.used_id        = 0
		self.used_title     = 0
		self.used_trans_titles = 0
		self.used_tag       = 0
		self.used_year      = 0
		self.used_publisher = 0
		self.used_series    = 0
		self.used_series_num= 0
		self.used_pages     = 0
		self.used_ptype     = 0
		self.used_ctype     = 0
		self.used_isbn      = 0
		self.used_catalog   = 0
		self.used_image     = 0
		self.used_price     = 0
		self.used_note      = 0
		self.used_webpages  = 0
		self.title_id       = 0
		self.num_authors    = 0
		self.pub_authors    = []
		self.num_artists    = 0
		self.pub_artists    = []
		self.pub_id         = ''
		self.pub_title      = ''
		self.pub_trans_titles = []
		self.pub_tag        = ''
		self.pub_year       = ''
		self.pub_pages      = ''
		self.pub_ptype      = ''
		self.pub_ctype      = ''
		self.pub_isbn       = ''
		self.pub_catalog    = ''
		self.pub_image      = ''
		self.pub_price      = ''
		self.pub_publisher_id = ''
		self.pub_publisher  = ''
		self.pub_series     = ''
		self.pub_series_id  = ''
		self.pub_series_num = ''
		self.pub_note       = ''
		self.pub_webpages   = []
		self.titles         = ''
		self.reviews        = ''
		self.interviews     = ''
		self.editor	    = ''
		self.error          = ''
		self.cover_ids      = {}
		self.cover_records  = {}
		self.cover_artists  = {}
		self.cover_dates    = {}
		self.cover_titles   = {}
		self.cover_changed  = {}
                self.reference_title_count = 0
                self.identifiers    = {}
                self.body   = ''

	def pushTitle(self, titleEntry):
		if self.titles == '':
			self.titles = titleEntry
		else:
			tmp = self.titles
			while tmp.next != '':
				tmp = tmp.next
			tmp.next = titleEntry

	def pushReview(self, reviewEntry):
		if self.reviews == '':
			self.reviews = reviewEntry
		else:
			tmp = self.reviews
			while tmp.next != '':
				tmp = tmp.next
			tmp.next = reviewEntry

	def pushInterview(self, interviewEntry):
		if self.interviews == '':
			self.interviews = interviewEntry
		else:
			tmp = self.interviews
			while tmp.next != '':
				tmp = tmp.next
			tmp.next = interviewEntry

	def xmlCoverArt(self, clone):
                retval = ''
                for cover_record in self.cover_records:
                        cover_title_id = self.cover_records[cover_record]
                        # For EditPub, only add modified or new COVERART titles
                        # For ClonePub, add all COVERART titles
                        if clone or (cover_record in self.cover_changed) or not cover_title_id:
                                retval += '      <Cover>\n'
                                # If cloning, always add the COVERART title ID. If editing
                                # only add the COVERART title ID if it's not 0, i.e. for pre-existing COVERART titles
                                if clone or self.cover_records[cover_record]:
                                        retval += '        <Record>%d</Record>\n' % int(cover_title_id)
                                retval += '        <cTitle>%s</cTitle>\n' % self.cover_titles[cover_record]
                                retval += '        <cDate>%s</cDate>\n' % self.cover_dates[cover_record]
                                artist_count = 1
                                retval += '        <cArtists>'
                                for artist in self.cover_artists[cover_record]:
                                        if artist_count > 1:
                                                retval += '+'
                                        retval += artist
                                        artist_count += 1
                                retval += '</cArtists>\n'
                                retval += '      </Cover>\n'
                return retval

	def xmlContent(self):
		retval = '    <Content>\n'
		# Cover Art records
		retval += self.xmlCoverArt(0)
		tmp = self.titles
		while tmp != '':
			retval += tmp.xmlTitle()
			tmp = tmp.next
		tmp = self.reviews
		while tmp != '':
			retval += tmp.xmlTitle()
			tmp = tmp.next
		tmp = self.interviews
		while tmp != '':
			retval += tmp.xmlTitle()
			tmp = tmp.next
		retval += '    </Content>\n'
		return retval

	def xmlCloneContent(self):
		retval = ''
		retval += '<Content>\n'
		# Cover Art records -- the new way
		retval += self.xmlCoverArt(1)
		tmp = self.titles
		while tmp != '':
			retval += tmp.xmlCloneTitle()
			tmp = tmp.next
		tmp = self.reviews
		while tmp != '':
			retval += tmp.xmlCloneTitle()
			tmp = tmp.next
		tmp = self.interviews
		while tmp != '':
			retval += tmp.xmlCloneTitle()
			tmp = tmp.next
		retval += '</Content>\n'
		return retval

        def xmlIdentifiers(self, include_type_name = 0):
		update_string = "    <External_IDs>\n"
		for type_name in self.identifiers:
                        for id_value in self.identifiers[type_name]:
                                type_id = self.identifiers[type_name][id_value][0]
                                update_string += "      <External_ID>\n"
                                update_string += "          <IDtype>%d</IDtype>\n" % int(type_id)
                                if include_type_name:
                                        update_string += "          <IDtypeName>%s</IDtypeName>\n" % db.escape_string(XMLescape(type_name))
                                # Identifier values must be XML-escaped here since they are not escaped in cgi2obj
                                update_string += "          <IDvalue>%s</IDvalue>\n" % db.escape_string(XMLescape(id_value))
                                update_string += "      </External_ID>\n"
		update_string += "    </External_IDs>\n"
		return update_string

	def printContent(self):
		tmp = self.titles
		while tmp.next != '':
			tmp.printTitle()
			tmp = tmp.next

        def authors(self):
                counter = 0
                retval = ''
                while counter < self.num_authors:
                        if counter == 0:
                                retval = normAuthor(self.pub_authors[counter])
                        else:
                                retval += "+" + normAuhtor(self.pub_authors[counter])
                        counter += 1
                return retval

        def artists(self):
                counter = 0
                retval = ''
                while counter < self.num_artists:
                        if counter == 0:
                                retval = normAuthor(self.pub_artists[counter])
                        else:
                                retval += "+" + normAuthor(self.pub_artists[counter])
                        counter += 1
                return retval

	def load(self, id):
		if id == 0:
			return
		query = "select * from pubs where pub_id=%d" % int(id)
		self.db.query(query)
		result = self.db.store_result()
		record = result.fetch_row()
		if record:
			if record[0][PUB_PUBID]:
				self.pub_id = record[0][PUB_PUBID]
				self.used_id = 1
			if record[0][PUB_TITLE]:
				self.pub_title = record[0][PUB_TITLE]
				self.used_title = 1
			if record[0][PUB_TAG]:
				self.pub_tag  = record[0][PUB_TAG]
				self.used_tag = 1
			if record[0][PUB_YEAR]:
				self.pub_year = record[0][PUB_YEAR]
				self.used_year = 1
			if record[0][PUB_PAGES]:
				self.pub_pages = record[0][PUB_PAGES]
				self.used_pages = 1
			if record[0][PUB_PTYPE]:
				self.pub_ptype = record[0][PUB_PTYPE]
				self.used_ptype = 1
			if record[0][PUB_CTYPE]:
				self.pub_ctype = record[0][PUB_CTYPE]
				self.used_ctype = 1
			if record[0][PUB_ISBN]:
				self.pub_isbn = record[0][PUB_ISBN]
				self.used_isbn = 1
			if record[0][PUB_CATALOG]:
				self.pub_catalog = record[0][PUB_CATALOG]
				self.used_catalog = 1
			if record[0][PUB_IMAGE]:
				self.pub_image = record[0][PUB_IMAGE]
				self.used_image = 1
			if record[0][PUB_PRICE]:
				self.pub_price = record[0][PUB_PRICE]
				self.used_price = 1
			if record[0][PUB_SERIES_NUM]:
				self.pub_series_num = record[0][PUB_SERIES_NUM]
				self.used_series_num = 1

                        self.pub_webpages = SQLloadPubWebpages(record[0][PUB_PUBID])
                        if self.pub_webpages:
                                self.used_webpages = 1

                        res2 = SQLloadTransPubTitles(record[0][PUB_PUBID])
                        if res2:
                                self.pub_trans_titles = res2
                                self.used_trans_titles = 1

                        query = """select authors.author_canonical from authors, pub_authors
                                   where pub_authors.author_id=authors.author_id and
                                   pub_authors.pub_id=%d""" % record[0][PUB_PUBID]
                        self.db.query(query)
                        res2 = self.db.store_result()
                        rec2 = res2.fetch_row()
			while rec2:
				try:
					self.pub_authors.append(rec2[0][0])
					self.num_authors += 1
					rec2 = res2.fetch_row()
				except:
					break

			titles = SQLloadTitlesXBT(record[0][PUB_PUBID])
			results = []
			for title in titles:
				if title[TITLE_TTYPE] == 'COVERART':
					artists = SQLTitleAuthors(title[TITLE_PUBID])
					for artist in artists:
						self.pub_artists.append(artist)
						self.num_artists += 1

			if record[0][PUB_PUBLISHER]:
                        	query = "select publisher_name from publishers where publisher_id='%d'" % (record[0][PUB_PUBLISHER])
                        	self.db.query(query)
                        	res2 = self.db.store_result()
                        	rec2 = res2.fetch_row()
                        	if rec2:
					self.used_publisher = 1
					self.pub_publisher_id = record[0][PUB_PUBLISHER]
					self.pub_publisher = rec2[0][0]

			if record[0][PUB_SERIES]:
                        	query = "select pub_series_name from pub_series where pub_series_id='%d'" % (record[0][PUB_SERIES])
                        	self.db.query(query)
                        	res2 = self.db.store_result()
                        	rec2 = res2.fetch_row()
                        	if rec2:
					self.used_series = 1
					self.pub_series = rec2[0][0]
					self.pub_series_id = record[0][PUB_SERIES]

			if record[0][PUB_NOTE]:
                        	query = "select note_note from notes where note_id='%d'" % (int(record[0][PUB_NOTE]))
                        	self.db.query(query)
                        	res2 = self.db.store_result()
                        	rec2 = res2.fetch_row()
                        	if rec2:
					self.used_note = 1
					self.pub_note = rec2[0][0]

			self.loadExternalIDs()

		else:
			self.error = 'Pub record not found'
			return

        def loadExternalIDs(self):
                # Build a dictionary of external IDs for this pub. The dictionary structure is:
                # self.identifiers[type_name][id_value] = (type_id, type_full_name)
                ext_ids = SQLLoadIdentifiers(self.pub_id)
                id_types = SQLLoadIdentifierTypes()
                for ext_id in ext_ids:
                        type_id = ext_id[IDENTIFIER_TYPE_ID]
                        type_name = id_types[type_id][0]
                        type_full_name = id_types[type_id][1]
                        id_value = ext_id[IDENTIFIER_VALUE]
                        if type_name not in self.identifiers:
                                self.identifiers[type_name] = {}
                        self.identifiers[type_name][id_value] = (type_id, type_full_name)

	###########################################
	# obj2xml converts a pubs class object
	# into XML format
	###########################################
	def obj2xml(self):
		if self.used_id:
			container = "    <Publication>\n"
			container += "      <Record>%s</Record>\n" % (self.pub_id)

			if self.used_title:
				container += "      <Title>%s</Title>\n" % XMLescape(self.pub_title)

			if self.num_authors:
				container += "      <Authors>\n"
				counter = 0
				while counter < self.num_authors:
					container += "        <Author>%s</Author>\n" % XMLescape(self.pub_authors[counter])
					counter += 1
				container += "      </Authors>\n"

			if self.used_year:
				container += "      <Year>%s</Year>\n" % XMLescape(self.pub_year)
			if self.used_isbn:
				container += "      <Isbn>%s</Isbn>\n" % XMLescape(self.pub_isbn)
			if self.used_catalog:
				container += "      <Catalog>%s</Catalog>\n" % XMLescape(self.pub_catalog)
			if self.used_publisher:
				container += "      <Publisher>%s</Publisher>\n" % XMLescape(self.pub_publisher)
			if self.used_series:
				container += "      <PubSeries>%s</PubSeries>\n" % XMLescape(self.pub_series)
			if self.used_series_num:
				container += "      <PubSeriesNum>%s</PubSeriesNum>\n" % XMLescape(self.pub_series_num)
			if self.used_price:
				container += "      <Price>%s</Price>\n" % XMLescape(self.pub_price)
			if self.used_pages:
				container += "      <Pages>%s</Pages>\n" % XMLescape(self.pub_pages)
			if self.used_ptype:
				container += "      <Binding>%s</Binding>\n" % XMLescape(self.pub_ptype)
			if self.used_ctype:
				container += "      <Type>%s</Type>\n" % XMLescape(self.pub_ctype)
			if self.used_tag:
				container += "      <Tag>%s</Tag>\n" % XMLescape(self.pub_tag)
			if self.used_image:
				container += "      <Image>%s</Image>\n" % XMLescape(self.pub_image)

			if self.used_note:
				container += "      <Note>%s</Note>\n" % XMLescape(self.pub_note)

			#########################
			# Content
			#########################
			#self.titles
			#self.reviews
			#self.interviews
			#self.editor


			container += "    </Publication>\n"
		else:
			print "XML: pass"
			container = ""
		return container


	###########################################
	# cgi2obj converts input from an html form
	# into a pubs class object.
	###########################################
	def cgi2obj(self, reference_title = 'explicit'):
                import re
		sys.stderr = sys.stdout
		self.form = cgi.FieldStorage()
		if self.form.has_key('pub_id'):
                        try:
        			self.pub_id = str(int(self.form['pub_id'].value))
        		except:
                                self.error = "Publication ID must be an integer number"
                                return
			self.used_id = 1

		try:
			self.pub_title = XMLescape(self.form['pub_title'].value)
			self.used_title = 1
			if not self.pub_title:
                                raise
                except:
                        self.error = 'No title specified'
                        return

		if self.form.has_key('title_id'):
                        try:
        			self.title_id = str(int(self.form['title_id'].value))
        		except:
                                self.error = "Title ID must be an integer number"
                                return

		if self.form.has_key('editor'):
			self.editor = self.form['editor'].value

      		for key in self.form:
                        if 'trans_titles' in key:
                                value = XMLescape(self.form[key].value)
                                if value:
                                        self.pub_trans_titles.append(value)
                                        self.used_trans_titles = 1

		###################################
		# AUTHORS
		###################################
		self.num_authors = 0
		self.pub_authors = []
                counter = 0
                while counter < 200:
                        if self.form.has_key('pub_author'+str(counter+1)):
                                value = self.form['pub_author'+str(counter+1)].value
                                value = XMLescape(normAuthor(value))
                                if value and (value not in self.pub_authors):
                                        self.pub_authors.append(value)
                                        self.num_authors += 1
                        counter += 1
                if not self.num_authors:
                        self.error = """No authors were specified. Every publication
                                        must have an author/editor. For uncredited
                                        publications, use 'uncredited'. When entering
                                        data from a secondary source and the author/editor
                                        is not known, use 'unknown'. If the author is
                                        explicitly credited as 'Anonymous', use 'Anonymous'"""
                        return


		###################################
		# METADATA
		###################################
		if self.form.has_key('pub_tag'):
			tag = self.form['pub_tag'].value
			tag = string.replace(tag, "'", '')
			tag = string.replace(tag, "<", '')
			tag = string.replace(tag, ">", '')
			self.pub_tag = tag
			self.used_tag = 1
		try:
                        # Handle XML escaping; also strip leading and trailing spaces
                        self.pub_year = XMLescape(self.form['pub_year'].value)
                        if not self.pub_year:
                                raise
                        # Validate and normalize the date - change to 0000-00-00 if it's invalid
                        self.pub_year = normalizeDate(self.pub_year)
			self.used_year = 1
		except:
                        self.error = 'No year was specified'
                        return

		if self.form.has_key('pub_publisher'):
                        value = XMLescape(self.form['pub_publisher'].value)
                        if value:
        			self.pub_publisher = value
        			self.used_publisher = 1

		if self.form.has_key('pub_series'):
                        value = XMLescape(self.form['pub_series'].value)
                        if value:
        			self.pub_series = value
        			self.used_series = 1

		if self.form.has_key('pub_series_num'):
                        value = XMLescape(self.form['pub_series_num'].value)
                        if value:
        			self.pub_series_num = value
        			self.used_series_num = 1

		if self.form.has_key('pub_pages'):
                        value = XMLescape(self.form['pub_pages'].value)
                        if value:
        			self.pub_pages = value
        			self.used_pages = 1

		if self.form.has_key('pub_ptype'):
                        value = XMLescape(self.form['pub_ptype'].value)
                        if value not in FORMATS:
                                self.error = 'Invalid Publication Format - %s' % value
                                return
                        self.pub_ptype = value
                        self.used_ptype = 1

                ctype = ''
		try:
			ctype = self.form['pub_ctype'].value
			if ctype not in PUB_TYPES:
                                raise
                        self.pub_ctype = ctype
                        self.used_ctype = 1
		except:
                        self.error = 'Invalid Publication Type - %s' % ctype
                        return

		if self.form.has_key('pub_image'):
                        value = XMLescape(self.form['pub_image'].value)
                        if value:
                                self.error = invalidURL(value)
                                if self.error:
                                        return
                                if value[0:41] == '%s://%s/index.php/Image' % (PROTOCOL, WIKILOC):
                                        self.error = "URL for covers should be for the image, not the Wiki page the image is on"
                                        return
        			self.pub_image = value
        			self.used_image = 1

		if self.form.has_key('pub_isbn'):
                        value = XMLescape(self.form['pub_isbn'].value)
                        value = string.replace(value, '-', '')
                        value = string.replace(value, ' ', '')
                        value = string.replace(value, 'x', 'X')
                        if value:
                                self.pub_isbn = value
                                self.used_isbn = 1

		if self.form.has_key('pub_catalog'):
                        value = XMLescape(self.form['pub_catalog'].value)
                        if value:
        			self.pub_catalog = value
        			self.used_catalog = 1

		for key in self.form:
                        if key.startswith('pub_webpages') or key.startswith('shared_pub_webpages'):
                                value = XMLescape(self.form[key].value)
                                if value:
                                        if value in self.pub_webpages:
                                                continue
                                        self.error = invalidURL(value)
                                        if self.error:
                                                return
                                        self.pub_webpages.append(value)
                                        self.used_webpages = 1

                # External identifiers
                identifier_types = SQLLoadIdentifierTypes()
                for key in self.form:
                        if 'external_id.' in key:
                                # Get the External ID number and value
                                try:
                                        ext_id_number = int(key.split('.')[1])
                                        if not ext_id_number:
                                                raise
                                except:
                                        self.error = 'Invalid identifier type'
                                        return
                                ext_id_value = self.form[key].value.strip()

                                # Check if there are invalid characters in the user-entered value
                                self.error = invalidURLcharacters(ext_id_value, 'External ID', 'unescaped')
                                if self.error:
                                        return

                                # Retrieve the external identifier type associated with this user-entered value
                                # If there is none, it's non-numeric or 0, then this ID is invalid
                                try:
                                        id_type_number = int(self.form['external_id_type.%d' % ext_id_number].value)
                                        if not id_type_number:
                                                raise
                                except:
                                        self.error = 'Invalid identifier type'
                                        return
                                type_tuple = identifier_types.get(id_type_number, None)
                                if not type_tuple:
                                        self.error = 'Unsupported identifier type %d' % id_type_number
                                        return
                                type_name = type_tuple[0]
                                type_full_name = type_tuple[1]
                                if type_name not in self.identifiers:
                                        self.identifiers[type_name] = {}
                                # If this ID has already been entered for this ID type, skip it
                                if ext_id_value in self.identifiers[type_name]:
                                        continue
                                self.identifiers[type_name][ext_id_value] = (id_type_number, type_full_name)

		if self.form.has_key('pub_price'):
                        value = XMLescape(self.form['pub_price'].value)
                        if value:
                                currency_map = {'B' : BAHT_SIGN,
                                              'E' : EURO_SIGN,
                                              'Kc ': '%s ' % CZECH_KORUNA_SIGN,
                                              'Kcs ': '%s ' % CZECHOSLOVAK_KORUNA_SIGN,
                                              'L' : POUND_SIGN,
                                              'P' : PESO_SIGN,
                                              'Y' : YEN_SIGN,
                                              'zl ': '%s ' % ZLOTY_SIGN
                                              }
                                for abbrev in currency_map:
                                        if re.match('^%s[0-9]{1}' % abbrev, value):
                                                currency_sign = currency_map[abbrev]
                                                padding_space = ''
                                                if currency_sign.endswith(' '):
                                                        padding_space = ' '
                                                value = '%s%s%s' % (XMLescape(currency_sign), padding_space, value[len(abbrev):])
                                                break
        			self.used_price = 1
        			self.pub_price = value

		if self.form.has_key('pub_note'):
                        value = XMLescape(self.form['pub_note'].value)
                        if value:
        			self.pub_note = value
        			self.used_note = 1

		#####################################################################
		# COVER ART CONTENT
		#####################################################################
		# Parse the submitted form and put its values in Python dictionaries
                for key in self.form.keys():
                        # Retrieve and save all cover IDs
                        splitstring = key.partition('cover_id')
                        cover_id = splitstring[2]
                        if cover_id:
                                try:
                                        cover_id = int(cover_id)
                                        if cover_id < 1:
                                                raise
                                except:
                                        self.error = 'Invalid Cover ID'
                                        return
                                try:
                                        self.cover_ids[cover_id] = int(self.form[key].value)
                                except:
                                        self.error = 'Invalid Cover ID Value'
                                        return
                                continue
                        # Retrieve and save all cover artists
                        splitstring = key.partition('cover_artist')
                        suffix = splitstring[2]
                        if suffix:
                                split_suffix = suffix.partition('.')
                                cover_id = split_suffix[0]
                                artist_id = split_suffix[2]
                                try:
                                        cover_id = int(cover_id)
                                        if cover_id < 1:
                                                raise
                                except:
                                        self.error = 'Invalid Cover ID'
                                        return
                                try:
                                        artist_id = int(artist_id)
                                        if artist_id < 1:
                                                raise
                                except:
                                        self.error = 'Invalid Artist ID'
                                        return
                                artist_name = XMLescape(normAuthor(self.form[key].value))
                                if not artist_name:
                                        continue
                                # Add the artist's name to the list of artists for this cover ID
                                if cover_id not in self.cover_artists:
                                        self.cover_artists[cover_id] = []
                                if artist_name not in self.cover_artists[cover_id]:
                                        self.cover_artists[cover_id].append(artist_name)
                                continue
                        # Retrieve and save cover titles
                        splitstring = key.partition('cover_title')
                        cover_id = splitstring[2]
                        if cover_id:
                                try:
                                        cover_id = int(cover_id)
                                        if cover_id < 1:
                                                raise
                                except:
                                        self.error = 'Invalid Cover Title ID'
                                        return
                                self.cover_titles[cover_id] = XMLescape(self.form[key].value)
                                continue
                        # Retrieve and save cover dates
                        splitstring = key.partition('cover_date')
                        cover_id = splitstring[2]
                        if cover_id:
                                try:
                                        cover_id = int(cover_id)
                                        if cover_id < 1:
                                                raise
                                except:
                                        self.error = 'Invalid Cover Date ID'
                                        return
                                self.cover_dates[cover_id] = normalizeDate(self.form[key].value)
                                continue

                # Cross-check the cover IDs against all other submitted field values
                # to make sure that the submitted data is internally consistent
                for cover_id in self.cover_artists:
                        if cover_id not in self.cover_ids:
                                self.error = 'Artist ID for a non-existent Cover ID'
                                return
                for cover_id in self.cover_titles:
                        if cover_id not in self.cover_ids:
                                self.error = 'Title ID for a non-existent Cover ID'
                                return
                for cover_id in self.cover_dates:
                        if cover_id not in self.cover_ids:
                                self.error = 'Date ID for a non-existent Cover ID'
                                return

                # If a cover record was submitted with a title but no artist(s),
                # return an error
                for cover_id in self.cover_titles:
                        if cover_id not in self.cover_artists:
                                self.error = 'A cover submitted with a title but no artist(s)'
                                return

                # If a cover record was submitted with a date but no artist(s),
                # return an error
                for cover_id in self.cover_dates:
                        if cover_id not in self.cover_artists:
                                self.error = 'A cover submitted with a date but no artist(s)'
                                return

                # Build a dictionary of cover records for which cover artists were submitted
                # which will eliminate blank cover art records
                for cover_id in self.cover_ids:
                        if cover_id in self.cover_artists:
                                self.cover_records[cover_id] = self.cover_ids[cover_id]

                # For new cover records, use the publication date as the cover date
                # and the publication title as the cover title
                for cover_record in self.cover_records:
                        if cover_record not in self.cover_titles:
                                self.cover_titles[cover_record] = self.pub_title
                        # Check if an all-spaces title was entered
                        elif not self.cover_titles[cover_record]:
                                self.cover_titles[cover_record] = self.pub_title
                        if cover_record not in self.cover_dates:
                                self.cover_dates[cover_record] = self.pub_year

                # For pre-existing covers, check if each cover record was modified. This will
                # allow us to save only the modified records in the submission payload.
                for cover_id in self.cover_records:
                        cover_title_id = self.cover_records[cover_id]
                        if not cover_title_id:
                                continue
                        old_title = SQLloadTitle(cover_title_id)
                        if old_title[TITLE_YEAR] != self.cover_dates[cover_id]:
                                self.cover_changed[cover_id] = 1
                                continue
                        if XMLescape(old_title[TITLE_TITLE]) != self.cover_titles[cover_id]:
                                self.cover_changed[cover_id] = 1
                                continue
                        old_artists = SQLTitleAuthors(cover_title_id)
                        if compare_lists(self.cover_artists[cover_id], old_artists):
                                self.cover_changed[cover_id] = 1
                                continue
                

		###################################
		# REGULAR TITLE CONTENT
		###################################
		counter = 1
		title_types = {}
		while counter:
			#############################
			# TITLE
			#############################
			key = "title_title"+str(counter)
			oldTitle = 0
			if self.form.has_key(key):
				newTitle = titleEntry()
				newTitle.setTitle(self.form[key].value)

				key = "title_id"+str(counter)
				if self.form.has_key(key):
					newTitle.setID(self.form[key].value)
					if int(newTitle.id) > 0:
						oldTitle = titleEntry()
						title_data = SQLloadTitle(newTitle.id)
						oldTitle.setTitle(title_data[TITLE_TITLE])
						oldTitle.setID(newTitle.id)
			else:
				key = "title_page"+str(counter)
				if self.form.has_key(key):
					self.error = "Entry must have a title. Page=%s" % (self.form[key].value)
					return
				key = "title_author%s.1" % str(counter)
				if self.form.has_key(key):
					self.error = "Entry must have a title. Author=%s" % (self.form[key].value)
					return
				# Check if this is the last submitted Title record
				if lastRecord(self.form, "title_title", counter):
                                        break
                                else:
					counter += 1
					continue

			#############################
			# PAGE
			#############################
			key = "title_page"+str(counter)
			if self.form.has_key(key):
                                page_number = self.form[key].value
                                if len(page_number) > 20:
                                        key = "title_title"+str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Title=%s" % (self.form[key].value)
                                                return
                                        key = "title_author%s.1" % str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Author=%s" % (self.form[key].value)
                                                return
				newTitle.setPage(page_number)
			if oldTitle:
				title_page = SQLGetPageNumber(oldTitle.id, self.pub_id)
				if title_page:
					oldTitle.setPage(title_page)

			#############################
			# DATE
			#############################
			key = "title_date"+str(counter)
			if self.form.has_key(key):
				newTitle.setDate(self.form[key].value)
			else:
				newTitle.setDate(self.pub_year)
			if oldTitle:
				oldTitle.setDate(title_data[TITLE_YEAR])

			#############################
			# TTYPE
			#############################
			key = "title_ttype"+str(counter)
			if self.form.has_key(key):
				newTitle.setType(self.form[key].value)
                                if newTitle.type not in REGULAR_TITLE_TYPES:
                                        self.error = 'Invalid title type'
                                        return
                                title_types[newTitle.type] = title_types.get(newTitle.type, 0) + 1
                                if newTitle.type == self.pub_ctype:
                                        self.reference_title_count += 1
                                if newTitle.type == 'EDITOR' and self.pub_ctype in ('MAGAZINE', 'FANZINE'):
                                        self.reference_title_count += 1
			if oldTitle:
				oldTitle.setType(title_data[TITLE_TTYPE])

			#############################
			# LENGTH
			#############################
			key = "title_storylen"+str(counter)
			if self.form.has_key(key):
                                newTitle.setLength(self.form[key].value)
                                if newTitle.length not in STORYLEN_CODES:
                                        self.error = 'Invalid short fiction length'
                                        return
                                if newTitle.length and newTitle.type != 'SHORTFICTION':
                                        self.error = 'Only SHORTFICTION titles can have Length values'
                                        return
			if oldTitle:
                                oldTitle.setLength(title_data[TITLE_STORYLEN])

			#############################
			# AUTHORS
			#############################
			author = 1
			author_list = []
			total_skips = 0
			while True:
				key = "title_author%s.%s" % (str(counter), str(author))
				if self.form.has_key(key):
					value = normAuthor(self.form[key].value)
					if value and (value not in author_list):
                                                author_list.append(value)
				else:
					total_skips += 1
					if total_skips > 10:
						break
				author += 1
			authors = '+'.join(author_list)

			if authors == '':
				key = "title_title"+str(counter)
				if self.form.has_key(key):
					self.error = "Entry must have an author. Title=%s" % (self.form[key].value)
				else:
					self.error = "Entry must have an author"
                                return
			else:
				newTitle.setAuthors(authors)

			if oldTitle:
				authors = SQLTitleAuthors(newTitle.id)
				newauthors = ''
				count = 1
				for author in authors:
					if count == 1:
						newauthors += author
					else:
						newauthors += '+'+author
					count += 1
				oldTitle.setAuthors(newauthors)

			if oldTitle:
				newTitle.setOldTitle(oldTitle)
			self.pushTitle(newTitle)

			counter += 1

                        if title_types.get('EDITOR', 0) > 1:
                                self.error = 'Multiple EDITOR titles are not allowed'
                                return

                        if title_types.get('CHAPBOOK', 0) > 1:
                                self.error = 'Multiple CHAPBOOK titles are not allowed'
                                return

                        # Check that the reference title was entered if it is an EditPub and 
                        # was NOT entered if it is another type of submission
                        # Currently disabled pending more debugging
##                        if self.reference_title_count:
##                                if reference_title == 'implied':
##                                        self.error = 'Except when editing publications, the reference title should not be entered in the '
##                                        self.error += 'Content section. It will be added automatically at submission creation time'
##                                        return
##                        else:
##                                if reference_title == 'explicit':
##                                        # The wording should be changed to match the wording in the JavaScript code.
##                                        self.error = 'When editing publications, the Regular Titles subsection of the Content'
##                                        self.error += ' section must contain one title whose type matches the publication type.'
##                                        self.error += ' For Magazine and Fanzine publications the matching title type should be EDITOR.'
##                                        return
##                                        pass

                        # Check that the entered title types are valid for the specified publication type
                        if self.pub_ctype not in ('MAGAZINE', 'FANZINE') and title_types.get('EDITOR', 0):
                                self.error = 'Only MAGAZINE and FANZINE publications can contain EDITOR titles'
                                return
                        
                        if self.pub_ctype != 'CHAPBOOK' and title_types.get('CHAPBOOK', 0):
                                self.error = 'Only CHAPBOOK publications can contain CHAPBOOK titles'
                                return

                        if self.pub_ctype == 'CHAPBOOK':
                                for title_type in ('ANTHOLOGY', 'COLLECTION', 'NONFICTION', 'NOVEL', 'OMNIBUS'):
                                        if title_types.get(title_type, 0):
                                                self.error = '%s titles are not allowed within CHAPBOOK publications' % title_type
                                                return

                        if self.pub_ctype in ('MAGAZINE', 'FANZINE') and title_types.get('NOVEL', 0):
                                self.error = 'NOVEL titles are not allowed in MAGAZINE/FANZINE publications. '
                                self.error += 'Use (Complete Novel) SERIALs instead. See Help for more details'
                                return


		###################################
		# REVIEW CONTENT
		###################################
		counter = 1
		while counter:
			#############################
			# TITLE
			#############################
			key = "review_title"+str(counter)
			oldReview = 0
			if self.form.has_key(key):
				newReview = reviewEntry()
				try:
					newReview.setTitle(self.form[key].value)
				except:
					self.error = "Could not read the value associated with %s" % key
					break

				key = "review_id"+str(counter)
				if self.form.has_key(key):
					newReview.setID(self.form[key].value)
					if int(newReview.id) > 0:
						oldReview = reviewEntry()
						title_data = SQLloadTitle(newReview.id)
						oldReview.setTitle(title_data[TITLE_TITLE])
						oldReview.setID(newReview.id)
			else:
				key = "review_page"+str(counter)
				if self.form.has_key(key):
					self.error = "Reviews must have a title. Page=%s" % (self.form[key].value)
					return
				key = "review_author%s.1" % str(counter)
				if self.form.has_key(key):
					self.error = "Reviews must have a title. Author=%s" % (self.form[key].value)
					return
				# Check if this is the last submitted Review record
				if lastRecord(self.form, "review_title", counter):
                                        break
                                else:
					counter += 1
					continue

			#############################
			# PAGE
			#############################
			key = "review_page"+str(counter)
			if self.form.has_key(key):
                                page_number = self.form[key].value
                                if len(page_number) > 20:
                                        key = "review_title"+str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Title=%s" % (self.form[key].value)
                                                return
                                        key = "review_author%s.1" % str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Author=%s" % (self.form[key].value)
                                                return
				newReview.setPage(page_number)
                        if oldReview:
                                title_page = SQLGetPageNumber(oldReview.id, self.pub_id)
                                if title_page:
                                        oldReview.setPage(title_page)

			#############################
			# DATE
			#############################
			key = "review_date"+str(counter)
			if self.form.has_key(key):
				newReview.setDate(self.form[key].value)
			else:
				newReview.setDate(self.pub_year)
			if oldReview:
				oldReview.setDate(title_data[TITLE_YEAR])

			#############################
			# BOOK AUTHORS
			#############################
			author = 1
			author_list = []
			total_skips = 0
			while True:
				key = "review_author%s.%s" % (str(counter), str(author))
				if self.form.has_key(key):
					value = normAuthor(self.form[key].value)
					if value and (value not in author_list):
                                                author_list.append(value)
				else:
					total_skips += 1
					if total_skips > 10:
						break
				author += 1
			authors = '+'.join(author_list)

			if authors == '':
				key = "review_title"+str(counter)
				if self.form.has_key(key):
					self.error = "Reviews must specify at least one reviewed author. Title=%s" % (self.form[key].value)
				else:
					self.error = "Reviews must specify at least one reviewed author"
				return
			else:
				newReview.setBookAuthors(authors)

			if oldReview:
				authors = SQLReviewAuthors(newReview.id)
				newauthors = ''
				count = 1
				for author in authors:
					if count == 1:
						newauthors += author
					else:
						newauthors += '+'+author
					count += 1
				oldReview.setBookAuthors(newauthors)


			#############################
			# REVIEWER
			#############################
			author = 1
			author_list = []
			total_skips = 0
			while True:
				key = "review_reviewer%s.%s" % (str(counter), str(author))
				if self.form.has_key(key):
					value = normAuthor(self.form[key].value)
					if value and (value not in author_list):
                                                author_list.append(value)
				else:
					total_skips += 1
					if total_skips > 10:
						break
				author += 1
			authors = '+'.join(author_list)

			if authors == '':
				key = "review_title"+str(counter)
				if self.form.has_key(key):
					self.error = "Reviews must specify at least one reviewer. Title=%s" % (self.form[key].value)
				else:
					self.error = "Reviews must specify at least one reviewer"
				return
			else:
				newReview.setReviewers(authors)

			if oldReview:
				reviewers = SQLTitleAuthors(newReview.id)
				newreviewers = ''
				count = 1
				for reviewer in reviewers:
					if count == 1:
						newreviewers += reviewer
					else:
						newreviewers += '+'+reviewer
					count += 1
				oldReview.setReviewers(newreviewers)

			if oldReview:
				newReview.setOldReview(oldReview)
			self.pushReview(newReview)

			counter += 1


		###################################
		# INTERVIEW CONTENT
		###################################
		counter = 1
		while counter:
			#############################
			# TITLE
			#############################
			key = "interview_title"+str(counter)
			oldInterview = 0
			if self.form.has_key(key):
				newInterview = interviewEntry()
				newInterview.setTitle(self.form[key].value)
				key = "interview_id"+str(counter)
				if self.form.has_key(key):
					newInterview.setID(self.form[key].value)
					if int(newInterview.id) > 0:
						oldInterview = interviewEntry()
						title_data = SQLloadTitle(newInterview.id)
						oldInterview.setTitle(title_data[TITLE_TITLE])
						oldInterview.setID(newInterview.id)
			else:
				key = "interview_page"+str(counter)
				if self.form.has_key(key):
					self.error = "Interviews must have a title. Page=%s" % (self.form[key].value)
					return
				key = "interviewee_author%s.1" % str(counter)
				if self.form.has_key(key):
					self.error = "Interviews must have a title. Interviewee=%s" % (self.form[key].value)
					return
				key = "interviewer_author%s.1" % str(counter)
				if self.form.has_key(key):
					self.error = "Interviews must have a title. Interviewer=%s" % (self.form[key].value)
					return
				# Check if this is the last submitted Interview record
				if lastRecord(self.form, "interview_title", counter):
                                        break
                                else:
					counter += 1
					continue
			
			#############################
			# PAGE
			#############################
			key = "interview_page"+str(counter)
			if self.form.has_key(key):
                                page_number = self.form[key].value
                                if len(page_number) > 20:
                                        key = "interview_title"+str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Title=%s" % (self.form[key].value)
                                                return
                                        key = "interview_author%s.1" % str(counter)
                                        if self.form.has_key(key):
                                                self.error = "Page numbers must be 20 characters or less. Author=%s" % (self.form[key].value)
                                                return
				newInterview.setPage(page_number)
                        if oldInterview:
                                title_page = SQLGetPageNumber(oldInterview.id, self.pub_id)
                                if title_page:
                                        oldInterview.setPage(title_page)

			#############################
			# DATE
			#############################
			key = "interview_date"+str(counter)
			if self.form.has_key(key):
				newInterview.setDate(self.form[key].value)
			else:
				newInterview.setDate(self.pub_year)
			if oldInterview:
				oldInterview.setDate(title_data[TITLE_YEAR])


			#############################
			# INTERVIEWEE
			#############################
			author = 1
			author_list = []
			total_skips = 0
			while True:
				key = "interviewee_author%s.%s" % (str(counter), str(author))
				if self.form.has_key(key):
					value = normAuthor(self.form[key].value)
					if value and (value not in author_list):
                                                author_list.append(value)
				else:
					total_skips += 1
					if total_skips > 10:
						break
				author += 1
			authors = '+'.join(author_list)

			if authors == '':
				key = "interview_title"+str(counter)
				if self.form.has_key(key):
					self.error = "Interviews must specify at least one interviewed author. Title=%s" % (self.form[key].value)
				else:
					self.error = "Interviews must specify at least one interviewed author"
				return
			else:
				newInterview.setInterviewees(authors)

			if oldInterview:
				authors = SQLInterviewAuthors(newInterview.id)
				newauthors = ''
				count = 1
				for author in authors:
					if count == 1:
						newauthors += author
					else:
						newauthors += '+'+author
					count += 1
				oldInterview.setInterviewees(newauthors)

			#############################
			# INTERVIEWER
			#############################
			author = 1
			author_list = []
			total_skips = 0
			while True:
				key = "interviewer_author%s.%s" % (str(counter), str(author))
				if self.form.has_key(key):
					value = normAuthor(self.form[key].value)
					if value and (value not in author_list):
                                                author_list.append(value)
				else:
					total_skips += 1
					if total_skips > 10:
						break
				author += 1
			authors = '+'.join(author_list)

			if authors == '':
				key = "interview_title"+str(counter)
				if self.form.has_key(key):
					self.error = "Interviews must specify at least one interviewer. Title=%s" % (self.form[key].value)
				else:
					self.error = "Interviews must specify at least one interviewer"
				return
			else:
				newInterview.setInterviewers(authors)

			if oldInterview:
				interviewers = SQLTitleAuthors(newInterview.id)
				newinterviewers = ''
				count = 1
				for interviewer in interviewers:
					if count == 1:
						newinterviewers += interviewer
					else:
						newinterviewers += '+'+interviewer
					count += 1
				oldInterview.setInterviewers(newinterviewers)

			if oldInterview:
				newInterview.setOldInterview(oldInterview)
			self.pushInterview(newInterview)
			counter += 1

        def PrintPrimaryVerifications(self):
                primary_verifications = SQLPrimaryVerifiers(self.pub_id)
                if not primary_verifications:
                        return
                print '<div class="VerificationBox">'
                print '<h2>Primary Verifications</h2>'
                print '<table>'
                print '<tr class="table1">'
                print '<th>Verifier</th>'
                print '<th>Date</th>'
                print '<th>Type</th>'
                print '<th>Last User Activity Date</th>'
                print '</tr>'
                for verification in primary_verifications:
                        user_id = verification[0]
                        user_name = verification[1]
                        ver_time = verification[2]
                        ver_transient = verification[3]
                        print '<tr class="table2">'
                        print '<td><a href="%s://%s/index.php/User:%s">%s</a></td>' % (PROTOCOL, WIKILOC, user_name, user_name)
                        print '<td class="keep">%s</td>' % ver_time
                        if ver_transient:
                                print '<td class="keep">Transient</td>'
                        else:
                                print '<td class="keep">Permanent</td>'
                        last_user_activity = SQLLastUserActivity(user_id)
                        print '<td>%s</td>' % last_user_activity
                        print '</tr>'
                print '</table>'
                print '</div>'

        def PrintAllSecondaryVerifications(self):
                print '<div class="VerificationBox">'
                secondary_verifications = SQLSecondaryVerifications(self.pub_id)
                RefList = SQLGetRefDetails()
                self.PrintSecondaryVerificationsHeaders()
                for reference in RefList:
                        print '<tr>'
                        print '<td class="label"><a href="%s">%s</a></td>' % (reference[REFERENCE_URL], reference[REFERENCE_LABEL])
                        found = 0
                        for verification in secondary_verifications:
                                if verification[VERIF_REF_ID] == reference[REFERENCE_ID]:
                                        name = SQLgetUserName(verification[VERIF_USER_ID])
                                        if verification[VERIF_STATUS] == 0:
                                                print '<td class="drop"><b>Not Verified</b></td>'
                                                print '<td class="drop">&nbsp;</td>'
                                                print '<td class="drop">&nbsp;</td>'
                                        elif verification[VERIF_STATUS] == 1:
                                                print '<td class="keep">Verified</td>'
                                                print '<td class="keep"><a href="%s://%s/index.php/User:%s">%s</a></td>' % (PROTOCOL, WIKILOC, name, name)
                                                print '<td class="keep">%s</td>' % verification[VERIF_TIME]
                                        elif verification[VERIF_STATUS] == 2:
                                                print '<td class="label">N/A</td>'
                                                print '<td class="label"><a href="%s://%s/index.php/User:%s">%s</a></td>' % (PROTOCOL, WIKILOC, name, name)
                                                print '<td class="label">%s</td>' % verification[VERIF_TIME]
                                        found = 1
                                        break
                        if not found:
                                print '<td class="drop"><b>Not Verified</b></td>'
                                print '<td class="drop">&nbsp;</td>'
                                print '<td class="drop">&nbsp;</td>'
                        print '</tr>'
                print '</table>'
                print '</div>'

        def PrintActiveSecondaryVerifications(self):
                secondary_verifications = SQLActiveSecondaryVerifications(self.pub_id)
                if not secondary_verifications:
                        return
                print '<div class="VerificationBox">'
                self.PrintSecondaryVerificationsHeaders()
                for verification in secondary_verifications:
                        print '<tr>'
                        print '<td class="label"><a href="%s">%s</a></td>' % (verification[3], verification[2])
                        print '<td class="keep">Verified</td>'
                        name = SQLgetUserName(verification[0])
                        print '<td class="keep"><a href="%s://%s/index.php/User:%s">%s</a></td>' % (PROTOCOL, WIKILOC, name, name)
                        print '<td class="keep">%s</td>' % verification[1]
                        print '</tr>'
                print '</table>'
                print '</div>'

        def PrintSecondaryVerificationsHeaders(self):
                print '<h2>Secondary Verifications</h2>'
                print '<table>'
                print '<tr class="table1">'
                print '<th>Source</th>'
                print '<th>Status</th>'
                print '<th>Verifier</th>'
                print '<th>Date</th>'
                print '</tr>'

        def printExternalIDs(self, format = 'list'):
                if not self.identifiers:
                        if format == 'list':
                                # If this is an empty table cell, display a hyphen
                                print '-'
                        return
                formatted_ids = self.formatExternalIDs()
                if format == 'list':
                        print '  <ul class="noindent">'
                for formatted_id in formatted_ids:
                        if format == 'list':
                                print '<li>',formatted_id
                        else:
                                print formatted_id,'<br>'
                if format == 'list':
                        print '  </ul>'

        def formatExternalIDs(self):
                formatted_ids = []
                sites = SQLLoadIdentifierSites()
                types = SQLLoadIdentifierTypes()
                for type_name in sorted(self.identifiers.keys()):
                        formatted_line = FormatExternalIDType(type_name, types)
                        for id_value in self.identifiers[type_name]:
                                type_id = self.identifiers[type_name][id_value][0]
                                type_full_name = self.identifiers[type_name][id_value][1]
                                formatted_id = FormatExternalIDSite(sites, type_id, id_value)
                                formatted_line += ' %s' % formatted_id
                        formatted_ids.append(formatted_line)
                return formatted_ids

        def printModNoteRequired(self):
                user = User()
                user.load()
                mod_note_required = 0
                if self.requiresModeratorNote(user.id):
                        mod_note_required = 1
                print '<input name="mod_note_required" value="%d" type="HIDDEN">' % mod_note_required


        def requiresModeratorNote(self, user_id):
                # Returns 1 if there is at least one primary verifier who is not the current user
                verifiers = SQLPrimaryVerifiers(self.pub_id)
                for verifier in verifiers:
                        if int(verifier[0]) != int(user_id):
                                return 1
                return 0

class pubBody():
        def __init__(self):
                self.body = ''
                self.pub = pubs(db)
                self.userid = ''
                self.titles = []

        def build_page_body(self):
                self.body = '<div class="ContentBox">'
                self._build_image()
                self._build_pub_title_line()
                self._build_magazine_link()

        def _build_image(self):
                if not self.pub.pub_image:
                        return
		self.body += '<table>'
		self.body += '<tr class="scan">'
		self.body += '<td>'
                image = self.pub.pub_image.split("|")[0]
		self.body += '<a href="%s"><img src="%s" ' % (image, image)
		self.body += 'alt="picture" class="scan"></a></td>'
		self.body += '<td class="pubheader">'

        def _build_pub_title_line(self):
                self.body += '<ul>'
                self.body += '<li><b>Publication:</b> '
                self.body += ISFDBMouseover(self.pub.pub_trans_titles, self.pub.pub_title, '')
                self.body += buildRecordID('Publication', self.pub.pub_id, self.userid, None, 1)

        def _build_magazine_link(self):
                # Display a link to other issues for Magazines
                if not self.pub.pub_ctype in ('MAGAZINE', 'FANZINE'):
                        return

                editor = ''
                # Find the EDITOR Title in this Magazine issues
                for title in self.titles:
                        if title[TITLE_TTYPE] != 'EDITOR':
                                continue
                        editor = title
                # Check that the editor Title was found -- some issues may not have it
                if not editor:
                        return

                # If there is a parent EDITOR record, load it instead of the child EDITOR record
                if editor[TITLE_PARENT]:
                        editor = SQLloadTitle(editor[TITLE_PARENT])
                # If this EDITOR record is in a Series, link to that Series
                if editor[TITLE_SERIES]:
                        self.body += ' (%s)' % ISFDBLinkNoName('pe.cgi', editor[TITLE_SERIES], 'View All Issues')
                        self.body += ' (%s)' % ISFDBLinkNoName('seriesgrid.cgi', editor[TITLE_SERIES], 'View Issue Grid')
                # If the EDITOR record is not in a Series, check the number of magazine pubs for the record
                else:
                        pubs_for_editor = SQLGetPubsByTitle(editor[TITLE_PUBID])
                        # Link the EDITOR record directly if it has more than 1 issue
                        if len(pubs_for_editor) > 1:
                                self.body += ' (%s)' % ISFDBLinkNoName('title.cgi', editor[TITLE_PUBID], 'View All Issues')
