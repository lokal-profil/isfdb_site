#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

        title_id = SESSION.Parameter(0, 'int')
        title = SQLgetTitle(title_id)
        if not title:
		SESSION.DisplayError('Title Does Not Exist')

	PrintHeader('All Covers for %s' % title)
	PrintNavbar('titlecovers', 0, 0, 'titlecovers.cgi', title_id)

        pubs = SQLGetPubsByTitle(title_id)
        count = 0
        for pub in pubs:
                if pub[PUB_IMAGE]:
                        print ISFDBLinkNoName("pl.cgi", pub[PUB_PUBID], '<img src="%s" alt="Coverart" class="scans">' % pub[PUB_IMAGE].split("|")[0])
                        count += 1
        if not count:
                print '<h3>No covers for %s</h3>' % title

        print '<p>%s' % ISFDBLinkNoName('title.cgi', title_id, '<b>Back to the Title page for %s</b>' % title, True)

	PrintTrailer('titlecovers', title_id, title_id)
