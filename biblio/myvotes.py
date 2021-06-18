#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2021   Al von Ruff, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from isfdb import *
from common import *
from login import *
from SQLparsing import *


def PrintRecord(record, eccolor):

	if not record:
		return

	if eccolor:
		print '<tr align=left class="table1">'
	else:
		print '<tr align=left class="table2">'

	# Watch out for votes for no-longer-existing titles
	title_id = record[1]
	title = SQLloadTitle(title_id)
	if title:
		title_link = ISFDBLink('title.cgi', title_id, title[TITLE_TITLE])
		title_type = title[TITLE_TTYPE]
		title_year = title[TITLE_YEAR]
	else:
		title_link = "<i>Title Deleted (id %d)</i>" % (title_id)
		title_type = "-"
		title_year = "-"

	print '<td>%d</td>' % (record[3])
	print '<td>%s</td>' % (title_link)
	print '<td>%s</td>' % (title_type)
	print '<td>%s</td>' % (title_year)

	# Only display author(s) if there is a title
	print '<td>'
	if title:
		authors = SQLTitleBriefAuthorRecords(title_id)
		counter = 0
		for author in authors:
			if counter:
				print ' <b>and</b> '
			displayAuthorById(author[0], author[1])
			counter += 1
	else:
		print "-"

	print '</td>'

	print '</tr>'


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

	PrintHeader('My Votes')
	PrintNavbar('myvotes', 0, 0, 'myvotes.cgi', 0)

	(myID, username, usertoken) = GetUserData()
	myID = int(myID)
	if not myID:
		print '<h3>You have to be logged in to view your votes</h3>'
		PrintTrailer('votes', 0, 0)
		sys.exit(0)

	# Get the (next) set of votes.  We join over the titles table to avoid picking
	# up any votes for titles that have been deleted.
	if start:
		query = """select v.* from votes v, titles t
                        where v.user_id=%d
                        and t.title_id = v.title_id
                        order by v.rating desc, t.title_title
                        limit %d,50""" % (myID, start)
	else:
		query = """select v.* from votes v, titles t
                        where v.user_id=%d
                        and t.title_id = v.title_id
                        order by v.rating desc, t.title_title
                        limit 50""" % (myID)
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>No votes present</h3>'
		PrintTrailer('votes', 0, 0)
		sys.exit(0)

        print '<table class="vote_table">'
        print '<tr class="table1">'
        print '<th>Vote</th>'
        print '<th>Title</th>'
        print '<th>Type</th>'
        print '<th>Year</th>'
        print '<th>Author</th>'
        print '</tr>'

        record = result.fetch_row()
	color = 0
	while record:
		PrintRecord(record[0], color)
		color = color ^ 1
        	record = result.fetch_row()

	print '</table>'
	print '<p> [<a href="http:/%s/myvotes.cgi?%d">MORE</a>]' % (HTFAKE, start+50)

	PrintTrailer('votes', 0, 0)

