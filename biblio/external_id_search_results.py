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
from biblio import *


##########################################################################################
# MAIN SECTION
##########################################################################################

if __name__ == '__main__':

        PrintHeader("ISFDB Publication Search by External ID")
        PrintNavbar('search', 0, 0, 0, 0)
	form = cgi.FieldStorage()
	try:
                id_types = SQLLoadIdentifierTypes()
                id_type = form['ID_TYPE'].value
                if int(id_type) not in id_types:
                        raise
		id_value = form['ID_VALUE'].value
                id_value = string.strip(id_value)
        except:
                print "<h2>No search value specified</h2>"
                PrintTrailer('search', '', 0)
                sys.exit(0)

        results = SQLFindPubByExternalID(id_type, id_value)
        matches = len(results)
        if matches == 1:
                plural = ''
        else:
                plural = 'es'
        print "<p><b>A search for '%s' found %d match%s" % (id_value, matches, plural)
        if results:
                PrintPubsTable(results, 'adv_search')

	print '<p>'
	PrintTrailer('search', 0, 0)

