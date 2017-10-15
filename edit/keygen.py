#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2014   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2014/09/11 22:30:35 $


import sys
import md5
import random
from isfdb import *
from isfdblib import *
from SQLparsing import *

def GenerateKey(plain):
	hash = md5.new()
	hash.update(plain)
	return hash.hexdigest()

if __name__ == '__main__':

        try:
                mode = sys.argv[1]
        except:
		mode = 'view_key'

        PrintPreSearch("Key Maintenance")
        PrintNavBar(0, 0)

	(userid, username, usertoken) = GetUserData()
	if userid == 0:
		print "<h2>Must be logged in to perform key maintenance</h2>"
		PrintPostSearch(0, 0, 0, 0, 0)
		sys.exit(0)

	print 'A license key is only required to submit data programmatically.'
	print 'It is not needed for manual editing.<p>'

	print '<b>License Key info for</b>: [<a href="http://%s/index.php/User:%s">%s</a>]<br>' % (WIKILOC, username, username)
	if mode == 'view_key':
        	query = "select * from license_keys where user_id=%d" % int(userid)
        	db.query(query)
        	result = db.store_result()
		if result.num_rows() > 0:
        		record = result.fetch_row()
			print "<b>License Key:</b> %s" % (record[0][2])
        	else:
			print "<b>License Key:</b> NOT SET" 
	elif mode == 'new_key':
		number = random.random()
		number = number * 1000000.0
		intnum = int(number)
		strnum = str(intnum)
		license_key = GenerateKey(strnum)
		print "<b>License Key:</b> %s" % (license_key)

        	query = "select * from license_keys where user_id=%d" % int(userid)
        	db.query(query)
        	result = db.store_result()
		if result.num_rows() > 0:
			query = "update license_keys set license_key='%s' where user_id=%d" % (license_key, int(userid))
		else:
			query = "insert into license_keys(license_key, user_id) values('%s', %d)" % (license_key, int(userid))
        	db.query(query)

	print '<br><p>[<a href="http:/%s/edit/keygen.cgi?new_key">Generate New Key</a>]' % (HTFAKE)
	PrintPostSearch(0, 0, 0, 0, 0)
