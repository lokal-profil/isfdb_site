#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
#	 ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.11 $
#     Date: $Date: 2017/06/13 23:53:29 $

import cgi
import sys
from isfdb import *
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node
	

def GetElementValue(element, tag):
        document = element[0].getElementsByTagName(tag)
        try:
                value = document[0].firstChild.data.encode(UNICODE)
        except:
                value = ''
        return value


def SendResponse(success, errorMessage):
        print '<?xml version="1.0" encoding="%s" ?>' % UNICODE
	print '<ISFDB>'
	if success:
		print '<Status>OK</Status>'
	else:
		print '<Status>FAIL</Status>'
		print '<Error>%s</Error>' % errorMessage
	print '</ISFDB>'
	sys.exit(0)

def deleteLicenseKey(xmldata):
	index = string.find(xmldata, '<LicenseKey>')
	if index:
		newxml = xmldata[:index]
	else:
		return(xmldata)
	index = string.find(xmldata, '</LicenseKey>')
	if index:
		index += 13
		newxml += xmldata[index:]
		return(newxml)
	return(xmldata)


if __name__ == '__main__':

	print 'Content-type: text/html\n'

	XMLdata = sys.stdin.read()
	index = string.find(XMLdata, "<?xml ")
	XMLdata = XMLdata[index:]
	try:
		doc = minidom.parseString(XMLdata)
	except:
		SendResponse(0, "Bad XML data")

	for type in SUBMAP:
        	merge = doc.getElementsByTagName(SUBMAP[type][1])
        	if merge:
        		key = GetElementValue(merge, 'LicenseKey')
			if key == '':
				SendResponse(0, "No LicenseKey Field")

        		submitter = GetElementValue(merge, 'Submitter')
			if submitter == '':
				SendResponse(0, "No Submitter Field")
			valid_submitters = ('Ahasuerus', 'Fixer')
			if submitter not in valid_submitters:
                                SendResponse(0, "This user is not authorized to create submissions via the ISFDB Web API. Post on the ISFDB Moderator Noticeboard if you need access.")

			submitter_id = SQLgetSubmitterID(submitter)

			query = "select * from license_keys where user_id=%d and license_key='%s'" % (int(submitter_id), db.escape_string(key))
			db.query(query)
			result = db.store_result()
			if result.num_rows() == 0:
				SendResponse(0, "Bad License Key")

			cleanData = deleteLicenseKey(XMLdata)
			# Collapse multiple adjacent spaces
			cleanData = " ".join(cleanData.split())
			submission = "insert into submissions(sub_state, sub_type, sub_data, sub_time, sub_submitter) values('N', %d, '%s', NOW(), %d)" % (type, db.escape_string(cleanData), submitter_id)
			db.query(submission)
			SendResponse(1, 0)
			sys.exit(0)

	SendResponse(0, "Bad Submission Type")
