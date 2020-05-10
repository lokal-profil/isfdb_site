#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2020   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from pubClass import *
from login import *
from SQLparsing import *

def displayError(value):
        print "<h3>%s.</h3>" % (value)
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Delete Publication")

	try:
		record = int(sys.argv[1])
                pub = pubs(db)
                pub.load(record)
                if not pub.pub_title:
                        raise
	except:
		PrintNavBar(0, 0)
		displayError('Publication does not exist')
	
	PrintNavBar('edit/deletepub.cgi', record)
	
	print '<b>Publication to Delete:</b> <i>%s</i>' % pub.pub_title
	print '<p>'
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitdelpub.cgi">'
	print '<p>'
        print '<b>Note to Moderator:</b><br>'
        print '<textarea tabindex="1" name="mod_note" rows="4" cols="60"></textarea>'
        print '<p>'
        print '<input name="pub_id" value="%d" type="HIDDEN">' % (record)
        print '<input type="SUBMIT" value="Delete">'
        pub.printModNoteRequired()
        print '</form>'

	PrintPostSearch(tableclose=False)
