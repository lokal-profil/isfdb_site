#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2021   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

	
import cgi
import sys
from isfdb import *
from isfdblib import *
from seriesClass import *
from SQLparsing import *
from login import *
from library import *


if __name__ == '__main__':

	user = User()
	user.load()
	if not user.id:
                SESSION.DisplayError('You must be logged in to add tags')

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        try:
                title_id = int(form['title_id'].value)
	except:
                SESSION.DisplayError('Title ID not specified')

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
	update = 'delete from tag_mapping where title_id=%d and user_id=%d' % ( int(title_id), int(user.id))
        db.query(update)

	# Insert the new tags
	for tag in tags:
                result = SQLaddTagToTitle(tag, title_id, user.id)

	# Delete all old tags that are now without an associated entry in the tag_mapping table
	SQLDeteleOrphanTags()

        ServerSideRedirect('http:/%s/title.cgi?%d' % (HTFAKE, int(title_id)))
