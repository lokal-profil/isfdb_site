#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2019   Al von Ruff, Ahasuerus and Bill Longley
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

class AdvancedPubSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Publication Search')
                PrintNavbar('adv_pub_search', 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                self.print_full_header()
                self.print_pub_search()
                PrintTrailer('adv_pub_search', 0, 0)

        def print_pub_search(self):
                print '<h2>Publication Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                print '<ul>'
                print '<li> ISBN searches ignore dashes and search for both ISBN-10 and ISBN-13'
                print '</ul>'
                for number in range(1, self.max_term + 1):
                        self.print_pub_selectors(number)
                self.print_pub_sort_by()
                self.print_submit_button('Publication')

        def print_pub_selectors(self, number):
                print '<p id="pub_selectors_%d">' % number
                print '<select NAME="USE_%d" id="pub_%d">' % (number, number)
                print '<option SELECTED VALUE="pub_title">Title'
                print '<option VALUE="pub_trans_title">Transliterated Title'
                print '<option VALUE="pub_ctype">Publication Type'
                print '<option VALUE="author_canonical">Author\'s Name'
                print '<option VALUE="author_birthplace">Author\'s Birth Place'
                print '<option VALUE="author_birthdate">Author\'s Birthdate'
                print '<option VALUE="author_deathdate">Author\'s Deathdate'
                print '<option VALUE="author_webpage">Author\'s Webpage'
                print '<option VALUE="pub_year">Publication Year'
                print '<option VALUE="pub_month">Publication Month'
                print '<option VALUE="pub_publisher">Publisher'
                print '<option VALUE="trans_publisher">Transliterated Publisher'
                print '<option VALUE="pub_series">Publication Series'
                print '<option VALUE="trans_pub_series">Transliterated Publication Series'
                print '<option VALUE="pub_isbn">ISBN'
                print '<option VALUE="pub_catalog">Catalog ID'
                print '<option VALUE="pub_price">Price'
                print '<option VALUE="pub_pages">Page Count'
                print '<option VALUE="pub_coverart">Cover Artist'
                print '<option VALUE="pub_ptype">Format'
                print '<option VALUE="pub_verifier">Primary Verifier'
                print '<option VALUE="pub_note">Notes'
                print '<option VALUE="pub_frontimage">Image URL'
                print '</select>'

                self.print_operators('pub', number)

                print '<input id="pubterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_pub_sort_by(self):
                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                print '<option SELECTED VALUE="pub_title">Title'
                print '<option VALUE="pub_ctype">Publication Type'
                print '<option VALUE="pub_year">Date'
                print '<option VALUE="pub_isbn">ISBN'
                print '<option VALUE="pub_catalog">Catalog ID'
                print '<option VALUE="pub_price">Price'
                print '<option VALUE="pub_pages">Page Count'
                print '<option VALUE="pub_ptype">Format'
                print '<option VALUE="pub_frontimage">Image URL'
                print '</select>'

        
if __name__ == '__main__':
        search = AdvancedPubSearch()
        search.display_selection()
