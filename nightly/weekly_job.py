#!_PYTHONLOC
#
#     (C) COPYRIGHT 2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 844 $
#     Date: $Date: 2022-02-15 16:06:20 -0500 (Tue, 15 Feb 2022) $

from database_stats import *
from nightly_cleanup import *
from nightly_html import *
from transliterations import *
from wiki import wiki
from sfe3 import Sfe3


if __name__ == '__main__':
        database_stats()
        nightly_cleanup_reports()
        wiki()
        transliterations()
        nightly_html()
        sfe3 = Sfe3()
        sfe3.process()
