#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import os
import string
from SQLparsing import *
from biblio import *
from library import ISFDBText


def PrintPublisherTableColumns():
	print '<table class="generic_table">'
	print '<tr class="generic_table_header">'
	print '<td><b>Publisher</b></td>'
 	print '</tr>'
 	return

def PrintPublisherRecord(publisher_id, publisher_name, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'
        print '<td>%s</td>' % ISFDBLink('publisher.cgi', publisher_id, publisher_name)
        print '</tr>'

def PrintMagazineTableColumns():
	print '<table class="generic_table">'
	print '<tr class="generic_table_header">'
	print '<th>Magazine</th>'
	print '<th>Parent Series</th>'
 	print '</tr>'
 	return

def PrintMagazineRecord(title_title, series_id, parent_id, series_title, bgcolor):
        if bgcolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

        print '<td>%s' % ISFDBLink('pe.cgi', series_id, title)
        if title_title != series_title:
                print '*'
        print ' %s</td>' % ISFDBLinkNoName('seriesgrid.cgi', series_id, '(issue grid)')
	if parent_id:
		parent_title = SQLgetSeriesName(int(parent_id))
        	print '<td>'
        	print ISFDBLink('pe.cgi', parent_id, parent_title)
                print ' %s</td>' % ISFDBLinkNoName('seriesgrid.cgi', parent_id, '(issue grid)')
	else:
		print '<td>-</td>'
        print '</tr>'


if __name__ == '__main__':

        dir_type = SESSION.Parameter(0, 'str', None, ('author','publisher','magazine'))

        title = "%s Directory" % dir_type.title()
        if len(SESSION.parameters) == 1:
                section= ''
	else:
                section = SESSION.Parameter(1, 'str')
                title += ": %s" % ISFDBText(section.title())
        if dir_type == 'author' and section:
                SESSION.DisplayError('Second Parameter Not Allowed for Author Directory')

	PrintHeader(title)
	PrintNavbar('directory', 0, 0, 'directory.cgi', dir_type)

        if dir_type == 'publisher':
                records_map = SQLGetPublisherDirectory()
        elif dir_type == 'magazine':
                records_map = SQLGetMagazineDirectory()
        else:
                records_map = SQLGetAuthorDirectory()
        
        first_characters = string.ascii_lowercase + "'"
        if dir_type != 'author':
                # The Author Directory doesn't support asterisks in author names because
                # it uses the Advanced Author Search logic, which treats asterisks as wildcards
                first_characters += "*"
        second_characters = first_characters + "." + "/"
        
	if section == '':
                if dir_type == 'publisher':
                        print """Also see the ISFDB Wiki
                                <a href="%s://%s/index.php/Category:Publishers">category</a> for publishers""" % (PROTOCOL, WIKILOC)
                elif dir_type == 'magazine':
                        print """Also see the ISFDB Wiki pages for
                                <a href="%s://%s/index.php/Magazines">magazines</a>
                                and <a href="%s://%s/index.php/Fanzines">fanzines</a>""" % (PROTOCOL, WIKILOC, PROTOCOL, WIKILOC)
		if dir_type != 'magazine':
                        print '<h2>Directory of %s names starting with:</h2><p>' % (dir_type)
                else:
                        print '<h2>Directory of magazine and fanzine names starting with:</h2><p>'
                print '<table class="authordirectory">'
		for x in first_characters:
			print '<tr>'
			for y in second_characters:
                                key = x + y
				if key in records_map:
                                        if dir_type == 'author':
                                                output = '<td>%s' % AdvSearchLink((('USE_1', 'author_lastname'),
                                                                                   ('OPERATOR_1', 'starts_with'),
                                                                                   ('TERM_1', key),
                                                                                   ('ORDERBY', 'author_lastname'),
                                                                                   ('TYPE', 'Author'),
                                                                                   ('C', 'AND')))
                                                output += '<b>%s%s</b></a></td>' % (x.upper(), y)
                                                print output
                                        else:
                                                print '<td>%s</td>' % ISFDBLinkNoName('directory.cgi', '%s+%s%s' % (dir_type, x, y), '<b>%s%s</b>' % (x.upper(), y))
				else:
					print '<td class="authordirectorynolink">%s%s</td>' % (x.upper(), y)
			print '</tr>'
		print '</table>'
		print '<p>'

        else:
                if len(section) == 1:
                        print '<h3>ERROR: Single character directories are not allowed due to excessive load on the server</h3>'
                        PrintTrailer('directory', 0, 0)
                        sys.exit(0)
                # Display a link to the previous sub-directory if available
                for char in reversed(range(0, second_characters.find(section[1]))):
                        key = section[0] + second_characters[char]
                        if key in records_map:
                                first = key[0]
                                second = key[1]
                                print '<small>%s</small>' % ISFDBLinkNoName('directory.cgi',
                                                                            '%s+%s%s' % (dir_type, first, second),
                                                                            '<b>Back to %s%s</b>' % (first.upper(), second))
                                break

                print ISFDBLink('directory.cgi', dir_type, '<b>Up to %s Directory</b>' % dir_type.title())

                # Display a link to the next sub-directory if available
                for char in range(second_characters.find(section[1])+1, len(second_characters)):
                        key = section[0] + second_characters[char]
                        if key in records_map:
                                first = key[0]
                                second = key[1]
                                print '<small>%s</small>' % ISFDBLinkNoName('directory.cgi',
                                                                            '%s+%s%s' % (dir_type, first, second),
                                                                            '<b>Forward to %s%s</b>' % (first.upper(), second))
                                break

                search_string = db.escape_string(section[0] + section[1] + '%')

                # Magazine Directory
                if dir_type == 'magazine':
                        (results, count) = SQLFindMagazine(search_string, 1)
                        print '<br><br>'
                        if count:
                                print """<b>Note: Matching magazines whose series titles do not match the
                                entered value have asterisks next to their titles.<br><br>
                                Number of %s names starting with "%s": %d </b>""" % (dir_type, ISFDBText(section), count)
                                PrintMagazineTableColumns()
                                bgcolor = 1
                                for title in sorted(results.keys(), key=lambda x: x.lower()):
                                        for series_id in results[title]:
                                                parent_id = results[title][series_id][0]
                                                series_name = results[title][series_id][1]
                                                PrintMagazineRecord(title, series_id, parent_id, series_name, bgcolor)
                                                bgcolor ^= 1
                                print '</table>'
                        else:
                                print '<b>No %s names found starting with: %s</b>' % (dir_type, ISFDBText(section))
                        PrintTrailer('directory', 0, 0)
                        sys.exit(0)

                # Publisher directory
                query = """select distinct p.* from publishers p
                        where p.publisher_name like _utf8"%s"
                        COLLATE 'utf8_general_ci'
                        union
                        select distinct p.* from publishers p, trans_publisher tp
                        where p.publisher_id = tp.publisher_id
                        and tp.trans_publisher_name like _utf8"%s"
                        COLLATE 'utf8_general_ci'
                        order by publisher_name""" % (search_string, search_string)
		db.query(query)
		result = db.store_result()
		number_of_records = result.num_rows()
		if number_of_records:
                        print '<h3>Number of publisher names starting with "%s": %d </h3>' % (section, number_of_records)
			bgcolor = 1
                        PrintPublisherTableColumns()
                        record = result.fetch_row()
                        while record:
                                record_name = record[0][1]
                                record_id = record[0][0]
                                PrintPublisherRecord(record_id, record_name, bgcolor)
				bgcolor ^= 1
                                record = result.fetch_row()
                        print '</table><p>'
		else:
			print '<h3>No %s names found starting with: %s</h3>' % (dir_type, ISFDBText(section))

	PrintTrailer('directory', 0, 0)
