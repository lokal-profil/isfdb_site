#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2017   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.8 $
#     Date: $Date: 2017/06/13 23:53:29 $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node

if __name__ == '__main__':

	PrintHeader("Top Contributors")
	PrintNavbar('top', 0, 0, 'topcontrib.cgi', 0)

	try:
		type = int(sys.argv[1])
	except:
		type = 0

	if type == 0:
		print "<h2>Top ISFDB contributors (All Submission Types)</h2>"
		filename = LOCALFILES + "top_contributors_all.html"
                f = open(filename,"r")
                data = f.read()
                f.close()
                print data
	elif type in SUBMAP and SUBMAP[type][3]:
                print "<h2>Top ISFDB contributors (%s)</h2>" % (SUBMAP[type][3])
		filename = LOCALFILES + "top_contributors%d.html" % type
                f = open(filename,"r")
                data = f.read()
                f.close()
                print data
	else:
		print "<h3>Specified submission type is currently inactive</h3>"
        	PrintTrailer('top', 0, 0)
		sys.exit(0)

	PrintTrailer('top', 0, 0)

