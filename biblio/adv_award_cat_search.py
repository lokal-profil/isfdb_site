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

class AdvancedAwardCatSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Award Category Search')
                PrintNavbar('adv_award_cat_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_award_cat_search()
                PrintTrailer('adv_award_cat_search', 0, 0)

        def print_award_cat_search(self):
                print '<h2>Award Category Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                for number in range(1, self.max_term + 1):
                        self.print_award_cat_selectors(number)
                self.print_award_cat_sort_by()
                self.print_submit_button('Award Category')

        def print_award_cat_selectors(self, number):
                print '<p id="award_cat_selectors_%d">' % number
                print '<select NAME="USE_%d" id="award_type_%d">' % (number, number)
                print '<option VALUE="award_cat_name">Award Category Name'
                print '<option VALUE="award_type_short_name">Parent Award Type Short Name'
                print '<option VALUE="award_type_full_name">Parent Award Type Full Name'
                print '<option VALUE="award_cat_order">Award Category Order'
                print '<option VALUE="note">Notes'
                print '<option VALUE="webpage">Webpage'
                print '</select>'

                self.print_operators('award_cat', number)

                print '<input id="award_catterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_award_cat_sort_by(self):
                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                print '<option SELECTED VALUE="award_cat_name">Award Category Name'
                print '<option VALUE="award_cat_order">Award Category Order'
                print '</select>'

        
if __name__ == '__main__':
        search = AdvancedAwardCatSearch()
        search.display_selection()
