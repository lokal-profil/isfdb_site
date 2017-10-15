#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/09/14 05:07:05 $

import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

def PrintPubRecord(count, pub_id, url, pub_title, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%d</td>' % (count)
        print '<td><a href="http:/%s/pl.cgi?%s">%s</a></td>' % (HTFAKE, pub_id, pub_title)
        print '<td>%s</td>' % (url)
        print '<td><a href="http:/%s/mod/resolve_bad_url.cgi?%s">Click Once Resolved</a></td>' % (HTFAKE, pub_id)
	print '</tr>'

if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################

	PrintPreMod('Publications with Suspect Images')
        PrintNavBar()

        query = 'select bad_images.pub_id,bad_images.image_url,pubs.pub_title from \
                bad_images,pubs where pubs.pub_id=bad_images.pub_id order by pubs.pub_title'

	db.query(query)
	result = db.store_result()
	num = result.num_rows()

        if num:
                PrintTableColumns(('#', 'Publication', 'Suspect URL', 'Click Once Resolved'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        pub_id = record[0][0]
                        url = record[0][1]
                        pub_title = record[0][2]
                        PrintPubRecord(count, pub_id, url, pub_title, bgcolor)
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1

		print "</table>"
	else:
		print "<h2>No publications with bad images found</h2>"
