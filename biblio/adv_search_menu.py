#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2019   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 332 $
#     Date: $Date: 2019-02-02 19:56:04 -0500 (Sat, 02 Feb 2019) $


import sys
import string
from isfdb import *
from SQLparsing import *
from common import *
from advSearchClass import AdvancedSearch

class AdvancedSearchSelection(AdvancedSearch):
        def __init__(self):
                pass
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Search')
                PrintNavbar('adv_search_menu', 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                print '<ul>'
                print '<li>A downloadable version of the ISFDB database is available <a href="http://%s/index.php/ISFDB_Downloads">here</a>' % WIKILOC
                print '</ul>'
                print '<hr>'
                print '<ul>'
                print '<li><b>Custom Searches of Individual Record Types:</b>'
                print '<ul>'
                print '<li><a href="http://%s/adv_author_search.cgi">Authors</a>' % HTFAKE
                print '<li><a href="http://%s/adv_title_search.cgi">Titles</a>' % HTFAKE
                print '<li><a href="http://%s/adv_series_search.cgi">Series</a>' % HTFAKE
                print '<li><a href="http://%s/adv_pub_search.cgi">Publications</a>' % HTFAKE
                print '<li><a href="http://%s/adv_publisher_search.cgi">Publishers</a>' % HTFAKE
                print '<li><a href="http://%s/adv_pub_series_search.cgi">Publication Series</a>' % HTFAKE
                print '<li><a href="http://%s/adv_award_type_search.cgi">Award Types</a>' % HTFAKE
                print '</ul>'
                print '<li><b>Other Searches:</b>'
                print '<ul>'
                print '<li><a href="http://%s/adv_identifier_search.cgi">Publication Search by External Identifier</a>' % HTFAKE
                print '<li><a href="http://%s/adv_notes_search.cgi">Notes Search</a>' % HTFAKE
                print '<li><a href="http://%s/adv_web_page_search.cgi">Web Page Search</a>' % HTFAKE
                print '<li><a href="http://%s/adv_user_search.cgi">User Search</a>' % HTFAKE
                print '</ul>'
                print '</ul>'
                print '<p><hr><p>'
                self.print_google_search()
                PrintTrailer('adv_search_menu', 0, 0)

        def print_google_search(self):
                print '<h2>Or Search ISFDB Using Google</h2>'
                print '<form METHOD="GET" action="http:/%s/google_search_redirect.cgi" accept-charset="utf-8">' % (HTFAKE)
                print '<p>'
                print '<select NAME="PAGE_TYPE">'
                print '<option VALUE="name">Name'
                print '<option VALUE="title">Title'
                print '<option VALUE="series">Series'
                print '<option VALUE="publication">Publication'
                print '<option VALUE="pubseries">Publication Series'
                print '<option VALUE="publisher">Publisher'
                print '<option VALUE="award_category">Award Category'
                print '</select>'

                print '<select NAME="OPERATOR">'
                print '<option VALUE="exact">contains exact word'
                print '<option SELECTED VALUE="approximate">contains approximate word'
                print '</select>'

                print '<input NAME="SEARCH_VALUE" SIZE="50">'
                print '<p>'

                print '<input TYPE="SUBMIT" VALUE="Submit Query">'
                print '</form>'

        
if __name__ == '__main__':
        search = AdvancedSearchSelection()
        search.display_selection()
