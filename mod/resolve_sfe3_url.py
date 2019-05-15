#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus 
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
from login import User

	
if __name__ == '__main__':
	try:
		url = sys.argv[1]
                user = User()
                user.load()
                user.load_moderator_flag()
                if not user.moderator:
                        raise
	except:
                PrintPreMod('Resolving SFE3 URL')
                PrintNavBar()
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad arguments</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        update = "update sfe3_authors set resolved=1 where url='%s'" % db.escape_string(url)
	db.query(update)
	ServerSideRedirect("http:/%s/edit/sfe3_authors.cgi" % HTFAKE )
