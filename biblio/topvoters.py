#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2015   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2015/10/11 02:43:23 $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node

#mysql> show columns from votes;
#+----------+---------+------+-----+---------+----------------+
#| Field    | Type    | Null | Key | Default | Extra          |
#+----------+---------+------+-----+---------+----------------+
#| vote_id  | int(11) | NO   | PRI | NULL    | auto_increment |
#| title_id | int(11) | YES  | MUL | NULL    |                |
#| user_id  | int(11) | YES  | MUL | NULL    |                |
#| rating   | int(11) | YES  |     | NULL    |                |
#+----------+---------+------+-----+---------+----------------+

if __name__ == '__main__':

	PrintHeader("Top Voters")
	PrintNavbar('top', 0, 0, 'topmods.cgi', 0)

	print "<h2>Top ISFDB Voters</h2>"
	print "<p>"

	print '<table cellpadding="3" bgcolor="#FFFFFF">'

	query = "select distinct user_id,count(user_id) as xx from votes group by user_id order by xx desc"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	color = 0
	while record:
                # Only display users with 10+ votes
                if record[0][1] <10:
                        break
		query = "select user_name from mw_user where user_id=%d" % (record[0][0])
		db.query(query)
		res2 = db.store_result()
        	rec2 = res2.fetch_row()
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
		print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, rec2[0][0], rec2[0][0])
		print '<td>%d</td>' % (record[0][1])
		print '</tr>'
		color = color ^ 1
        	record = result.fetch_row()
	print '</table><p>'

	PrintTrailer('top', 0, 0)

