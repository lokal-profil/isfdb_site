#!_PYTHONLOC
#
#     (C) COPYRIGHT 2020   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 477 $
#     Date: $Date: 2019-12-01 20:16:10 -0500 (Sun, 01 Dec 2019) $


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node


if __name__ == '__main__':

	PrintHeader('Recent Activity')
	PrintNavbar('recent_activity', 0, 0, 'recent_activity.cgi', 0)

	print '<ul>'
	print '<li>%s' % ISFDBLink('recent.cgi', '', 'Recent Edits')
	print '<li>%s' % ISFDBLink('recent_primary_ver.cgi', '', 'Recent Primary Verifications')
	print '<li>%s' % ISFDBLink('recentver.cgi', '', 'Recently Added Secondary Verifications')
	print '<li>%s' % ISFDBLink('removed_secondary_verifications.cgi', '', 'Recently Removed Secondary Verifications')
	print '</ul>'

	PrintTrailer('recent_activity', 0, 0)

