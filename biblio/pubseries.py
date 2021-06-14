#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2021   Ahasuerus, Bill Longley and Dirk Stoecker
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
from login import *


def DisplayError(message):
        PrintHeader('Publication Series Error')
        PrintNavbar('pub_series', '', 0, 'ea.cgi', '')
        print '<h2>Error: %s.</h2>' % message
        PrintTrailer('pub_series', '', 0)
        sys.exit(0)


if __name__ == '__main__':

        try:
                pub_series_id = str(int(sys.argv[1]))
                pub_series = SQLGetPubSeries(pub_series_id)
                if not pub_series:
                        raise
	except:
                DisplayError('Publication series not found')

	messages = {}
	messages[0] = 'Show earliest year first'
	messages[1] = 'Show last year first'
	messages[2] = 'Sort by series number'
	messages[3] = 'Show covers'
	try:
                # Get the display order
                display_order = int(sys.argv[2])
        except:
                # The default is descending
                display_order=0

        if display_order not in messages:
                DisplayError('Invalid argument')

        user = User()
        user.load()

	title = 'Publication Series: %s' % pub_series[PUB_SERIES_NAME]
	PrintHeader(title)
	PrintNavbar('pub_series', pub_series_id, pub_series_id, 'pubseries.cgi', pub_series_id)

	print '<div class="ContentBox">'
        other_series = SQLGetSimilarRecords(pub_series_id, pub_series[PUB_SERIES_NAME], 'pub_series', 'pub_series_id', 'pub_series_name')
        if other_series:
                print '<h3>Note: There are other publication series with the same name:'
                displayRecordList('pub_series', other_series)
                print '</h3>'
	print '<ul>'
        # Transliterated name(s)
        trans_names = SQLloadTransPubSeriesNames(pub_series_id)
        print '<li><b>Publication Series: </b>%s' % ISFDBMouseover(trans_names, pub_series[PUB_SERIES_NAME], '')
        printRecordID('Pub. Series', pub_series_id, user.id)

	# Webpages
	webpages = SQLloadPubSeriesWebpages(int(pub_series_id))
	PrintWebPages(webpages)

	# Note
	if pub_series[PUB_SERIES_NOTE]:
		print '<li>'
		notes = SQLgetNotes(pub_series[PUB_SERIES_NOTE])
		print FormatNote(notes, 'Note', 'short', pub_series_id, 'Pubseries')

	print '</ul>'
	print '</div>'

	print '<div class="ContentBox">'
	output = ''
	for message_number in sorted(messages.keys()):
                if message_number != display_order:
                        if output:
                                output += ' %s ' % BULLET
                        output += '<a href="http:/%s/pubseries.cgi?%d+%d">%s</a>' % (HTFAKE,
                                                                                     int(pub_series_id),
                                                                                     message_number,
                                                                                     messages[message_number])
        print output,'<p>'
        if display_order == 3:
                pubs = SQLGetPubSeriesPubs(pub_series_id, 2)
                count = 0
                for pub in pubs:
                        if pub[PUB_IMAGE]:
                                print ISFDBLink("pl.cgi", pub[PUB_PUBID],
                                                '<img src="%s" alt="Coverart" class="scans">' % pub[PUB_IMAGE].split("|")[0])
                                count += 1
                if not count:
                        print '<h3>No covers for %s</h3>' % pub_series[PUB_SERIES_NAME]
        else:
                pubs = SQLGetPubSeriesPubs(pub_series_id, display_order)
                PrintPubsTable(pubs, 'pubseries')
	print '</div>'

	PrintTrailer('pub_series', pub_series_id, pub_series_id)
