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

class AdvancedIDSearch(AdvancedSearch):
        
        def display_selection(self):
                PrintHeader('Publication Search by Identifier')
                PrintNavbar('adv_id_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_identifier_search()
                PrintTrailer('adv_id_search', 0, 0)

        def print_identifier_search(self):
                print '<h2>Publication Search by External Identifier</h2>'
                print '<form METHOD="GET" action="http:/%s/external_id_search_results.cgi">' % (HTFAKE)
                print '<p>'
                id_types = SQLLoadIdentifierTypes()
                print '<select NAME="ID_TYPE">'
                for type_number in sorted(id_types, key = id_types.get):
                        type_name = id_types[type_number][0]
                        print '<option VALUE="%d">%s</option>' % (type_number, type_name)
                print '</select>'

                print '<select NAME="OPERATOR">'
                print '<option SELECTED VALUE="exact">is exactly'
                print '<option VALUE="contains">contains'
                print '<option VALUE="notcontains">does not contain'
                print '<option VALUE="starts_with">starts with'
                print '<option VALUE="not_starts_with">does not start with'
                print '<option VALUE="ends_with">ends with'
                print '<option VALUE="not_ends_with">does not end with'
                print '</select>'

                print '<input NAME="ID_VALUE" SIZE="50">'
                print '<p>'

                print '<input TYPE="SUBMIT" VALUE="Submit Query">'
                print '</form>'

        
if __name__ == '__main__':
        search = AdvancedIDSearch()
        search.display_selection()
