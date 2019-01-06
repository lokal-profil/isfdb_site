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


import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isfdblib import *


if __name__ == '__main__':

	PrintPreMod('XML Viewer')
        PrintNavBar()

	try:
		submission = int(sys.argv[1])
	except:
                print '<h2>Invalid submission specified</h2>'
		sys.exit(0)

        query = "select * from submissions where sub_id=%d" % submission
        db.query(query)
        result = db.store_result()
        if result.num_rows() == 0:
                print '<h2>Submission number %d not found in the submission queue</h2>' % submission
                sys.exit(0)
	
        record = result.fetch_row()
	outstr = record[0][SUB_DATA]
        outstr = string.replace(outstr, '<', '&lt;')
        outstr = string.replace(outstr, '>', '&gt;')
        outstr = string.replace(outstr, '\n', '<br>')

        print outstr

        subtype = record[0][SUB_TYPE]
        approval_script = SUBMAP[subtype][0]
        print '<br><a href="http:/%s/mod/%s.cgi?%s">Back to submission</a>' % (HTFAKE, approval_script, record[0][SUB_ID])

	PrintPostMod()

