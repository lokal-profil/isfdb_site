#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2015   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.8 $
#     Date: $Date: 2015/12/17 02:02:43 $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

	PrintHeader("My Translation Preferences")
	PrintNavbar('mylanguages', 0, 0, 'mylanguages.cgi', 0)

        user = User()
        user.load()

	if not user.id:
                print 'You must be logged in to modify your translation preferences'
                sys.exit(0)
        	PrintTrailer('mylanguages', 0, 0)

	# Get a list of currently defined languages
        query = "select lang_id, lang_name from languages order by lang_name"
	db.query(query)
	result = db.store_result()
	row = result.fetch_row()
	langs = []
	while row:
                langs.append(row[0])
		row = result.fetch_row()
	
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/submitmylanguages.cgi">'
        print '<ul>'
        for lang in langs:
                if lang[0] in user.languages:
                        checked = 'checked'
                else:
                        checked = ''
        	print '<li><input type="checkbox" name="lang_choice.%s" value="on" %s>%s</li>' % (lang[0], checked, lang[1])
        	print '<input name="lang_id.%d" value="%s" type="HIDDEN">' % (lang[0], lang[1])

        print '</ul>'
	print '<input type="SUBMIT" value="Update Translation Preferences">'
        print '</form>'

	PrintTrailer('mylanguages', 0, 0)

