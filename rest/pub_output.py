#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2022   Al von Ruff, Ahasuerus and Lokal_Profil
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
        printTag(len(pub_bodies), 'Records', indent=1)
        print '  <Publications>'
        for pub_body in pub_bodies:
                print '    <Publication>'
                onePubOutput(pub_body)
                print '    </Publication>'
        print '  </Publications>'
        print '</ISFDB>'

def onePubOutput(publication):

        pub = pubs(db)
        pub.pub_id = publication[PUB_PUBID]

        printTag(pub.pub_id, 'Record')
        printTag(publication[PUB_TITLE], Title)
        authors = SQLPubAuthors(pub.pub_id)
        printMultiValued(authors, 'Authors', 'Author')

        if publication[PUB_YEAR]:
                printTag(convertDate(publication[PUB_YEAR], 1), 'Year')
        printTag(publication[PUB_ISBN], 'Isbn')
        printTag(publication[PUB_CATALOG], 'Catalog')
        if publication[PUB_PUBLISHER]:
                publisher = SQLGetPublisher(publication[PUB_PUBLISHER])
                printTag(publisher[PUBLISHER_NAME], 'Publisher')
        if publication[PUB_SERIES]:
                pubseries = SQLGetPubSeries(publication[PUB_SERIES])
                printTag(pubseries[PUB_SERIES_NAME], 'PubSeries')
        printTag(publication[PUB_SERIES_NUM], 'PubSeriesNum')
        printTag(publication[PUB_PRICE], 'Price')
        printTag(publication[PUB_PAGES], 'Pages')
        printTag(publication[PUB_PTYPE], 'Binding')
        printTag(publication[PUB_CTYPE], 'Type')
        printTag(publication[PUB_TAG], 'Tag')
        printTag(publication[PUB_IMAGE], 'Image')

        artists = SQLPubArtists(pub.pub_id)
        printMultiValued(artists, 'CoverArtists', 'Artist')

        if publication[PUB_NOTE]:
                notes = SQLgetNotes(publication[PUB_NOTE])
                printTag(notes, 'Note')

        pub.loadExternalIDs()
        if pub.identifiers:
                print pub.xmlIdentifiers(1)

        pub.loadPubWebpages()
        printMultiValued(pub.pub_webpages, 'Webpages', 'Webpage')

        pub.loadTransTitles()
        printMultiValued(pub.pub_trans_titles, 'TransTitles', 'TransTitle')

def printTag(value, tag, indent=3, linebreak=False):
        if not value:
                return
        if linebreak:
                internal = '\n%s%s\n%s' % ('  ' * (indent + 1), XMLescape(value, 1),'  ' * indent)
        else:
                internal = XMLescape(value, 1)
        print '%s<%s>%s</%s>' % ('  ' * indent, tag, internal, tag)

def printMultiValued(values, outer_tag, inner_tag, indent=3):
        if not values:
                return
        output = '%s<%s>\n' % ('  ' * indent, outer_tag)
        for value in values:
                output += '%s<%s>%s</%s>\n' % ('  ' * (indent + 1), inner_tag, XMLescape(value, 1), inner_tag)
        output += '%s</%s>\n' % ('  ' * indent, outer_tag)
        print output
