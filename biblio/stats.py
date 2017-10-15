#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2013   Al von Ruff, Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.9 $
#     Date: $Date: 2013/12/17 03:01:28 $


import sys
import os
import string
from SQLparsing import *
from biblio import *

if __name__ == '__main__':

	PrintHeader('ISFDB Statistics')
	PrintNavbar('stats', 0, 0, 'stats.cgi', 0)
        filename = LOCALFILES + "summary_statistics.html"
        f = open(filename,"r")
        data = f.read()
        f.close()
        print data
	PrintTrailer('frontpage', 0, 0)
