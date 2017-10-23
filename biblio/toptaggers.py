#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2017   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2017/10/23 22:52:07 $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node

#mysql> show columns from tag_mapping;
#+-----------+---------+------+-----+---------+----------------+
#| Field     | Type    | Null | Key | Default | Extra          |
#+-----------+---------+------+-----+---------+----------------+
#| tagmap_id | int(11) | NO   | PRI | NULL    | auto_increment |
#| tag_id    | int(11) | YES  | MUL | 0       |                |
#| title_id  | int(11) | YES  | MUL | 0       |                |
#| user_id   | int(11) | YES  | MUL | 0       |                |
#+-----------+---------+------+-----+---------+----------------+

if __name__ == '__main__':

	PrintHeader("Top Taggers")
	PrintNavbar('top', 0, 0, 'topmods.cgi', 0)

	print "<h2>Top ISFDB Taggers</h2>"
	print "<p>"

	print '<table cellpadding="3" bgcolor="#FFFFFF">'
	print '<tr class="table1">'
	print '<th>User</th>'
	print '<th>Tags</th>'
	print '<th>Last User Activity Date</th>'
	print '</tr>'

	query = "select distinct user_id,count(user_id) as xx from tag_mapping group by user_id order by xx desc"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	color = 0
	while record:
                user_id = record[0][0]
                count = record[0][1]
                # Only display users with 10+ tags
                if count < 10:
                        break
		query = "select user_name from mw_user where user_id=%d" % user_id
		db.query(query)
		res2 = db.store_result()
        	rec2 = res2.fetch_row()
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
		if rec2:
                        print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, rec2[0][0], rec2[0][0])
                else:
                        print '<td>&nbsp;</td>'
		print '<td>%d</td>' % count
		print '<td>%s</td>' % SQLLastUserActivity(user_id)
		print '</tr>'
		color = color ^ 1
        	record = result.fetch_row()
	print '</table><p>'

	PrintTrailer('top', 0, 0)

