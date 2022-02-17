#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2021   Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *

if __name__ == '__main__':

	PrintHeader('Authors By Debut Year')
	PrintNavbar('authors_by_debut_year', 0, 0, 'authors_by_debut_year.cgi', 0)

        print ISFDBLink('authors_by_debut_year.cgi', '0', 'Prior to 1900')
        print '<table class="seriesgrid">'
        print '<tr>'
        print '<th colspan="10">Years</th>'
        print '</tr>'
        PrintAnnualGrid(1900, 'authors_by_debut_year', '', 0, '')
	PrintTrailer('frontpage', 0, 0)
