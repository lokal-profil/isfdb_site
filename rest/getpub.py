#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2017   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.11 $
#     Date: $Date: 2017/07/23 00:11:35 $

import sys
import string
from isfdb import *
from SQLparsing import *
from library import XMLescape
from isbn import *
from pubClass import pubs


def isbn10(isbn13):
	isbn = isbn13[3:12]
	counter = 0
	sum = 0
	mult = 1
	while counter < 9:
		sum += (mult * int(isbn[counter]))
		mult += 1
		counter += 1
	remain = sum % 11
	if remain == 10:
		isbn = isbn + 'X'
	else:
		isbn = isbn + str(remain)
	return isbn

def isbn13(isbn):
	isbn = string.replace(isbn, ' ', '')
	newISBN = '978' + isbn[0:9]
	try:
		sum1 = int(newISBN[0]) + int(newISBN[2]) + int(newISBN[4]) + int(newISBN[6]) + int(newISBN[8]) + int(newISBN[10])
		sum2 = int(newISBN[1]) + int(newISBN[3]) + int(newISBN[5]) + int(newISBN[7]) + int(newISBN[9]) + int(newISBN[11])
		checksum = sum1 + (sum2 * 3)
		remainder = checksum - ((checksum/10)*10)
		if remainder:
			remainder = 10 - remainder
		newISBN = newISBN + str(remainder)
		return newISBN
	except:
		return isbn

def displayPubAuthors(pub_id):
        authors = SQLPubAuthors(pub_id)
        for author in authors:
                print '        <Author>%s</Author>' % XMLescape(author, 1)

def PrintArtist(title_id):
	authors = SQLTitleAuthors(title_id)
	for author in authors:
                print '        <Artist>%s</Artist>' % XMLescape(author, 1)

def doRecord(publication):	

	print '    <Publication>'
	print '      <Record>%s</Record>' % (publication[PUB_PUBID])
	print '      <Title>%s</Title>' % XMLescape(publication[PUB_TITLE], 1)
	print '      <Authors>' 
	displayPubAuthors(publication[PUB_PUBID])
	print '      </Authors>'

	if publication[PUB_YEAR]:
		year = publication[PUB_YEAR][:4]
		if year == '0000':
			print '      <Year>unknown</Year>' 
		elif year == '8888':
			print '      <Year>unpublished</Year>' 
		else:
			print '      <Year>%s</Year>' % publication[PUB_YEAR]

	if publication[PUB_ISBN]:
		print '      <Isbn>%s</Isbn>' % XMLescape(publication[PUB_ISBN], 1)
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

def fetch_isbn(isbn, firsttry):
	query = "select * from pubs where pub_isbn='%s'" % db.escape_string(isbn)
	db.query(query)
	result = db.store_result()
	records = result.num_rows()

	if (records == 0) and firsttry:
		return(1)

	print '<?xml version="1.0" encoding="iso-8859-1" ?>'
	print '<ISFDB>'
	print '  <Records>%d</Records>' % records
	print '  <Publications>'

	record = result.fetch_row()
	while record:
		doRecord(record[0])
                record = result.fetch_row()
	return(0)


if __name__ == '__main__':

	print 'Content-type: text/html\n'

	try:
		isbn = string.replace(sys.argv[1], '-', '')
	except:
		print "getpub.cgi: Bad ISBN"
		sys.exit(1)

	not_found = fetch_isbn(isbn, 1)
	if not_found:
		if len(isbn) == 13:
			isbn = isbn10(isbn)
		elif len(isbn) == 10:
			isbn = isbn13(isbn)
		fetch_isbn(isbn, 0)

	print '  </Publications>'
	print '</ISFDB>'
