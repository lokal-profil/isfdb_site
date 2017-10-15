#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2015   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2015/09/13 02:30:37 $

import string
import sys
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

	
if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################

        (userid, username, usertoken) = GetUserData()
	if SQLisUserModerator(userid) == 0:
                PrintPreMod('Resolve Cleanup records')
                PrintNavBar()
                print '<h2>Only moderators can ignore/resolve records found by cleanup reports</h2>'
                PrintPostMod()
                sys.exit(0)

	try:
		cleanup_id = int(sys.argv[1])
		# Mode 0 is "delete from the table"; mode 1 is "set the resolve flag"
		mode = int(sys.argv[2])
		if mode not in (0,1):
                        raise
                # Redirect back to cleanup_report.cgi?report_number
                return_location = 'cleanup_report.cgi?%d' % int(sys.argv[3])
	except:
                PrintPreMod('Resolve Cleanup records')
                PrintNavBar()
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad arguments</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if mode == 0:
                update = 'delete from cleanup where cleanup_id=%d' % cleanup_id
        else:
                update = 'update cleanup set resolved=1 where cleanup_id=%d' % cleanup_id
	db.query(update)
        ServerSideRedirect("http:/%s/edit/%s" % (HTFAKE, return_location))
        
