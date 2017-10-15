#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.5 $
#     Date: $Date: 2016/08/09 22:19:41 $


from SQLparsing import *
from common import *
from library import *


if __name__ == '__main__':

	try:
		author_id = int(sys.argv[1])
        	author_name = SQLloadAuthorData(author_id)[AUTHOR_CANONICAL]
	except:
		PrintHeader("Invalid or non-existing author ID")
		PrintNavbar('authortags', 0, 0, 'authortags.cgi', 0)
		PrintTrailer('authortags', 0, 0)
		sys.exit(0)

	label = "All Tags for %s" % author_name

	PrintHeader(label)
	PrintNavbar('authortags', 0, 0, 'authortags.cgi', author_id)

        # Determine the current user
        (userid, username, usertoken) = GetUserData()

        tags = SQLgetAuthorTags(author_id, int(userid))
        if not tags:
                print '<h3>No tags for author %s</h3>' % author_name
        else:
                print_string = ''
                count = 0
                for tag in tags:
                        if count:
                                print_string += ', '
                        print_string += '<a href="http:/%s/tag_author.cgi?%d+%d">%s</a> (%d)' % (HTFAKE, tag[0], author_id, tag[1], tag[2])
                        count += 1
                print print_string

        print '<p><b>Back to the Summary Bibliography page for %s</b>' % ISFDBLink('ea.cgi', author_id, author_name)

	PrintTrailer('authortags', author_id, author_id)
