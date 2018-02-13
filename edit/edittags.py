#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2018   Al von Ruff and Ahasuerus
#	 ALL RIGHTS RESERVED
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
from isfdblib_help import *
from isfdblib_print import *


if __name__ == '__main__':

	try:
		title_id = int(sys.argv[1])
		title_title = SQLgetTitle(title_id)
		if not title_title:
                        raise
	except:
                PrintPreSearch("Tag Editor")
                PrintNavBar("edit/edittags.cgi", 0)
                print "<h3>Missing or invalid title</h3>"
                PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	try:
		showall = int(sys.argv[2])
	except:
		showall = 0

	PrintPreSearch("Tag Editor")
	PrintNavBar("edit/edittags.cgi", title_id)

	print '<div id="HelpBox">'
	print "<b>Help on editing tags: </b>"
	print '<a href="http://%s/index.php/Help:Screen:TagEditor">Help:Screen:TagEditor</a><p>' % (WIKILOC)
	print '</div>'

	(user_id, username, usertoken) = GetUserData()

        help = HelpTag()
	print "<form id='data' METHOD=\"POST\" ACTION=\"/cgi-bin/edit/submittags.cgi\">"

	print '<table border="0">'
	print '<tbody id="tagBody">'

        # Retrieve the tags specific to the currently logged in user
	tags = SQLgetUserTags(title_id, user_id)
	
        printmultiple(tags, "Tag", "tag_name", "AddTag", help)

	print "</tbody>"
	print "</table>"

	print "<p>"
	print "<hr>"
	print "<p>"
	print '<input NAME="title_id" VALUE="%d" TYPE="HIDDEN">' % title_id
	print '<input NAME="user_id" VALUE="%d" TYPE="HIDDEN">' % int(user_id)
	print '<input TYPE="SUBMIT" VALUE="Submit Data">'
	print "</form>"
	print "<p>"
	print "<hr>"

	print "<b>Existing Tags Associated With This Work:</b>"
	tags = SQLgetTitleTags(title_id)
	if tags == []:
		print 'None'
	else:
		first = 1
		for tag in tags:
			if first:
				print '<a href="http:/%s/tag.cgi?%d">%s</a>' % (HTFAKE, tag[0], tag[1])
				first = 0
			else:
				print ', <a href="http:/%s/tag.cgi?%d">%s</a>' % (HTFAKE, tag[0], tag[1])
	print '<p>'


	if showall:
		print "<b>All Tags in the Database:</b>"
	else:
		print "<b>Most Popular Tags in the Database:</b>"

        # 2-step process to retrieve tag-specific data; necessitated by MySQL performance issues with certain count(distinct) queries
        # Retrieve the most popular tags and how many times they have been used
	query = "select distinct tag_id,count(tag_id) from tag_mapping group by tag_id order by count(tag_id) desc"
	if not showall:
                query += " limit 1000"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	tag_map = []
	tag_ids = []
	while record:
        	tag_map.append(record[0])
        	tag_ids.append(str(record[0][0]))
		record = result.fetch_row()

        # Get the tag names for the tags that were retrieved above and put them in a dictionary
	query = "select tag_id,tag_name from tags where tag_id in (%s)" % (db.escape_string((",".join(tag_ids))))
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	tag_names = {}
	while record:
        	tag_names[record[0][0]] = record[0][1]
		record = result.fetch_row()

	first = 1
	output = ''
	for tag in tag_map:
                tag_id = tag[0]
                tag_count = tag[1]
                tag_name = tag_names[tag_id]
                if first:
                        first = 0
                else:
                        output += ", "
                output += '<a href="http:/%s/tag.cgi?%d">%s</a> (%d)' % (HTFAKE, tag_id, tag_name, tag_count)
        print output
	
	if not showall:
		print '<br><p><a href="http:/%s/edit/edittags.cgi?%d+1"><b>Show All Tags</b></a>' % (HTFAKE, title_id)

	PrintPostSearch(tableclose=False)
