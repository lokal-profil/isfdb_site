#!/usr/bin/python
#    (C) COPYRIGHT 2008-2013   Al von Ruff, MaryD, RobertGl and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import os
import MySQLdb
import md5
from localdefs import *
from struct import *


def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)



if __name__ == '__main__':


	try:
		username = sys.argv[1]
		password = sys.argv[2]
	except:
		print 'usage: create_user.py username password'
		print '       The third parameter, if specified, should be 1 for moderator users'
		print '       and 0 for non-moderator users. The default is 1 (moderator).'
		sys.exit(1)

        # By default, the new user is a moderator. The third parameter passed to this script (if '0')
        # overrides the default behavior and makes the new user a non-privileged user.
        moderator = '1'
        try:
		moderator = sys.argv[3]
	except:
		pass

	db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
	db.select_db(DBASE)

	###############################################################
	# Insert a username and password into mw_user
	###############################################################
	query = "insert into mw_user(user_name,user_real_name,user_password,user_newpassword,user_email,user_options,user_token,user_touched) values('%s','','','','','','','')" % (username)
	db.query(query)
	user_id = db.insert_id()

	hash = md5.new()
	hash.update(password)
	password = str(hash.hexdigest())

	newstr = "%d-%s" % (user_id, password)
	hash2 = md5.new()
	hash2.update(newstr)
	submitted_password = hash2.hexdigest()

	query = "update mw_user set user_password='%s' where user_id='%d'" % (submitted_password, user_id)
	db.query(query)

        if moderator == '1':
                # Insert moderator rights into mw_user_groups
                query = "insert into mw_user_groups(ug_user, ug_group) values(%d, '%s')" % (user_id, 'sysop')
                db.query(query)
        
        ###############################################################
        # mw_user_groups is an InnoDB table. We have to commit changes,
        # otherwise this insertion does nothing.
        ###############################################################
	db.commit()

	db.close()
