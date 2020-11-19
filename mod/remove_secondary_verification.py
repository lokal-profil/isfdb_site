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
from SQLparsing import *
from login import *


if __name__ == '__main__':

	PrintPreMod('Remove Secondary Verification')
	PrintNavBar()

        try:
                ver_id = int(sys.argv[1])
                ver_data = SQLGetSecondaryVerificationByVerID(ver_id)[0]
                pub_id = ver_data[VERIF_PUB_ID]
                reference_id = ver_data[VERIF_REF_ID]
                verifier_id = ver_data[VERIF_USER_ID]
                verification_time = ver_data[VERIF_TIME]
                
                pub_data = SQLGetPubById(pub_id)
                if not pub_data:
                        raise
        except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad verification ID</h3>'
		print '</div>'
		PrintPostMod(0)
		sys.exit(0)

        (deleter_id, username, usertoken) = GetUserData()

        delete = 'delete from verification where verification_id = %d' % int(ver_id)
	db.query(delete)

        insert = """insert into deleted_secondary_verifications(pub_id, reference_id, verifier_id, verification_time, deleter_id, deletion_time)
                    values(%d, %d, %d, '%s', %d, NOW())
                    """ % (int(pub_id), int(reference_id), int(verifier_id), verification_time, int(deleter_id))
	db.query(insert)

        print 'Secondary Verification removed. <br>'
        print '[%s]' % ISFDBLink('pl.cgi', pub_id, 'View This Pub')
        print '[%s]' % ISFDBLink('edit/verify.cgi', pub_id, 'View/Add Verifications')

	PrintPostMod(0)

