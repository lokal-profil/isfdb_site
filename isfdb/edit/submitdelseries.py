#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2014   Ahasuerus
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
from isfdblib import *
from pubClass import *
from login import *
from library import *
from SQLparsing import *
from navbar import *
from viewers import DisplaySeriesDelete
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Series Delete Submission'
        submission.cgi_script = 'deleteseries'
        submission.type = MOD_DELETE_SERIES
        submission.viewer = DisplaySeriesDelete

        form = cgi.FieldStorage()
        try:
		series_id = int(form['series_id'].value)
		series_name = form['series_name'].value
	except:
                submission.error('Invalid series information')
        if form.has_key('reason'):
		reason = form['reason'].value
	else:
		reason = 'No reason given.'

	if not submission.user.id:
                submission.error('', series_id)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <SeriesDelete>\n"
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(series_name)))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Record>%d</Record>\n" % (series_id)
	update_string += "    <Reason>%s</Reason>\n" % (db.escape_string(XMLescape(reason)))
	update_string += "  </SeriesDelete>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
