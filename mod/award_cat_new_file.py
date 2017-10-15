#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2016/10/25 01:12:42 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardcatClass import *


if __name__ == '__main__':

	PrintPreMod('Add New Award Category - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
        	xml = SQLloadXML(submission)
                doc = minidom.parseString(XMLunescape2(xml))
                merge = doc.getElementsByTagName('NewAwardCat')
                if not merge:
                        raise
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"
        subname = GetElementValue(merge, 'Submitter')
        submitter = SQLgetSubmitterID(subname)
        AwardCatName = GetElementValue(merge, 'AwardCatName')
        AwardTypeId = GetElementValue(merge, 'AwardTypeId')
        DisplayOrder = GetElementValue(merge, 'DisplayOrder')

        #######################################
        # Insert into the award category  table
        #######################################
        if not DisplayOrder:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, NULL)" % (db.escape_string(AwardCatName), int(AwardTypeId))
        else:
                insert = "insert into award_cats(award_cat_name, award_cat_type_id, award_cat_order) values('%s', %d, %d)" % (db.escape_string(AwardCatName), int(AwardTypeId), int(DisplayOrder))
        print "<li> ", insert
        db.query(insert)
        award_cat_id = int(db.insert_id())

        #####################################
        # NOTE
        #####################################
        note_id = ''
        note = GetElementValue(merge, 'Note')
        if note:
                insert = "insert into notes(note_note) values('%s');" % db.escape_string(note)
                print "<li> ", insert
                db.query(insert)
                note_id = int(db.insert_id())
                update = "update award_cats set award_cat_note_id = %d where award_cat_id=%d" % (note_id, award_cat_id)
                print "<li> ", update
                db.query(update)

        ##########################################################
        # Insert the new webpages
        ##########################################################

        value = GetElementValue(merge, 'Webpages')
        if value:
                webpages = doc.getElementsByTagName('Webpage')
                for webpage in webpages:
                        address = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                        update = "insert into webpages(award_cat_id, url) values(%d, '%s')" % (award_cat_id, db.escape_string(address))
                        print "<li> ", update
                        db.query(update)

        markIntegrated(db, submission, award_cat_id)

	print "</ul>"
	print "<hr>"
	print '[<a href="http:/%s/mod/list.cgi?N">Submission List</a>]' % (HTFAKE)
	print '[<a href="http:/%s/award_category.cgi?%d+1">View This Category</a>]' % (HTFAKE, award_cat_id)
	print '[<a href="http:/%s/awardtype.cgi?%d">View This Category\'s Award Type</a>]' % (HTFAKE, int(AwardTypeId))

	PrintPostMod()

