#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2019   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string
from isfdb import *
from SQLparsing import *
from advSearchClass import AdvancedSearch

if __name__ == '__main__':
        search = AdvancedSearch()
        search.display_selection()
