#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2019   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 59 $
#     Date: $Date: 2018-01-16 21:18:05 -0500 (Tue, 16 Jan 2018) $

import sys
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import *
from sfe3 import Sfe3

if __name__ == '__main__':
	PrintPreSearch('SFE3 Author Articles without a matching SFE3 URL in ISFDB Author Records')
        PrintNavBar('edit/sfe3_authors.cgi', 0)

        sfe3 = Sfe3()
        sfe3.display_report()
        PrintPostSearch(0, 0, 0, 0, 0, 0)
