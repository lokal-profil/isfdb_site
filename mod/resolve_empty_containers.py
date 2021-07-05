#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus 
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from library import *

	
if __name__ == '__main__':

        cleanup_id = SESSION.Parameter(0, 'int')
        report_type = SESSION.Parameter(1, 'str', None, ('decade','year','month','unknown'))
        date_range = SESSION.Parameter(2, 'int')
        report_id = SESSION.Parameter(3, 'int')
        return_location = 'empty_containers.cgi?%s+%d+%d' % (report_type, date_range, report_id)

        update = 'update cleanup set resolved=1 where cleanup_id=%d' % cleanup_id
	db.query(update)
        ServerSideRedirect("http:/%s/edit/%s" % (HTFAKE, return_location))
        
