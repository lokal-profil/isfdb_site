#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus 
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
	##################################################################
	# Output the leading HTML stuff
	##################################################################

	try:
		pub_id = int(sys.argv[1])
	except:
                PrintPreMod('Resolving Suspect Image')
                PrintNavBar()
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        update = 'delete from bad_images where pub_id=%d' % pub_id
	db.query(update)
	ServerSideRedirect("http:/%s/mod/bad_images.cgi" % HTFAKE)
