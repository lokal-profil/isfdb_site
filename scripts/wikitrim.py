#!/usr/bin/python
#    (C) COPYRIGHT 2008-2011   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2011/11/13 07:02:29 $

import cgi
import sys
import os
import MySQLdb
from localdefs import *


def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)



def trimpages(db, page_id):

    ###############################################################
    # Get every text revision associated with the page, and delete all but the latest 50.
    ###############################################################
    query = "select rev_text_id from mw_revision where rev_page = '%s' order by rev_id desc;" % (page_id)
    db.query(query)
    result = db.store_result()
    counter = 0
    record = result.fetch_row()
    while record:
        if (counter > 50):
            delete = "delete from mw_text where old_id='%d'" % (record[0][0])
            print delete
            db.query(delete)
        record = result.fetch_row()
        counter += 1



if __name__ == '__main__':


    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    ###############################################################
    # Find every page in the wiki, and call trimpages() with its
    # namespace and title
    ###############################################################
    #query = "select * from mw_page where page_namespace = 4 and page_title in ('Community_Portal', 'Help_desk', 'Moderator_noticeboard', 'Verification_requests')"
    query = "select * from mw_page"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    while record:
        #print "Page ID: %s" % (record[0][0])
        trimpages(db, record[0][0])
        record = result.fetch_row()
    db.close()
