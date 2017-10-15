#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2014/02/26 05:49:20 $


import sys
import os
import string
from SQLparsing import *
from common import *


if __name__ == '__main__':

	PrintHeader('Award Directory')
	PrintNavbar('directory', 0, 0, 'directory.cgi', 0)

        print 'For the current status of the award data entry project see the <a href="http://%s/index.php/Awards">Wiki Awards page</a>' % (WIKILOC)
        print '<p>'
        results = SQLSearchAwards('')
        PrintAwardResults(results)

        print '<p>'

	PrintTrailer('directory', 0, 0)
