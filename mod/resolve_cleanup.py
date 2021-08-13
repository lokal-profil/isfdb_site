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

from isfdb import *
from SQLparsing import *
from library import ServerSideRedirect
from login import User

	
if __name__ == '__main__':

	user = User()
	user.load()
	user.load_moderator_flag()
	if not user.moderator:
                SESSION.DisplayError('Only Moderators Can Resolve Cleanup Report Records')

        cleanup_id = SESSION.Parameter(0, 'int')
        # Mode 0 is "delete from the table"; mode 1 is "set the resolve flag"
        mode = SESSION.Parameter(1, 'int', None, (0, 1))
        report_number = SESSION.Parameter(2, 'int')
        return_location = 'cleanup_report.cgi?%d' % report_number

        if mode == 0:
                update = 'delete from cleanup where cleanup_id=%d' % cleanup_id
        else:
                update = 'update cleanup set resolved=1 where cleanup_id=%d' % cleanup_id
	db.query(update)
        ServerSideRedirect("http:/%s/edit/%s" % (HTFAKE, return_location))
        
