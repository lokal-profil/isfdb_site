#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2017   Al von Ruff, Ahasuerus and Dirk Stoeker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.30 $
#     Date: $Date: 2017/06/19 19:21:55 $


import string
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from login import *
from SQLparsing import *
from library import *
from xml.dom import minidom
from xml.dom import Node


def PrintRecord(record, eccolor, approving_moderator):
        if eccolor:
                print '<tr align=left class="table1">'
        else:
                print '<tr align=left class="table2">'

	subject = ''
	status = ''
	recordType = ''
	submitter = ''
	subtype = record[SUB_TYPE]
	if SUBMAP.has_key(subtype):
                approval_script = SUBMAP[subtype][0]
		recordType = SUBMAP[subtype][1]
		
        	# Determine the current status of the submission, including whether it's on hold
		if (record[SUB_HOLDID]):
			holder = SQLgetUserName(record[SUB_HOLDID])
			status = '<td>ON HOLD (<a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, holder, holder)
			status += ' <a href="http://%s/index.php/User_talk:%s">(Talk)</a>)</td>' % (WIKILOC, holder)
		else:
			status = "<td>%s</td>" % (record[SUB_STATE])

                user_id = record[SUB_SUBMITTER]
               
		###############################################
		# First try parsing the XML record
		###############################################
		try:
			doc = minidom.parseString(XMLunescape2(record[SUB_DATA]))
		except:
			pass

		###############################################
		# Now extract data fields
		###############################################
		try:
			doc2 = doc.getElementsByTagName(recordType)
			subject = GetElementValue(doc2, 'Subject')
			submitter = GetElementValue(doc2, 'Submitter')
			recordType = DetermineRecordType(recordType, subtype, doc2)
		except:
			subject = '<b>XML PARSE ERROR</b>'
			submitter = SQLgetUserName(user_id)

        	display_string = '<td'
        	# Submissions by the approving moderator appear in blue
        	if str(user_id) == approving_moderator:
                        display_string += ' class="submissionown"'
                # Submissions by other moderators appear in yellow
        	elif SQLisUserModerator(user_id):
                        display_string += ' class="submissionmoderator"'
                # Submissions by users with fewer than 20 Wiki edits appear in green
                elif (SQLisUserBot(user_id) == 0) and (SQLWikiEditCount(submitter) < 20):
                        display_string += ' class="submissionnewbie"'
        	display_string += '>'
                display_string += ISFDBLink("mod/%s.cgi" % approval_script, record[SUB_ID], record[SUB_ID])
                display_string += '</td>'
                print display_string
                print status
        	print "<td>%s</td>" % (recordType)

	try:
		print "<td>%s</td>" % (record[SUB_TIME])
	except:
		print "<td>unknown</td>"
	submitterlink  = '<td><a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, submitter, submitter)
	submitterlink += ' <a href="http://%s/index.php/User_talk:%s">(Talk)</a></td>' % (WIKILOC, submitter)
	print submitterlink
	print "<td>%s</td>" % (XMLunescape(subject))
        print "</tr>"



if __name__ == '__main__':

	try:
		arg = sys.argv[1]
	except:
		PrintPreMod("Bad Argument")
		PrintNavBar()
		PrintPostMod()
		sys.exit(0)

	if arg == 'N':
		title = 'New Submissions'
	elif arg == 'I':
		title = 'Approved Submissions'
	elif arg == 'R':
		title = 'Rejected Submissions'
	else:
		PrintPreMod("Bad Argument")
		PrintNavBar()
		PrintPostMod()
		sys.exit(0)

	PrintPreMod(title)
	PrintNavBar()

        print '<div id="HelpBox">'
        print '<b>Help on moderating: </b>'
        print '<a href="http://%s/index.php/Help:Screen:Moderator">Help:Screen:Moderator</a><p>' % WIKILOC
        print '</div>'

        LIBprintISFDBtime()
        
	query = "select * from submissions where sub_state='%s' order by sub_reviewed;" % (arg)
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>No submissions present</h3>'
		PrintPostMod()
		sys.exit(0)

	user_data = GetUserData()
	approving_moderator = str(user_data[0])

	print '<table class="review">'
	print '<tr>'
	print '<th>Submission</th>'
	print '<th>State</th>'
	print '<th>Type</th>'
	print '<th>Date/Time</th>'
	print '<th>Submitter</th>'
	print '<th>Subject</th>'
	print '</tr>'

        record = result.fetch_row()
	color = 0
	while record:
		PrintRecord(record[0], color, approving_moderator)
		color = color ^ 1
        	record = result.fetch_row()

	PrintPostMod()
