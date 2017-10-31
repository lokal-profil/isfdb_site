#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2013   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


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

	PrintHeader("Top Moderators")
	PrintNavbar('top', 0, 0, 'topmods.cgi', 0)
        filename = LOCALFILES + "top_moderators.html"
        f = open(filename,"r")
        data = f.read()
        f.close()
        print data
	PrintTrailer('top', 0, 0)

