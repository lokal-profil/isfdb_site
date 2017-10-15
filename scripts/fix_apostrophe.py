#!_PYTHONLOC
# -*- coding: cp1252 -*-
#
#     (C) COPYRIGHT 2009   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2009/10/26 00:49:49 $


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
	
	query_main = "select title_id,title_title from titles where title_title like '%\�%'"
	db.query(query_main)
	result_main = db.store_result()
	titles = result_main.fetch_row(0)
	for title in titles:
            title_id = title[0]
            title_title = title[1]
            new_title = db.escape_string(string.replace(title_title,'\x92',"'"))
            #print new_title
            update = "update titles set title_title = '%s' where title_id = '%d'" % (new_title,title_id)
            print update
            db.query(update)
