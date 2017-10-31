#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import string
import os
from isfdb import *
from SQLparsing import *
from common import *


##########################################################################################
# MAIN SECTION
##########################################################################################

if __name__ == '__main__':

        PrintHeader("ISFDB User Search")
        PrintNavbar('search', 0, 0, 0, 0)
	form = cgi.FieldStorage()
	try:
		user_name = form['USER_NAME'].value
                user_name = string.strip(user_name)
        except:
                print "<h2>No user name specified</h2>"
                PrintTrailer('search', '', 0)
                sys.exit(0)

        user_id = SQLgetSubmitterID(user_name)
        if not user_id:
                print "<h2>Specified user name does not exist</h2>"
                PrintTrailer('search', '', 0)
                sys.exit(0)
        moderator = 'No'
        if SQLisUserModerator(user_id):
                moderator = 'Yes'
        print '<table>'
        print '<tr class="table1">'
        print '<th>User Name</th>'
        print '<th>Moderator</th>'
        print '<th>Last User Activity Date</th>'
        print '</tr>'
        print '<tr class="table2">'
        print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name)
        print '<td>%s</td>' % moderator
        print '<td>%s</td>' % SQLLastUserActivity(user_id)
        print '</tr>'
        print '</table>'

	print '<p>'
	PrintTrailer('search', 0, 0)

