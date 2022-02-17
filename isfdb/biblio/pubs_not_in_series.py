#!_PYTHONLOC
#
#     (C) COPYRIGHT 2016-2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from common import *


if __name__ == '__main__':

        publisher_id = SESSION.Parameter(0, 'int')
        publisher = SQLGetPublisher(publisher_id)
        if not publisher:
                SESSION.DisplayError('Publisher not found')

	title = 'Publications not in a Publication Series for Publisher: %s' % publisher[PUBLISHER_NAME]
	PrintHeader(title)
	PrintNavbar('pubs_not_in_series', publisher_id, publisher_id, 'pubs_not_in_series.cgi', publisher_id)

        print 'Publications not in a Publication Series for Publisher: %s<p>' % ISFDBLink('publisher.cgi', publisher_id, publisher[PUBLISHER_NAME])
	pubs = SQLGetPubsNotInSeries(publisher_id)
	PrintPubsTable(pubs, 'pubs_not_in_series')

	PrintTrailer('pubs_not_in_series', publisher_id, publisher_id)
