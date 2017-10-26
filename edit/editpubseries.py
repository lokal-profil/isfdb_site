#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.12 $
#     Date: $Date: 2016/04/30 04:43:37 $


import cgi
import sys
import MySQLdb
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import *
from isfdb import *
from SQLparsing import *


if __name__ == '__main__':

	try:
		pub_series_id = int(sys.argv[1])
                record = SQLGetPubSeries(pub_series_id)
		if not record:
			raise
	except:
		PrintPreSearch("Publication Series Editor")
		PrintNavBar("edit/editpubseries.cgi", 0)
		print "<h3>Missing or invalid publication series ID</h3>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)
		
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Publication Series Editor")
	PrintNavBar("edit/editpubseries.cgi", sys.argv[1])

        help = HelpPubSeries()

        printHelpBox('publication series', 'PublicationSeries')

	print '<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitpubseries.cgi" onsubmit="return validatePubSeriesForm()">'

	print '<table border="0">'
	print '<tbody id="tagBody">'
	printfield("Pub. Series Name",  "pub_series_name",       help, record[PUB_SERIES_NAME])
	
        trans_pub_series_names = SQLloadTransPubSeriesNames(record[PUB_SERIES_ID])
        printmultiple(trans_pub_series_names, "Transliterated Name", "trans_pub_series_names",
                      "AddTransName", "AddMultipleField", help,
                      "'%s', '%s', '%s'" % ('AddTransName', 'Transliterated Name', 'trans_pub_series_names'))

	webpages = SQLloadPubSeriesWebpages(pub_series_id)
        printWebPages(webpages, 'pub_series', help)
	
        printtextarea('Note', 'pub_series_note', help, SQLgetNotes(record[PUB_SERIES_NOTE]))

        printtextarea('Note to Moderator', 'mod_note', help, '')

	print '</table>'

	print '<p>'
	print '<input NAME="pub_series_id" VALUE="%d" TYPE="HIDDEN">' % pub_series_id
	print '<input TYPE="SUBMIT" VALUE="Submit Data" tabindex="1">'
	print '</form>'
	print '<p>'

	PrintPostSearch(0, 0, 0, 0, 0)
