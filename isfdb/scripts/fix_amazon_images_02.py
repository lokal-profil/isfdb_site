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


import cgi
import sys
import os
import string
import MySQLdb
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

if __name__ == '__main__':

    db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
    db.select_db(DBASE)

    # Retrieve Amazon cover scans with extraneous formatting
    query = "select pub_id, pub_frontimage from pubs where pub_frontimage like 'http://images-eu.amazon.com/images/P/%.02.LZZZZZZZ.jpg'"
    db.query(query)
    result = db.store_result()
    record = result.fetch_row()
    pubs = {}
    while record:
        pub_id = record[0][0]
        image = record[0][1]
        pubs[pub_id] = '%s.jpg' % image.split('.02.LZZZZZZZ.jpg')[0]
        record = result.fetch_row()
    print result.num_rows()

    for pub_id in pubs:
        image = pubs[pub_id]
        update = "update pubs set pub_frontimage = '%s' where pub_id = %d" % (pubs[pub_id], pub_id)
        print update
        db.query(update)
