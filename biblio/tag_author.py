#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
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
from login import GetUserData


if __name__ == '__main__':

        tag_id = SESSION.Parameter(0, 'int')
        tag = SQLGetTagById(tag_id)
        if not tag:
                SESSION.DisplayError('Tag Does Not Exist')

        author_id = SESSION.Parameter(1, 'int')
        author_data = SQLloadAuthorData(author_id)
        if not author_data:
                SESSION.DisplayError('Author Does Not Exist')

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
