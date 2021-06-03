#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 351 $
#     Date: $Date: 2021-06-03 18:49:17 -0500 (Sat, 16 Feb 2019) $


from SQLparsing import *
from common import *
from library import *
from login import *

if __name__ == '__main__':

        try:
                publisher_id = int(SESSION.arguments[0])
        except:
                SESSION.DisplayError('Invalid Argument')

        try:
                publisher_name = SQLgetPublisherName(publisher_id)
                if not publisher_name:
                        raise
        except:
                SESSION.DisplayError('Specified Publisher Does Not Exist')

        try:
                sort_by = SESSION.arguments[1]
                if sort_by not in ('name', 'count'):
                        raise
        except:
                sort_by = 'count'

        PrintHeader('Authors for Publisher %s, Sorted by %s' % (publisher_name, sort_by.capitalize()))
	PrintNavbar('publisher_authors', publisher_id, publisher_id, 'publisher_authors.cgi', 0)

	if sort_by == 'name':
                print ISFDBLink('publisher_authors.cgi', '%s+count' % publisher_id, 'Sort by Publication Count')
	else:
                print ISFDBLink('publisher_authors.cgi', '%s+name' % publisher_id, 'Sort by Author Name')

        print ' &#8226; '
        print ISFDBLink('publisher.cgi', publisher_id, 'Return to the publisher page')
        print """<p>Note that the statistics below count the number of publications associated
                with publication-level authors and editors. They do not count the authors of
                individual titles (stories, poems, etc.) contained in publications. Each edition
                of a book increments its author's count. Different forms of an author's name, e.g.
                'Mary Shelley' vs. 'Mary W. Shelley', are counted separately."""

	authors = SQLGetAuthorsForPublisher(publisher_id, sort_by)
	table = ISFDBTable()
	table.headers.extend(['Author/Editor', 'Publication Count'])
	for author in authors:
                author_id = author[0]
                author_name = author[1]
                author_count = author[2]
                table.rows.append((ISFDBLink('ea.cgi', author_id, author_name), author_count))
        table.PrintTable()

	PrintTrailer('publisher_authors', publisher_id, publisher_id)
