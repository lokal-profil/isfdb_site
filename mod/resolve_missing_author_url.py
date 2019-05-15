#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2018   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

	
if __name__ == '__main__':
	try:
		script_type = int(sys.argv[1])
		missing_id  = int(sys.argv[2])
                (userid, username, usertoken) = GetUserData()
                if not SQLisUserModerator(userid):
                        raise
	except:
                PrintPreMod('Resolving author URL')
                PrintNavBar()
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad arguments</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        update = 'update missing_author_urls set resolved=1 where missing_id=%d' % missing_id
	db.query(update)
	ServerSideRedirect("http:/%s/mod/missing_author_urls.cgi?%d" % (HTFAKE, script_type))
