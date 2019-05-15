#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2018   Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 152 $
#     Date: $Date: 2018-06-19 11:47:00 -0400 (Tue, 19 Jun 2018) $


from common import *

if __name__ == '__main__':

	PrintHeader('Authors By Debut Year')
	PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        print '<a href="http:/%s/authors_by_debut_year.cgi?0">Prior to 1900</a>' % HTFAKE
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th colspan="10">Years</th>'
        print '</tr>'
        PrintAnnualGrid(1900, 'authors_by_debut_year', '', 0, '')
	PrintTrailer('frontpage', 0, 0)
