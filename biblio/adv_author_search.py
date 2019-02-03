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

class AdvancedAuthorSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Author Search')
                PrintNavbar('adv_author_search', 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                self.print_full_header()
                self.print_author_search()
                PrintTrailer('adv_author_search', 0, 0)

        def print_author_search(self):
                print '<h2>Author Search</h2>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'

                for number in range(1, self.max_term + 1):
                        self.print_author_selectors(number)
                self.print_author_sort_by()
                self.print_submit_button('Author')

        def print_author_selectors(self, number):
                print '<p id="author_selectors_%d">' % number
                print '<select NAME="USE_%d" id="author_%d">' % (number, number)
                print '<option SELECTED VALUE="author_canonical">Canonical Name'
                print '<option VALUE="author_trans_name">Transliterated Name'
                print '<option VALUE="author_lastname">Directory Entry'
                print '<option VALUE="author_legalname">Legal Name'
                print '<option VALUE="author_birthplace">Birth Place'
                print '<option VALUE="author_birthdate">Birthdate'
                print '<option VALUE="author_deathdate">Deathdate'
                print '<option VALUE="author_language">Working Language (list)'
                print '<option VALUE="author_language_free">Working Language (free form)'
                print '<option VALUE="author_trans_legalname">Transliterated Legal Name'
                print '<option VALUE="author_webpage">Webpage'
                print '<option VALUE="author_email">E-mail'
                print '<option VALUE="author_pseudos">Alternate Name'
                print '<option VALUE="author_note">Note'
                print '</select>'

                self.print_operators('author', number)

                print '<input id="authorterm_%d" NAME="TERM_%d" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_author_sort_by(self):
                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                print '<option SELECTED VALUE="author_canonical">Canonical Name'
                print '<option VALUE="author_lastname">Directory Entry'
                print '<option VALUE="author_legalname">Legal Name'
                print '<option VALUE="author_birthplace">Birth Place'
                print '<option VALUE="author_birthdate">Birthdate'
                print '<option VALUE="author_deathdate">Deathdate'
                print '</select>'

        
if __name__ == '__main__':
        search = AdvancedAuthorSearch()
        search.display_selection()
