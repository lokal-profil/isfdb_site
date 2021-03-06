#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019-2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from SQLparsing import *
from library import ISFDBLocalRedirect
from login import User

	
if __name__ == '__main__':

        url = SESSION.Parameter(0, 'str')

	user = User()
	user.load()
	user.load_moderator_flag()
	if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Resolve SFE URLs')

        update = "update sfe3_authors set resolved=1 where url='%s'" % db.escape_string(url)
	db.query(update)
	ISFDBLocalRedirect('edit/sfe3_authors.cgi')
