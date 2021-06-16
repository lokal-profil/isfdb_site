#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2021   Al von Ruff and Ahasuerus
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

        user_id = SESSION.Parameter(0, 'int')
        tag_id  = SESSION.Parameter(1, 'int')
        start = SESSION.Parameter(2, 'int', 0)
        tag = SQLGetTagById(tag_id)
        if not tag:
                SESSION.DisplayError('Tag Does Not Exist')
	user_name = SQLgetUserName(user_id)
        if user_name == 'UNKNOWN':
                SESSION.DisplayError('Unknown User')

        current_user = User()
        current_user.load()
        current_user.load_moderator_flag()

        PrintHeader("%s's Tags" % user_name)
	PrintNavbar('usertitles', 0, 0, 'usertitles.cgi', 0)

        print """<h3>Titles marked by user <a href="http:/%s/usertag.cgi?%d">%s</a>
                 with tag <a href="http:/%s/tag.cgi?%d">%s</a></h3>
                 """% (HTFAKE, user_id, user_name, HTFAKE, tag_id, tag[TAG_NAME])
	titles = SQLgetTitlesForTagForUser(tag_id, user_id, start)
	PrintTitleTable(titles, 0, 100, current_user)

	if len(titles) > 100:
                print '<a href="http:/%s/usertitles.cgi?%d+%d+%d">Next page (%d - %d)</a>' % (HTFAKE, user_id, tag_id, start+100, start+101, start+200)

	PrintTrailer('usertitles', user_id, user_id)
