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

class AdvancedAwardSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Award Search')
                PrintNavbar('adv_award_search', 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                self.print_full_header()
                self.print_award_search()
                PrintTrailer('adv_award_search', 0, 0)

        def print_award_search(self):
                print '<h2>Award Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                for number in range(1, self.max_term + 1):
                        self.print_award_selectors(number)
                self.print_award_sort_by()
                self.print_submit_button('Award')

        def print_award_selectors(self, number):
                print '<p id="award_selectors_%d">' % number
                print '<select NAME="USE_%d" id="award_%d">' % (number, number)
                print '<option VALUE="award_year">Award Year'
                print '<option VALUE="award_level">Award Level'
                print '<option VALUE="award_cat_name">Award Category'
                print '<option VALUE="award_type_short_name">Award Type Short Name'
                print '<option VALUE="award_type_full_name">Award Type Full Name'
                print '<option VALUE="note">Notes'
                print '</select>'

                self.print_operators('award', number)

                print '<input id="awardterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_award_sort_by(self):
                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                print '<option SELECTED VALUE="award_year">Award Year'
                print '<option VALUE="award_level">Award Level'
                print '</select>'

        
if __name__ == '__main__':
        search = AdvancedAwardSearch()
        search.display_selection()
