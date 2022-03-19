#!_PYTHONLOC
#
#     (C) COPYRIGHT 2011-2022  Bill Longley, Ahasuerus and Dirk Stoeker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from SQLparsing import *
from common import *
from library import *
from login import *
from myverificationsClass import MyVerifications


if __name__ == '__main__':

        start = SESSION.Parameter(0, 'int', 0)

	PrintHeader('My Primary Verifications')
	PrintNavbar('userver', 0, 0, 'userver.cgi', 0)
	
        my_verifications = MyVerifications()
        my_verifications.display()

	PrintTrailer('userver', 0, 0)

