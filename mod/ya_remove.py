#!_PYTHONLOC
#
#     (C) COPYRIGHT 2010-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgi
import sys
import MySQLdb
from isfdb import *
from common import *
from authorClass import *
from library import *
from SQLparsing import *

debug = 0


if __name__ == '__main__':

        PrintPreMod('Remove Alternate Name - SQL Statements')
        PrintNavBar()

	try:
		submission = sys.argv[1]
	except:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

        if NotApprovable(submission):
                sys.exit(0)

	print '<h1>SQL Updates:</h1>'
	print '<hr>'
	print '<ul>'

	submitter = ''
	try:
		xml = SQLloadXML(submission)
		doc = minidom.parseString(XMLunescape2(xml))
        	if doc.getElementsByTagName('RemovePseud'):
			merge = doc.getElementsByTagName('RemovePseud')
        		Record = GetElementValue(merge, 'Record')
        		submitter = GetElementValue(merge, 'Submitter')
       			if TagPresent(merge, 'Parent'):
        			parent = GetElementValue(merge, 'Parent')
        			#Retrieve the last pseudonym row id that matches this canonical/alternate pair
                                pseud_id = SQLGetPseudIdByAuthorAndPseud(parent,Record)
                                if not pseud_id:
                        		print '<div id="ErrorBox">'
                        		print '<h3>Error: This alternate name association no longer exists.</h3>'
                                	print '<h3>Please <a href="http:/%s/mod/hardreject.cgi?%s">use Hard Reject</a> to reject this submission.</h3>' % (HTFAKE, submission)
                        		print '</div>'
                        		PrintPostMod()
                        		sys.exit(0)
                                insert = "delete from pseudonyms where pseudo_id = %d" % int(pseud_id)
                                print '<li> ', insert
                                if debug == 0:
                                        db.query(insert)
                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)
	except:
		submitter = 'unknown'

        print '[<a href="http:/%s/ea.cgi?%d">View Former Canonical Name</a>]' % (HTFAKE, int(parent))
        print '[<a href="http:/%s/ea.cgi?%d">View Former Alternate Name</a>]' % (HTFAKE, int(Record))
        print '<p>'

        PrintPostMod(0)
