#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2017  Bill Longley, Ahasuerus and Dirk Stoeker
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
from login import *


def PubAuthors(pub_id):
	retval = ''
	authors = SQLPubBriefAuthorRecords(pub_id)
	counter = 0
	for author in authors:
		if counter:
			retval += ", "
		retval += ISFDBLink('ea.cgi', author[0], author[1])
		counter += 1
	return retval

def PubArtists(pub_id):
        list_of_pub_ids = []
        list_of_pub_ids.append(str(pub_id))
        cover_artists = SQLGetCoverAuthorsForPubs(list_of_pub_ids)
        return cover_artists

def PrintPubRecord(record, bgcolor):
        pub_id = record[0]
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%s</td>' % record[2]
        print '<td>%s</td>' % record[3]
        print '<td><a href="http:/%s/pl.cgi?%s">%s</a></td>' % (HTFAKE, pub_id, record[1])
	output = "" 
        if record[2] in ('MAGAZINE', 'ANTHOLOGY', 'FANZINE', 'NONFICTION'):
                output = "Ed. "
        output += PubAuthors(pub_id)
        print '<td>%s</td>' % output

        if record[4]:
                print '<td>Transient</td>'
        else:
                print '<td>&nbsp;</td>'

        cover_artists = PubArtists(pub_id)
        print '<td>'
        if pub_id in cover_artists:
                displayAuthorList(cover_artists[pub_id])
        else:
                '&nbsp;'
        print '</td>'

        if record[5]:
                print '<td>%s</td>' % CoverInfo(record[5])
        else:
                print '<td>&nbsp;</td>'

	print "</tr>"

def PrintTableColumns():
	print '<table class="userverifications">'
	print '<tr class="table2">'
	print '<th>Type</th>'
	print '<th>Ver. Date</th>'
	print '<th>Publication</th>'
	print '<th>Author(s) or Editor(s)</th>'
	print '<th>Transient?</th>'
	print '<th>Artist(s)</th>'
	print '<th>Cover</th>'
 	print '</tr>'

if __name__ == '__main__':

        try:
                start = int(sys.argv[1])
        except:
                start = 0

	PrintHeader("My Primary Verifications")
	PrintNavbar('userver', 0, 0, 'userver.cgi', 0)

        user = User()
        user.load()

	query = """select p.pub_id, p.pub_title, p.pub_ctype, 
                date_format(pv.ver_time,'%%Y-%%m-%%d') date,
                pv.ver_transient, p.pub_frontimage
                from pubs p, primary_verifications pv
                where pv.pub_id = p.pub_id and pv.user_id=%d
                order by date desc, pv.verification_id desc limit %d,%d
                """ % (int(user.id), start, 1000)

	db.query(query)
	result = db.store_result()
	num = result.num_rows()

	if num > 0:
                last = num
                if last > 1000:
                        last = 1000
		print "<h3>Displaying primary verifications %d-%d:</h3>" % (start+1, start+last)
		record = result.fetch_row()
		bgcolor = 1
		PrintTableColumns()
		while record:
			PrintPubRecord(record[0], bgcolor)
			bgcolor ^= 1
			record = result.fetch_row()
		print "</table>"
		if num > 999:
                        print '[<a href="http:/%s/userver.cgi?%d">%d-%d</a>]' % (HTFAKE, start+1000, start+1001, start+2000)
	else:
		print "<h2>No primary verifications found</h2>"

	PrintTrailer('userver', 0, 0)

