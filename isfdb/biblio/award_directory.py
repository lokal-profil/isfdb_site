#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import os
import string
from SQLparsing import *
from common import *


if __name__ == '__main__':

	PrintHeader('Award Directory')
	PrintNavbar('directory', 0, 0, 'directory.cgi', 0)

        print 'For the current status of the award data entry project see the <a href="%s://%s/index.php/Awards">Wiki Awards page</a>' % (PROTOCOL, WIKILOC)
        print '<p>'
        results = SQLSearchAwards('')
        PrintAwardResults(results, 10000)

        print '<p>'

	PrintTrailer('directory', 0, 0)
