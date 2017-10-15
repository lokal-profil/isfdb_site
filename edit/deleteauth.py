#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2006   Al von Ruff
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2008/04/24 10:30:47 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *


##################################################################
# Output the leading HTML stuff
##################################################################
#print "Content-type: text/html\n"
#print "<html>\n"
#print "<head><title>Delete Author</title></head>\n"
#print "<body text=\"#000000\" bgcolor=\"#ececec\">"

PrintTitle("Delete Author")
print "<h2>Deleted Author Record: %s</h2>" % sys.argv[1]
print "<a href=\"http://"+DBASEHOST+"/searchauthors.html\">[Search]</a>"
print "<a href=\"http://"+DBASEHOST+"/cgi-bin/edit/edittitle.cgi?0\">[New]</a>"
print "<hr>"
print "<p>"

db = dbConnect()
db.select_db(DBASE)
#delstring = "delete from authors where pubid = "+sys.argv[1] 
db.query(delstring)
db.close()


#
# Close the HTML page
print "</body>\n"
print "</html>\n"

