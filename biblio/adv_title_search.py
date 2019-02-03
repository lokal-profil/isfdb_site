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

class AdvancedTitleSearch(AdvancedSearch):
        def __init__(self):
                self.max_term = 5
        
        def display_selection(self):
                PrintHeader('ISFDB Advanced Title Search')
                PrintNavbar('adv_title_search', 0, 0, 0, 0)
                self.print_invisible_drop_down_values()
                self.print_full_header()
                self.print_title_search()
                PrintTrailer('adv_title_search', 0, 0)

        def print_title_search(self):
                print '<h2>Title Search</h2>'
                print '<p>'
                print '<ul>'
                print '<li> When specifying multiple authors and/or multiple tags, OR is supported but AND is not'
                print '</ul>'
                print '<p>'
                print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
                print '<p>'
                for number in range(1, self.max_term + 1):
                        self.print_title_selectors(number)
                self.print_title_sort_by()
                self.print_submit_button('Title')

        def print_title_selectors(self, number):
                print '<p id="title_selectors_%d">' % number
                print '<select NAME="USE_%d" id="title_%d">' % (number, number)
                print '<option SELECTED VALUE="title_title">Title'
                print '<option VALUE="title_trans_title">Transliterated Title'
                print '<option VALUE="author_canonical">Author\'s Name'
                print '<option VALUE="author_birthplace">Author\'s Birth Place'
                print '<option VALUE="author_birthdate">Author\'s Birthdate'
                print '<option VALUE="author_deathdate">Author\'s Deathdate'
                print '<option VALUE="author_webpage">Author\'s Webpage'
                print '<option VALUE="reviewee">Reviewed Author'
                print '<option VALUE="interviewee">Interviewed Author'
                print '<option VALUE="title_copyright">Title Year'
                print '<option VALUE="month">Title Month'
                print '<option VALUE="title_storylen">Length'
                print '<option VALUE="title_content">Content'
                print '<option VALUE="title_ttype">Title Type'
                print '<option VALUE="title_note">Notes'
                print '<option VALUE="title_synopsis">Synopsis'
                print '<option VALUE="series">Series'
                print '<option VALUE="title_language">Title Language (list)'
                print '<option VALUE="title_language_free">Title Language (free form)'
                print '<option VALUE="title_webpage">Title Webpage'
                print '<option VALUE="tag">Tag'
                print '<option VALUE="title_jvn">Juvenile'
                print '<option VALUE="title_nvz">Novelization'
                print '<option VALUE="title_non_genre">Non-Genre'
                print '<option VALUE="title_graphic">Graphic Format'
                print '</select>'

                self.print_operators('title', number)

                print '<input id="titleterm_%d" NAME="TERM_%d" SIZE="50">' % (number, number)
                if number == 1:
                        self.print_radio_selectors()
                print '<p>'

        def print_title_sort_by(self):
                print '<b>Sort Results By:</b>'
                print '<select NAME="ORDERBY">'
                print '<option SELECTED VALUE="title_title">Title'
                print '<option VALUE="title_copyright">Date'
                print '<option VALUE="title_ttype">Title Type'
                print '</select>'

        
if __name__ == '__main__':
        search = AdvancedTitleSearch()
        search.display_selection()
