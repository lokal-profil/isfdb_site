#!_PYTHONLOC
#
#     (C) COPYRIGHT 2019   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from sfe3 import Sfe3

def nightly_3rd_parties():
        sfe3 = Sfe3()
        sfe3.nightly_process()
