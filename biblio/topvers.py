#!_PYTHONLOC
#
#     (C) COPYRIGHT 2007-2013   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2013/12/17 05:50:28 $


import string
import sys
from isfdb import *
from common import *
from login import *
from SQLparsing import *


if __name__ == '__main__':

	PrintHeader("Top Verifiers")
	PrintNavbar('top', 0, 0, 'topmods.cgi', 0)
        filename = LOCALFILES + "top_verifiers.html"
        f = open(filename,"r")
        data = f.read()
        f.close()
        print data
	PrintTrailer('top', 0, 0)

