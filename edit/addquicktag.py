#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2021   Ahasuerus
#	 ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import MySQLdb
from SQLparsing import *
from isfdb import *
from isfdblib import *
from library import ISFDBLocalRedirect


def DoError(error, title_id):
	PrintPreSearch("Add Quick Tag")
	PrintNavBar("edit/addquicktag.cgi", 0)
        print "<h2>ERROR: %s</h2>" % error
        if title_id:
                print '<br>[<a href="http:/%s/title.cgi?%d">View This Title</a>]' % (HTFAKE, int(title_id))
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':

	(user_id, username, usertoken) = GetUserData()

        if not user_id:
                DoError('You must be logged in to tag titles', 0)

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        if form.has_key('title_id'):
                title_id = form['title_id'].value
	else:
                DoError('Specified title ID does not exit', 0)

        if form.has_key('tag'):
                new_tag = form['tag'].value
	else:
                DoError('No tag specified', 0)

	##################################################################
	# Retrieve all tags for this user/Title ID combination
	##################################################################
	tags = SQLgetUserTags(title_id, user_id)
	for tag in tags:
                if tag.lower() == new_tag.lower():
                        DoError('You have already added this Tag to this Title', title_id)

        result = SQLaddTagToTitle(new_tag, title_id, user_id)

        # Redirect the user back to the Title page
        ISFDBLocalRedirect('title.cgi?%d' % int(title_id))
