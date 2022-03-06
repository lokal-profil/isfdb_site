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

import os
import sys
import string
import re
from SQLparsing import *
from library import *
from nightly_cleanup import *
from nightly_html import *
from nightly_lib import *
from nightly_transliterations import *
from nightly_wiki import *

if __name__ == '__main__':
        delete_nightly()
        nightly_cleanup()
        nightly_wiki()
        nightly_transliterations()
        nightly_html()
