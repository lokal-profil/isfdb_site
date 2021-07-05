#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

	
if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')

        update = 'delete from bad_images where pub_id=%d' % pub_id
	db.query(update)
	ServerSideRedirect("http:/%s/mod/bad_images.cgi" % HTFAKE)
