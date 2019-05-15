#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2018   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import sys
import string
from isfdb import *
from SQLparsing import *
from library import XMLescape, convertDate
from pubClass import pubs


def pubOutput(pub_bodies):
	print '<?xml version="1.0" encoding="iso-8859-1" ?>'
	print '<ISFDB>'
	print '  <Records>%d</Records>' % len(pub_bodies)
	print '  <Publications>'
	for pub_body in pub_bodies:
		onePubOutput(pub_body)
	print '  </Publications>'
	print '</ISFDB>'

def onePubOutput(publication):	

	print '    <Publication>'
	print '      <Record>%s</Record>' % (publication[PUB_PUBID])
	print '      <Title>%s</Title>' % XMLescape(publication[PUB_TITLE], 1)
	print '      <Authors>' 
	displayPubAuthors(publication[PUB_PUBID])
	print '      </Authors>'

	if publication[PUB_YEAR]:
                print '      <Year>%s</Year>' % convertDate(publication[PUB_YEAR], 1)
	if publication[PUB_ISBN]:
		print '      <Isbn>%s</Isbn>' % XMLescape(publication[PUB_ISBN], 1)
	if publication[PUB_CATALOG]:
		print '      <Catalog>%s</Catalog>' % XMLescape(publication[PUB_CATALOG], 1)
	if publication[PUB_PUBLISHER]:
		publisher = SQLGetPublisher(publication[PUB_PUBLISHER])
		print '      <Publisher>%s</Publisher>' % XMLescape(publisher[PUBLISHER_NAME], 1)
	if publication[PUB_SERIES]:
                pubseries = SQLGetPubSeries(publication[PUB_SERIES])
                print '      <PubSeries>%s</PubSeries>' % XMLescape(pubseries[PUB_SERIES_NAME], 1)
	if publication[PUB_SERIES_NUM]:
		print '      <PubSeriesNum>%s</PubSeriesNum>' % XMLescape(publication[PUB_SERIES_NUM], 1)
	if publication[PUB_PRICE]:
		price = publication[PUB_PRICE]
		print '      <Price>%s</Price>' % XMLescape(price, 1)
	if publication[PUB_PAGES]:
		print '      <Pages>%s</Pages>' % XMLescape(publication[PUB_PAGES], 1)
	if publication[PUB_PTYPE]:
		print '      <Binding>%s</Binding>' % XMLescape(publication[PUB_PTYPE], 1)
	if publication[PUB_CTYPE]:
		print '      <Type>%s</Type>' % XMLescape(publication[PUB_CTYPE], 1)
	if publication[PUB_TAG]:
		print '      <Tag>%s</Tag>' % XMLescape(publication[PUB_TAG], 1)
	if publication[PUB_IMAGE]:
		print '      <Image>%s</Image>' % XMLescape(publication[PUB_IMAGE], 1)

	titles = SQLloadTitlesXBT(publication[PUB_PUBID])

        # Create a list of artists
	artists = []
	for title in titles:
		if title[TITLE_TTYPE] == 'COVERART':
                        artists.append(title[TITLE_PUBID])
        # If any artists were found, print them out
        if artists:
                print '      <CoverArtists>'
                for artist in artists:
                        PrintArtist(artist)
                print '      </CoverArtists>'

	if publication[PUB_NOTE]:
		notes = SQLgetNotes(publication[PUB_NOTE])
		print '      <Note>%s</Note>' % XMLescape(notes, 1)

        pub = pubs(db)
        pub.pub_id = publication[PUB_PUBID]
        pub.loadExternalIDs()
        if pub.identifiers:
                print pub.xmlIdentifiers(1)
	print '    </Publication>'

def displayPubAuthors(pub_id):
        authors = SQLPubAuthors(pub_id)
        for author in authors:
                print '        <Author>%s</Author>' % XMLescape(author, 1)

def PrintArtist(title_id):
	authors = SQLTitleAuthors(title_id)
	for author in authors:
                print '        <Artist>%s</Artist>' % XMLescape(author, 1)
