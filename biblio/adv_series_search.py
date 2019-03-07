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

class AdvancedSeriesSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Series Search')
                PrintNavbar('adv_series_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_search()
                PrintTrailer('adv_series_search', 0, 0)

        def print_search(self):
                print '<h2>Series Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                for number in range(1, self.max_term + 1):
                        self.print_series_selectors(number)
                self.print_series_sort_by()
                self.print_submit_button('Series')

        def print_series_selectors(self, number):
                print '<p id="series_selectors_%d">' % number
                print '<select NAME="USE_%d" id="series_%d">' % (number, number)
                print '<option VALUE="series_title">Series Name'
                print '<option VALUE="trans_series_name">Transliterated Series Name'
                print '<option VALUE="parent_series_name">Parent Series Name'
                print '<option VALUE="parent_series_position">Position within Parent Series'
                print '<option VALUE="series_note">Notes'
                print '<option VALUE="series_webpage">Webpage'
                print '</select>'

                self.print_operators('series', number)

                print '<input id="series_term_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_series_sort_by(self):
                print '<input NAME="ORDERBY" VALUE="series_title" TYPE="HIDDEN">'

        
if __name__ == '__main__':
        search = AdvancedSeriesSearch()
        search.display_selection()
