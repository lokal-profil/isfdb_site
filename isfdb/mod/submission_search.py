#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $


import sys
import string
from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from login import *

PrintPreMod('Submission Search')
PrintNavBar()
print '<form METHOD="GET" action="/cgi-bin/mod/submission_search_results.cgi">'
print '<p>'
print 'User Name (case sensitive): <input NAME="submitter_name" SIZE="50">'
print '<p>'
print '<input TYPE="SUBMIT" VALUE="Submit">'
print '</form>'
print '<p>'
PrintPostMod(0)
