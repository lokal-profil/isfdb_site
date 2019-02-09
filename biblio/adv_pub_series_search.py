#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 318 $
#     Date: $Date: 2019-01-12 19:09:26 -0500 (Sat, 12 Jan 2019) $


import sys
import string
from isfdb import *
from SQLparsing import *
from common import *
from advSearchClass import AdvancedSearch

class AdvancedPubSeriesSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Publication Series Search')
                PrintNavbar('adv_pub_series_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_pub_search()
                PrintTrailer('adv_pub_series_search', 0, 0)

        def print_pub_search(self):
                print '<h2>Publication Series Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                for number in range(1, self.max_term + 1):
                        self.print_pub_series_selectors(number)
                self.print_pub_series_sort_by()
                self.print_submit_button('Publication Series')

        def print_pub_series_selectors(self, number):
                print '<p id="pub_series_selectors_%d">' % number
                print '<select NAME="USE_%d" id="pub_series_%d">' % (number, number)
                print '<option VALUE="pub_series_name">Publication Series Name'
                print '<option VALUE="trans_pub_series_name">Transliterated Publication Series Name'
                print '<option VALUE="pub_series_note">Notes'
                print '<option VALUE="pub_series_webpage">Webpage'
                print '</select>'

                self.print_operators('pub_series', number)

                print '<input id="pub_series_term_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_pub_series_sort_by(self):
                print '<input NAME="ORDERBY" VALUE="pub_series_name" TYPE="HIDDEN">'

        
if __name__ == '__main__':
        search = AdvancedPubSeriesSearch()
        search.display_selection()
