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
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
from awardtypeClass import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

	PrintPreMod('Award Type Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('AwardTypeDelete')
        if not merge:
		print '<div id="ErrorBox">'
		print '<h3>Error: Invalid Award Type</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

        current = award_type()
        current.award_type_id = int(GetElementValue(merge, 'AwardTypeId'))
        current.load()

        ##############################################################
        # Delete webpages
        ##############################################################
        delete = "delete from webpages where award_type_id=%d" % current.award_type_id
        print "<li> ", delete
        db.query(delete)

        ##############################################################
        # Delete note
        ##############################################################
        if current.award_type_note_id:
                delete = "delete from notes where note_id=%d" % int(current.award_type_note_id)
                print "<li> ", delete
                db.query(delete)

        ##############################################################
        # Delete award type record
        ##############################################################
        delete = "delete from award_types where award_type_id=%d" % current.award_type_id
        print "<li> ", delete
        db.query(delete)

        markIntegrated(db, submission, current.award_type_id)

	PrintPostMod(0)
