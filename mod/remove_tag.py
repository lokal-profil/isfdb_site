#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $

import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *
from login import User

def DoError(message):
        PrintPreMod('Removing a Tag from a Title Record')
        PrintNavBar()
        print '<div id="ErrorBox">'
        print '<h3>%s</h3>' % message
        print '</div>'
        PrintPostMod(0)
        sys.exit(0)
	
if __name__ == '__main__':

        try:
                user = User()
                user.load()
                user.load_bureaucrat_flag()
                if not user.bureaucrat:
                        raise
	except:
                DoError('This option can only be accessed by ISFDB Bureaucrats')

	try:
		tagmap_id = int(sys.argv[1])
	except:
                DoError('Bad argument')

        try:
                title_id = SQLgetTitleByTagId(tagmap_id)[0]
        except:
                DoError("Specified Tag ID doesn't exist")

        SQLDeleteTagMapping(tagmap_id)
	
	ServerSideRedirect("http:/%s/mod/tag_breakdown.cgi?%d" % (HTFAKE, int(title_id)))
