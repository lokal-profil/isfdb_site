#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2006   Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2008/04/24 10:30:54 $


import cgi
import sys
import MySQLdb
import string
from isfdb import *
from isfdblib import *

############################################################
# Set up variables and output HTML header
############################################################
printed  = 0
eccolor  = 1
PrintPreSearch("Publication Search")

############################################################
# Setup environment and build SQL query from form data
############################################################
sys.stderr = sys.stdout
form = cgi.FieldStorage()
myisfdb = ISFDB()
(search_string, subsequent) = myisfdb.BuildPubSQL_FromForm(form, "0")

############################################################
# Connect to the database and print the results
############################################################
db = dbConnect()
db.select_db(DBASE)
db.query(search_string)
result = db.store_result()
record = result.fetch_row()
PrintPubHeader(record)
while record:
	PrintPubRecord(record, eccolor)
	eccolor = eccolor ^ 1
	printed = printed + 1
	record = result.fetch_row()

############################################################
# Close the database and finish the HTML
############################################################
db.close()
next_start = myisfdb.GetStart()+100
next_records = "%d-%d" % (next_start, next_start+99)
PrintPostSearch("pubsearch2", next_records, subsequent, printed, 0)

