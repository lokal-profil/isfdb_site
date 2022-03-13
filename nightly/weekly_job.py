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

from database_stats import database_stats
from nightly_cleanup import nightly_cleanup
from containers_cleanup import containers_cleanup
from html_cleanup import html_cleanup
from transliterations import transliterations
from translations_cleanup import translations_cleanup
from wiki import wiki
from sfe3 import Sfe3


if __name__ == '__main__':
        database_stats()
        nightly_cleanup()
        containers_cleanup()
        wiki()
        transliterations()
        translations_cleanup()
        html_cleanup()
        sfe3 = Sfe3()
        sfe3.process()
