#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *
from library import *
from SQLparsing import *
from calendarClass import CalendarMenu

if __name__ == '__main__':

        menu = CalendarMenu()
        menu.display()
