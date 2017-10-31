#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
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
from login import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node


if __name__ == '__main__':

	PrintHeader("Recent Secondary Verifications")
	PrintNavbar('recent', 0, 0, 'recentver.cgi', 0)

	try:
		start = int(sys.argv[1])
	except:
		start = 0

        # First select 200 verification IDs -- needs to be done as a separate query since the SQL optimizer
        # in MySQL 5.0 is not always smart enough to use all available indices for multi-table queries
        query = "select verification.* from verification where ver_status = 1 order by ver_time desc limit %d,200" % start

	db.query(query)
	result0 = db.store_result()
	if result0.num_rows() == 0:
		print '<h3>No verifications present</h3>'
		PrintTrailer('recent', 0, 0)
		sys.exit(0)
        ver = result0.fetch_row()
        ver_set = []
        while ver:
                ver_set.append(ver[0])
                ver = result0.fetch_row()

        print '<table cellpadding=3 class="generic_table">'
        print '<tr class="generic_table_header">'
        print '<th>Publication Title</th>'
        print '<th>Reference</th>'
        print '<th>User</th>'
        print '<th>Time</th>'
        print '</tr>'

        color = 0
        for ver in ver_set:
                query = """select r.reference_label, mu.user_name, p.pub_title
                           from reference r, mw_user mu, pubs p
                           where r.reference_id=%d
                           and mu.user_id=%d
                           and p.pub_id=%d""" % (ver[VERIF_REF_ID], ver[VERIF_USER_ID], ver[VERIF_PUB_ID])
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                color = color ^ 1
                while record:
                        user_name = record[0][1]
                        pub_title = record[0][2]
                        if color:
                                print '<tr align=left class="table1">'
                        else:
                                print '<tr align=left class="table2">'
                        print '<td><a href="http:/%s/pl.cgi?%s">%s</a></td>' % (HTFAKE, ver[VERIF_PUB_ID], pub_title)
                        print '<td>%s</td>' % record[0][0]
                        print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name)
                        print '<td>%s</td>' % ver[VERIF_TIME]
                        print '</tr>'
                        record = result.fetch_row()

	print '</table>'
	print '<p> [<a href="http:/%s/recentver.cgi?%d">MORE</a>]' % (HTFAKE, start+200)

	PrintTrailer('recent', 0, 0)

