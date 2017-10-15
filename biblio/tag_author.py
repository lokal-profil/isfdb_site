#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2016/08/09 22:19:41 $


from SQLparsing import *
from common import *
from library import *
from login import GetUserData


def DisplayError(text):
        PrintHeader(text)
        PrintNavbar('tag_author', 0, 0, 'tag_author.cgi', 0)
        PrintTrailer('tag_author', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
		tag_id = int(sys.argv[1])
                tag = SQLGetTagById(tag_id)
                if not tag:
                        raise
	except:
                DisplayError('Tag not found')

	try:
		author_id = int(sys.argv[2])
                author_data = SQLloadAuthorData(author_id)
                if not author_data:
                        raise
	except:
                DisplayError('Author not found')

        PrintHeader('Titles marked with tag %s for author %s' % (tag[TAG_NAME], author_data[AUTHOR_CANONICAL]))
	PrintNavbar('tag_author', 0, 0, 'tag_author.cgi', tag_id)

        print '<a class="inverted" href="http:/%s/tag.cgi?%d"><b>View all users and titles for this tag</b></a>' % (HTFAKE, tag_id)
	print '<h3>Titles by %s marked with tag: <i>%s</i></h3>' % (author_data[AUTHOR_CANONICAL], tag[TAG_NAME])
	print '<ul>'
        title_list = SQLgetTitlesForAuthorAndTag(tag_id, author_id)
        for title_record in title_list:
                print '<li>%s - %s ' % (convertYear(title_record[0][:4]), ISFDBLink('title.cgi', title_record[2], title_record[1]))
                authors = SQLTitleBriefAuthorRecords(title_record[2])
                need_and = 0
                for author in authors:
                        # Do not display the main author's name, only display collaborators
                        if author[0] == author_id:
                                continue
                        if need_and:
                                print '<b>and</b> %s ' % ISFDBLink('ea.cgi', author[0], author[1])
                        else:
                                print 'with %s ' % ISFDBLink('ea.cgi', author[0], author[1])
                                need_and = 1
                print '</li>'

	print '</ul>'

	PrintTrailer('tag', tag_id, tag_id)
