#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2016   Al von Ruff and Ahasuerus
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


def DisplayError(text):
        PrintHeader(text)
        PrintNavbar('usertitles', 0, 0, 'usertitles.cgi', 0)
        PrintTrailer('usertitles', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
		user_id = int(sys.argv[1])
		tag_id  = int(sys.argv[2])
	except:
                DisplayError('Bad Argument')

	try:
                start = int(sys.argv[3])
        except:
                start = 0

        tag = SQLGetTagById(tag_id)
        if not tag:
                DisplayError('Unknown Tag')

	user_name = SQLgetUserName(user_id)
        if user_name == 'UNKNOWN':
                DisplayError('Unknown User')

        current_user = User()
        current_user.load()
        current_user.load_moderator_flag()

        PrintHeader("%s's Tags" % user_name)
	PrintNavbar('usertitles', 0, 0, 'usertitles.cgi', 0)

        print """<h3>Titles marked by user <a href="http:/%s/usertag.cgi?%d">%s</a>
                 with tag <a href="http:/%s/tag.cgi?%d">%s</a></h3>
                 """% (HTFAKE, user_id, user_name, HTFAKE, tag_id, tag[1])
	titles = SQLgetTitlesForTagForUser(tag_id, user_id, start)
	PrintTitleTable(titles, 0, 100, current_user)

	if len(titles) > 100:
                print '<a href="http:/%s/usertitles.cgi?%d+%d+%d">Next page (%d - %d)</a>' % (HTFAKE, user_id, tag_id, start+100, start+101, start+200)

	PrintTrailer('usertitles', user_id, user_id)
