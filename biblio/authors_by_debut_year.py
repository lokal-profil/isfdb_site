#!_PYTHONLOC
#
#     (C) COPYRIGHT 20011-2014   Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *

if __name__ == '__main__':

        try:
                decade = int(sys.argv[1])
                header = 'Authors By Debut Year'
                if decade > 100:
                        header += ' - %d0s' % decade
                else:
                        header += ' - Prior to 1900'
        except:
                decade = 0
                header = 'Authors By Debut Year'
	PrintHeader(header)
	PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        # If no decade was specified, then list all decades that the data is available for
        if not decade:
                # Set the end decade to the decade of the current year
                endyear = localtime()[0]
                enddecade = endyear/10
                print '<h3>Select a time period:</h3>'
                print '<ul>'
                print '<li><a href="http:/%s/authors_by_debut_year.cgi?100">Prior to 1900</a>' % HTFAKE
                for decade in range(190, enddecade+1):
                        print '<li><a href="http:/%s/authors_by_debut_year.cgi?%d">%d0s</a>' % (HTFAKE, decade, decade)
                PrintTrailer('frontpage', 0, 0)
                sys.exit(0)

        try:
                filename = LOCALFILES + "authors_by_debut_year_%d.html" % decade
                f = open(filename,"r")
                data = f.read()
                f.close()
                print '<h3>Includes novels, short fiction, serials, poems and collections:</h3>'
                print data
        except:
                print '<h3>No data for the specified decade</h3>'
	PrintTrailer('frontpage', 0, 0)
