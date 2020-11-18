#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

	PrintPreMod('Remove Secondary Verification')
	PrintNavBar()

        try:
                ver_id = int(sys.argv[1])
                pub_id = SQLGetPubIdFromSecondaryVerification(ver_id)[0]
                pub_data = SQLGetPubById(pub_id)
                if not pub_data:
                        raise
        except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad verification ID</h3>'
		print '</div>'
		PrintPostMod(0)
		sys.exit(0)

        delete = 'delete from verification where verification_id = %d' % int(ver_id)
	db.query(delete)

        print 'Secondary Verification removed. Return to %s' % ISFDBLink('pl.cgi', pub_id, pub_data[PUB_TITLE])

	PrintPostMod(0)

