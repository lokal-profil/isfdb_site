#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

def PrintPubRecord(count, record, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        url = 'http://www.sf-encyclopedia.com/entry/%s' % record[0]
        author_id = record[1]
        author_name = record[2]
        missing_id = record[3]

        print '<td>%d</td>' % (count)
        print '<td><a href="%s" target="_blank">%s</a></td>' % (url, url)
        print '<td><a href="http:/%s/ea.cgi?%s">%s</a></td>' % (HTFAKE, author_id, author_name)
        print '<td><a href="http:/%s/mod/resolve_missing_author_url.cgi?%s+%s">Click Once Resolved</a></td>' % (HTFAKE, script_type, missing_id)
	print '</tr>'

if __name__ == '__main__':

        try:
                script_type = int(sys.argv[1])
                if script_type == 1:
                        script_name = 'SFE3'
                else:
                        raise
        except:
                PrintPreMod('Invalid script type')
                PrintNavBar()
                sys.exit(0)
                
	##################################################################
	# Output the leading HTML stuff
	##################################################################

	PrintPreMod('ISFDB-%s Author Mismatches' % script_name)
        PrintNavBar()

        query = 'select m.url, m.author_id, a.author_canonical, m.missing_id from missing_author_urls as m, '
        query += 'authors as a where m.author_id=a.author_id and m.resolved=0 UNION '
        query += 'select url,"","",missing_id from missing_author_urls where resolved=0 and author_id IS NULL'

	db.query(query)
	result = db.store_result()
	num = result.num_rows()

        if num:
                PrintTableColumns(('#', 'URL', 'Author', 'Click Once Resolved'))
                record = result.fetch_row()
                bgcolor = 1
                count = 1
                while record:
                        PrintPubRecord(count, record[0], bgcolor)
                        record = result.fetch_row()
                        bgcolor ^= 1
                        count += 1

		print "</table>"
	else:
		print "<h2>No author with missing %s links found found</h2>" % script_name
