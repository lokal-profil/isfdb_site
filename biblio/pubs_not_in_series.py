#!_PYTHONLOC
#
#     (C) COPYRIGHT 2016-2017   Ahasuerus
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


def DisplayError(message):
        PrintHeader('Publisher Error')
        PrintNavbar('publisher', '', 0, 'ea.cgi', '')
        print '<h2>Error: %s.</h2>' % message
        PrintTrailer('publisher', '', 0)
        sys.exit(0)


if __name__ == '__main__':

        try:
                publisher_id = str(int(sys.argv[1]))
                publisher = SQLGetPublisher(publisher_id)
                if not publisher:
                        raise
	except:
                DisplayError('Publisher not found')

	title = 'Publications not in a Publication Series for Publisher: %s' % publisher[PUBLISHER_NAME]
	PrintHeader(title)
	PrintNavbar('publisher', publisher_id, publisher_id, 'publisher.cgi', publisher_id)

        print 'Publications not in a Publication Series for Publisher: %s<p>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME])
	pubs = SQLGetPubsNotInSeries(publisher_id)
	PrintPubsTable(pubs, 'pubs_not_in_series')

	PrintTrailer('publisher', publisher_id, publisher_id)
