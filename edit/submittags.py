#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2020   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from seriesClass import *
from SQLparsing import *
from login import *
from library import *
	
debug = 0

def DoError(error, title_id):
	PrintPreSearch("Tag Submission")
	PrintNavBar(0, 0)
        print "<h2>ERROR: %s</h2>" % error
        if title_id:
                print '<br>[<a href="http:/%s/title.cgi?%d">View This Title</a>]' % (HTFAKE, int(title_id))
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        if form.has_key('title_id'):
                title_id = int(form['title_id'].value)
	else:
                DoError("Can't find title ID", 0)

        if form.has_key('user_id'):
                user_id = int(form['user_id'].value)
	else:
                DoError("Can't find user ID", 0)

	tags = []
	counter = 1
	while counter < 100:
		key = "tag_name%d" % counter
        	if form.has_key(key):
                	tag = form[key].value
                        # Strip off leading and trailing spaces. Normally it happens
                        # in XMLescape when a submission is created. However, title tags
                        # are filed into the database directly and do not go through the
                        # standard submission process, so we need to strip spaces directly.
                        tag = string.strip(tag)
                        tag = string.rstrip(tag)
                        # Replace multiple adjacent spaces with single spaces
                        tag = ' '.join(tag.split())
                        # Only add the new tag to the list of tags if it's not already in the list
                        if tag not in tags:
                                tags.append(tag)
		counter += 1

	# Delete the old tags
	update = 'delete from tag_mapping where title_id=%d and user_id=%d' % ( int(title_id), int(user_id))
        db.query(update)

	# Insert the new tags
	for tag in tags:
                result = SQLaddTagToTitle(tag, title_id, user_id)

	# Delete all old tags that are now without an associated entry in the tag_mapping table
	SQLDeteleOrphanTags()

        ServerSideRedirect('http:/%s/title.cgi?%d' % (HTFAKE, int(title_id)))
