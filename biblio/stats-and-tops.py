#!_PYTHONLOC
#
#     (C) COPYRIGHT 2013-2018   Ahasuerus
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
from biblio import *

if __name__ == '__main__':

	PrintHeader('ISFDB Statistics and Top Lists')
	PrintNavbar('stats', 0, 0, 'stats-and-tops.cgi', 0)

	print 'Note that some of these lists are created on demand and some are regenerated nightly'
	print '<h3>Database Statistics</h3>'
	print '<ul>'

        print '<li><a href="http:/%s/stats.cgi?4">Summary Database Statistics</a>' % (HTFAKE)
        print '<li><a href="http:/%s/stats.cgi?11">Submissions per Year</a>' % (HTFAKE)
        print '<li><a href="http://%s/index.php/Annual_Page_Views_and_Database_Growth">Database Growth and Annual Page Views</a>' % (WIKILOC)
        print '</ul>'
	print '<h4>Author Statistics</h4>'
	print '<ul>'
        print '<li><a href="http:/%s/authors_by_debut_year_table.cgi">Authors By Debut Year</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_viewed.cgi?authors">Most-Viewed Authors</a>' % (HTFAKE)
        print '<li><a href="http://%s/degrees.html">Author Communities</a> [as of 2005]' % (HTMLHOST)
        print '<li>Authors by Age:'
        print '<ul>'
        print '<li><a href="http:/%s/oldest.cgi">Oldest Living Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/oldest_nl.cgi">Oldest Non-Living Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/youngest.cgi">Youngest Living Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/youngest_nl.cgi">Youngest Non-Living Authors</a>' % (HTFAKE)
        print '</ul>'
        print '<li>Authors/Editors Ranked by Awards and Nominations:'
        print '<ul>'
        print '<li><a href="http:/%s/popular_authors_table.cgi?0">All Authors and Editors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?1">Novel Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?2">Short Fiction Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?3">Collection Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?4">Anthology Editors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?5">Non-Fiction Authors</a>' % (HTFAKE)
        print '<li><a href="http:/%s/popular_authors_table.cgi?6">Other Types Authors and Editors</a>' % (HTFAKE)
        print '</ul>'
        print '</ul>'

	print '<h4>Language Statistics</h4>'
        print '<ul>'
        print '<li><a href="http:/%s/authors_by_language.cgi">Authors by Language</a>' % (HTFAKE)
        print '<li><a href="http:/%s/titles_by_language.cgi">Titles by Language</a>' % (HTFAKE)
        print '</ul>'
        
	print '<h4>Title Statistics</h4>'
        print '<ul>'
        print '<li><a href="http:/%s/stats.cgi?5">Titles by Year of First Publication</a>' % (HTFAKE)
        print '<li><a href="http:/%s/stats.cgi?7">Titles by Author Age</a>' % (HTFAKE)
        print '<li><a href="http://%s/agestuff.html">Award-Winning Titles by Author Age</a> [as of 2005, to be updated]' % (HTMLHOST)
        print '<li><a href="http:/%s/stats.cgi?8">Percent of Titles in Series by Year</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_reviewed_table.cgi">Most-Reviewed Titles (in genre publications)</a>' % (HTFAKE)
        print '<li>Titles Ranked by Awards and Nominations:'
        print '<ul>'
        print '<li><a href="http:/%s/most_popular_table.cgi?0">All Titles</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?1">Novels</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?2">Short Fiction</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?3">Collections</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?4">Anthologies</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?5">Non-Fiction</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_popular_table.cgi?6">Other Types</a>' % (HTFAKE)
        print '</ul>'
        print '<li><a href="http:/%s/top100.cgi?novel">Top 100 Novels as Voted by ISFDB Users</a>' % (HTFAKE)
        print '<li>Most-Viewed Titles:'
        print '<ul>'
        print '<li><a href="http:/%s/most_viewed.cgi?novels">Most-Viewed Novels</a>' % (HTFAKE)
        print '<li><a href="http:/%s/most_viewed.cgi?short">Most-Viewed Short Fiction</a>' % (HTFAKE)
        print '</ul>'
        print '</ul>'
        
	print '<h4>Publication Statistics</h4>'
        print '<ul>'
        print '<li><a href="http:/%s/stats.cgi?6">Publications by Year</a>' % (HTFAKE)
        print '<li><a href="http:/%s/stats.cgi?9">Percent of Books by Type by Year</a>' % (HTFAKE)
        print '<li><a href="http:/%s/stats.cgi?10">Percent of Publications by Format by Year</a>' % (HTFAKE)
        print '</ul>'
	print '<h3>Top ISFDB Editors</h3>'
        print '<ul>'
	print '<li><a href="http:/%s/stats.cgi?2">Top Verifiers</a>' % (HTFAKE)
	print '<li><a href="http:/%s/stats.cgi?1">Top Moderators</a>' % (HTFAKE)
	print '<li><a href="http:/%s/toptaggers.cgi">Top Taggers</a>' % (HTFAKE)
	print '<li><a href="http:/%s/topvoters.cgi">Top Voters</a>' % (HTFAKE)
	print '<li><a href="http:/%s/topcontrib.cgi">Top Contributors (All Submission Types)</a>' % (HTFAKE)
	print '<ul>'
	for type in sorted(SUBMAP.keys()):
                if SUBMAP[type][3]:
                        print '<li><a href="http:/%s/topcontrib.cgi?%d">Top Contributors (%s)</a>' % (HTFAKE, type, SUBMAP[type][3])
	print '</ul>'
        
	print '</ul>'
	PrintTrailer('frontpage', 0, 0)
