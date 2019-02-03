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

class AdvancedUserSearch():
        
        def display_selection(self):
                PrintHeader('User Search')
                PrintNavbar('adv_user_search', 0, 0, 0, 0)
                self.print_user_search()
                PrintTrailer('adv_user_search', 0, 0)

        def print_user_search(self):
                print '<form METHOD="GET" action="http:/%s/user_search_results.cgi">' % HTFAKE
                print '<p>'
                print 'User Name: <input NAME="USER_NAME" SIZE="50">'
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Submit Query">'
                print '</form>'

        
if __name__ == '__main__':
        search = AdvancedUserSearch()
        search.display_selection()
