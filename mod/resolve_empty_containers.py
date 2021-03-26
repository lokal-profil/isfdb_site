#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

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

	try:
		cleanup_id = int(sys.argv[1])
		report_type = sys.argv[2]
		if report_type not in ('decade','year','month','unknown'):
                        raise
                date_range = int(sys.argv[3])
                report_id = int(sys.argv[4])
                return_location = 'empty_containers.cgi?%s+%d+%d' % (report_type, date_range, report_id)
	except:
                PrintPreMod('Resolve Empty Container records')
                PrintNavBar()
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad arguments</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        update = 'update cleanup set resolved=1 where cleanup_id=%d' % cleanup_id
	db.query(update)
        ServerSideRedirect("http:/%s/edit/%s" % (HTFAKE, return_location))
        
