#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2019   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import cgi
import MySQLdb
from isfdb import *
from common import *
from isfdblib import *
from library import *
from SQLparsing import *
#from xml.dom import minidom
#from xml.dom import Node


if __name__ == '__main__':

        PrintPreMod('Reject Submission')
        PrintNavBar()

	sys.stderr = sys.stdout
	form = cgi.FieldStorage()

	try:
		sub_id = int(form["sub_id"].value)
	except:
		print "ERROR: Can't get submission ID."
		sys.exit(1)

        if NotApprovable(sub_id):
                sys.exit(0)

	if form.has_key("reason"):
                # Run the rejection reason through XML escaping and
                # unescaping in order to normalize input
		reason = XMLunescape(XMLescape(form["reason"].value))
	else:
		reason = ''

        print "<ul>"

	(reviewerid, username, usertoken) = GetUserData()
	update = """update submissions set sub_state='R', sub_reason='%s',
                    sub_reviewer='%d', sub_reviewed=NOW()
                    where sub_id=%d""" % (db.escape_string(reason), int(reviewerid), sub_id)
        print "<li> ", update
	db.query(update)

        print "</ul><p><hr>"
	
	print "Record %d has been moved to the Rejected state.<br>" % sub_id
	print "<b>Reason:</b> ", reason

	print "<p>"
	print "<hr>"
	print ISFDBLink('mod/list.cgi', 'N', 'Submission List', 1)

	PrintPostMod(0)
