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

class Bureaucrat:
        def __init__(self):
                self.user = User()
                self.user.load()
        
        def display_options(self):
        	PrintPreMod('Bureaucrat Menu')
                PrintNavBar()
                if not SQLisUserBureaucrat(self.user.id):
                        print '<h3>Only ISFDB Bureaucrats Can Access This Menu</h3>'
                	PrintPostMod(0)
                        sys.exit(0)
                print '<ul>'
                print '<li>%s' % ISFDBLink('edit/newawardtype.cgi', '', 'Add New Award Type')
                print '</ul>'
                print '<p>'
        	PrintPostMod(0)

        
if __name__ == '__main__':
        bureaucrat = Bureaucrat()
        bureaucrat.display_options()
