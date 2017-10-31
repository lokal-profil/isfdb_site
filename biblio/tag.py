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
        PrintNavbar('tag', 0, 0, 'tag.cgi', 0)
        PrintTrailer('tag', 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	try:
		tag_id = int(sys.argv[1])
	except:
                DisplayError('Bad Argument')

	try:
		start = int(sys.argv[2])
	except:
                start = 0

	tag = SQLGetTagById(tag_id)
	if not tag:
                DisplayError('Bad Tag')

        PrintHeader('Titles marked with tag %s' % (tag[TAG_NAME]))
	PrintNavbar('tag', 0, 0, 'tag.cgi', tag_id)

        current_user = User()
        current_user.load()
        current_user.load_moderator_flag()

        if tag[TAG_STATUS]:
                status = 'Private'
        else:
                status = 'Public'
        print "This tag is currently marked <b>%s</b>" % status
        if current_user.moderator:
                if status == 'Private':
                        new_status = 'Public'
                else:
                        new_status = 'Private'
                print '<form METHOD="POST" ACTION="/cgi-bin/mod/change_tag_status.cgi">'
                print '<div>'
                print '<input name="new_status" value="%s" type="HIDDEN">' % new_status
                print '<input name="tag_id" value="%s" type="HIDDEN">' % tag[TAG_ID]
                print '<input name="tag_name" value="%s" type="HIDDEN">' % tag[TAG_NAME]
                print '<input type="SUBMIT" value="Change the status to %s">' % new_status
                print '</div>'
                print '</form>'

	##################################################
	#          U S E R S
	##################################################
	print '<h3>Users of this Tag: <i>%s</i></h3>' % tag[TAG_NAME]
	tag_users = SQLgetUsersForTag(tag_id)
	need_comma = 0
	for tag_user in tag_users:
                output = ''
		if need_comma:
			output += ', '
		else:
			need_comma = 1
                output += '<a href="http:/%s/usertag.cgi?%d">%s</a>' % (HTFAKE, tag_user[0], tag_user[2])
                output += ' (<a href="http:/%s/usertitles.cgi?%d+%d">%d</a>)' % (HTFAKE, tag_user[0], tag_id, tag_user[1])
		print output

	##################################################
	#          T I T L E S
	##################################################
	print '<h3>Titles Marked With Tag <i>%s</i></h3>' % tag[TAG_NAME]
	titles = SQLgetTitlesForTag(tag_id, start)
	PrintTitleTable(titles, 0, 100, current_user)

	if len(titles) > 100:
                print '<a href="http:/%s/tag.cgi?%d+%d">Next page (%d - %d)</a>' % (HTFAKE, tag_id, start+100, start+101, start+200)

	PrintTrailer('tag', tag_id, tag_id)
