#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2014   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

	try:
		user_id = int(sys.argv[1])
	except:
		PrintHeader("Bad Argument")
		PrintNavbar('usertag', 0, 0, 'usertag.cgi', 0)
		PrintTrailer('usertag', 0, 0)
		sys.exit(0)

	user_name = SQLgetUserName(user_id)
	label = "%s's Tags" % user_name

	PrintHeader(label)
	PrintNavbar('usertag', 0, 0, 'usertag.cgi', user_id)

	query = "select distinct tag_mapping.tag_id,count(tag_mapping.tag_id) as xx, tags.tag_name, tags.tag_status from tag_mapping,tags where tag_mapping.user_id=%d and tags.tag_id=tag_mapping.tag_id group by tag_mapping.tag_id order by xx desc" % user_id
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	first = 1
        bgcolor = 1
	while record:
                if first:
                        print "<table cellpadding=0 BGCOLOR=\"#FFFFFF\">"
                        print "<tr align=left bgcolor=\"#d6d6d6\">"
                        print "<td><b>Tag Name</b></td>"
                        print "<td><b>Count</b></td>"
                        print "<td><b>Private?</b></td>"
                        print "</tr>"
                        first = 0
                if bgcolor:
                        print '<tr align=left class="table1">'
                else:
                        print '<tr align=left class="table2">'
                print '<td>'
                print '<a href="http:/%s/tag.cgi?%s">%s</a>' % (HTFAKE, record[0][0], record[0][2])
                print '</td>'
                print '<td><a href="http:/%s/usertitles.cgi?%d+%d">%s</a></td>' % (HTFAKE, user_id, record[0][0], record[0][1])
                print '<td>'
                if record[0][3]:
                        print '<b>Private</b>'
                else:
                        print '&nbsp;'
                print '</td>'
                print '</tr>'
                bgcolor ^= 1
		record = result.fetch_row()

	print '</table>'
	print '<p><p>'

	PrintTrailer('usertag', user_id, user_id)
