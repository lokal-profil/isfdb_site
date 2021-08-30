#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2021   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from isfdb import *
from SQLparsing import *
from common import *
from advSearchClass import AdvancedSearch

class AdvancedNotesSearch(AdvancedSearch):
        
        def display_selection(self):
                PrintHeader('Notes Search')
                PrintNavbar('adv_notes_search', 0, 0, 0, 0)
                self.print_full_header()
                self.print_notes_search()
                PrintTrailer('adv_notes_search', 0, 0)

        def print_notes_search(self):
                print '<h2>Notes Search</h2>'
                print '<form METHOD="GET" action="%s:/%s/note_search_results.cgi">' % (PROTOCOL, HTFAKE)
                print '<p>'
                print 'Note/Synopsis '
                print '<select NAME="OPERATOR">'
                print '<option SELECTED VALUE="contains">contains'
                print '<option VALUE="exact">is exactly'
                print '<option VALUE="starts_with">starts with'
                print '<option VALUE="ends_with">ends with'
                print '</select>'
                print '<input NAME="NOTE_VALUE" SIZE="50">'
                print '<p>'
                print '<input TYPE="SUBMIT" VALUE="Submit Query">'
                print '</form>'

        
if __name__ == '__main__':
        search = AdvancedNotesSearch()
        search.display_selection()
