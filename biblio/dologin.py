#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2015   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2015/01/31 05:22:15 $


import sys
from common import *
from login import *
from SQLparsing import *

if __name__ == '__main__':

	PrintHeader('Login')
	PrintNavbar('login', 0, 0, 0, 0)
	try:
                LoginPage(sys.argv[1], sys.argv[2])
        except:
                print '<h2>Invalid Parameters</h2>'
	PrintTrailer('login', 0, 0)
