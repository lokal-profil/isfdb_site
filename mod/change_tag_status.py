#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
from isfdb import *
from library import ServerSideRedirect
from SQLparsing import *
from login import User


if __name__ == '__main__':

	user = User()
	user.load()
	user.load_moderator_flag()
	if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Change Tag Status')

	try:
                sys.stderr = sys.stdout
                form = cgi.FieldStorage()
		new_status = form["new_status"].value
		if new_status == 'Private':
                        numeric_status = 1
                elif new_status == 'Public':
                        numeric_status = 0
                else:
                        raise
                tag_id = int(form["tag_id"].value)
	except:
                SESSION.DisplayError('Bad Argument')

	update = 'update tags set tag_status=%d where tag_id=%d' % (numeric_status, tag_id)
	db.query(update)

	update = 'insert into tag_status_log (tag_id, user_id, new_status, timestamp) values(%d, %d, %d, NOW())' % (tag_id, int(user.id), numeric_status)
	db.query(update)

        ServerSideRedirect("http:/%s/tag.cgi?%d" % (HTFAKE, tag_id))

