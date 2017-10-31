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


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *


if __name__ == '__main__':

	PrintPreMod('Change Tag Status')
	PrintNavBar()

	try:
                sys.stderr = sys.stdout
                form = cgi.FieldStorage()
		new_status = form["new_status"].value
		if new_status == 'Private':
                        numeric_status = 1
                elif new_status == 'Public':
                        numeric_status = 0
                else:
                        raise
                tag_id = int(form["tag_id"].value)
                tag_name = form["tag_name"].value
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	query = "update tags set tag_status='%d' where tag_id='%d'" % (numeric_status, tag_id)
	db.query(query)

	print 'Tag status for <b>%s</b> changed to %s' % (tag_name, new_status)
	print '<br>'
	print '<a href="http:/%s/tag.cgi?%d">[<b>Return to the tag</b>]</a>' % (HTFAKE, tag_id)

	PrintPostMod()

