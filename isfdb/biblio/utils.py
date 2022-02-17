#
#     (C) COPYRIGHT 2004-2013   Al von Ruff and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
from isfdb import *


#==========================================================
#                 U T I L I T I E S
#==========================================================

def DecodeArg(arg):
	arg = string.replace(arg, '_', ' ')
	arg = string.replace(arg, '\\', '')
	return arg


