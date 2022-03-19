#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from nightly_cleanup import nightly_cleanup
from html_cleanup import html_cleanup

if __name__ == '__main__':
        nightly_cleanup()
        html_cleanup()
