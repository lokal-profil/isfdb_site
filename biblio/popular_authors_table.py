#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
from SQLparsing import *
from biblio import *


def ErrorBox(message):
	PrintHeader("Authors/Editors Ranked by Awards and Nominations")
	PrintNavbar('top', 0, 0, 'popular_authors_table.cgi', 0)
        print '<div id="ErrorBox">'
        print "<h3>%s.</h3>" % (message)
        print '</div>'
        PrintTrailer('popular_authors_table', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
		type = int(sys.argv[1])
		if type == 0:
                        author_type = 'Authors and Editors'
		elif type == 1:
                        author_type = 'Novel Authors'
                elif type == 2:
                        author_type = 'Short Fiction Authors'
                elif type == 3:
                        author_type = 'Collection Authors'
                elif type == 4:
                        author_type = 'Anthology Editors'
                elif type == 5:
                        author_type = 'Non-Fiction Authors'
                elif type == 6:
                        author_type = 'Other Title Types Authors'
                else:
                        raise
	except:
                ErrorBox("Invalid author/editor type")

	PrintHeader("%s Ranked by Awards and Nominations" % author_type)
	PrintNavbar('top', 0, 0, 'popular_authors_table.cgi', 0)

        print '<h3><a href="http:/%s/popular_authors.cgi?%d+all">Highest Ranked %s of All Time</a></h3>' % (HTFAKE, type, author_type)
        print '<h3><a href="http:/%s/popular_authors.cgi?%d+pre1950">Highest Ranked %s Prior to 1950</a></h3>' % (HTFAKE, type, author_type)

        print '<h3>Highest Ranked %s Since 1950 by Decade:</h3>' % author_type
        # Set the end decade to the decade of the current year
        endyear = localtime()[0]
        enddecade = endyear/10
        print '<ul>'
        for decade in range(195, enddecade+1):
                print '<li><a href="http:/%s/popular_authors.cgi?%d+decade+%d0">%d0s</a>' % (HTFAKE, type, decade, decade)
	
	PrintTrailer('top', 0, 0)

