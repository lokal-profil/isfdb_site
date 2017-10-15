#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2016   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.4 $
#     Date: $Date: 2016/10/25 01:12:42 $


import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardtypeClass import *


if __name__ == '__main__':

	PrintPreMod('Add New Award Type - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
        	xml = SQLloadXML(submission)
                doc = minidom.parseString(XMLunescape2(xml))
                merge = doc.getElementsByTagName('NewAwardType')
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
        ShortName = GetElementValue(merge, 'ShortName')
        FullName = GetElementValue(merge, 'FullName')
        AwardedBy = GetElementValue(merge, 'AwardedBy')
        AwardedFor = GetElementValue(merge, 'AwardedFor')
        Poll = GetElementValue(merge, 'Poll')
        NonGenre = GetElementValue(merge, 'NonGenre')

        #####################################
        # Insert into the award types table
        #####################################
        insert = "insert into award_types(award_type_name, award_type_by, award_type_for, award_type_short_name, award_type_poll, award_type_non_genre) values('%s', '%s', '%s', '%s', '%s', '%s')" % (db.escape_string(FullName), db.escape_string(AwardedBy), db.escape_string(AwardedFor), db.escape_string(ShortName), db.escape_string(Poll), db.escape_string(NonGenre))
        print "<li> ", insert
        db.query(insert)
        award_type_id = int(db.insert_id())

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
                update = "update award_types set award_type_note_id = %d where award_type_id=%d" % (note_id, award_type_id)
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
                        update = "insert into webpages(award_type_id, url) values(%d, '%s')" % (award_type_id, db.escape_string(address))
                        print "<li> ", update
                        db.query(update)

        markIntegrated(db, submission, award_type_id)

	print "</ul>"
	print "<hr>"
	print '[<a href="http:/%s/mod/list.cgi?N">Submission List</a>]' % (HTFAKE)
	print '[<a href="http:/%s/edit/editawardtype.cgi?%d">Edit This Award Type</a>]' % (HTFAKE, award_type_id)
	print '[<a href="http:/%s/awardtype.cgi?%d">View This Award Type</a>]' % (HTFAKE, award_type_id)

	PrintPostMod()

