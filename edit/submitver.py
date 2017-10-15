#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.9 $
#     Date: $Date: 2017/04/15 23:47:39 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
from pubClass import pubs
	
def insert_verif_record(pub_id, refID, status, userid):
	insert = """insert into verification(pub_id, reference_id, user_id, ver_time, ver_status)
                    values(%d, %d, %d, NOW(), %d)""" % (pub_id, refID, int(userid), int(status))
	print "<li> %s" % insert
	db.query(insert)

def update_verif_record(verification_id, ver_status, userid):
	update = """update verification
                    set ver_status=%d,
                    user_id=%d,
                    ver_time=NOW()
                    where verification_id=%d""" % (ver_status, int(userid), verification_id)
	print "<li> "+update
	db.query(update)

if __name__ == '__main__':
	##################################################################
	# Output the leading HTML stuff
	##################################################################
	PrintPreSearch("Secondary Verification Submission")
	PrintNavBar(0, 0)
	
        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

	if form.has_key('pubid'):
		pub_id = int(form['pubid'].value)
	else:
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

        pub = pubs(db)
        pub.load(pub_id)
	print '<h2>Secondary verification of %s</h2>' % ISFDBLink('pl.cgi', pub_id, pub.pub_title)
	print '<ul>'
	(userid, username, usertoken) = GetUserData()
	secondary_verifications = SQLSecondaryVerifications(pub_id)
	for name in form:
		if name[:2] == 'xx':
                        reference_id = int(name[2:])
			value = form[name].value
                        verifmap = {'NOTVER':0, 'VER':1, 'NA':2}
			ver_status = verifmap.get(value, 0)
			found = 0
			for verification in secondary_verifications:
				if verification[VERIF_REF_ID] == reference_id:
					if ver_status != int(verification[VERIF_STATUS]):
						update_verif_record(verification[VERIF_ID], ver_status, userid)
					found = 1
					break
			if not found and ver_status > 0:
                                insert_verif_record(pub_id, reference_id, ver_status, userid)

	print '</ul>'

	print '[<a href="http:/%s/pl.cgi?%d">View This Pub</a>]' % (HTFAKE, pub_id)
	print '[<a href="http:/%s/edit/editpub.cgi?%d">Edit This Pub</a>]' % (HTFAKE, pub_id)
	print '[<a href="http:/%s/edit/verify.cgi?%d">View/Add Verifications</a>]' % (HTFAKE, pub_id)

	PrintPostSearch(0, 0, 0, 0, 0)
