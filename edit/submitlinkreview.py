#!_PYTHONLOC
#
#     (C) COPYRIGHT 2008-2014   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 1.11 $
#     Date: $Date: 2014/11/16 03:41:49 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
from viewers import DisplayLinkReview


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Link Review Submission'
        submission.cgi_script = 'linkreview'
        submission.type = MOD_REVIEW_LINK
        submission.viewer = DisplayLinkReview

	form = cgi.FieldStorage()

	try:
		parent_id = form['Parent'].value
	except:
                submission.error('Valid title record must be specified')

	try:
		title_id = int(form['title_id'].value)
	except:
                submission.error('Valid review record must be specified')

	if not submission.user.id:
                submission.error('', title_id)

        try:
                # Drop everything to the left of the last question mark in case a title URL was entered
                parent_id = int(parent_id.split('?')[-1])
        except:
                submission.error('Title record number must be an integer')

        if title_id == parent_id:
                submission.error('Review record can not be linked to itself')

	if parent_id != 0:
		parent = SQLloadTitle(parent_id)
		if not parent:
                        submission.error('Title record does not exist')
	
	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <LinkReview>\n"

	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

	title = SQLloadTitle(int(title_id))
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(title[TITLE_TITLE])))
	update_string += "    <Record>%d</Record>\n" % int(title_id)
	update_string += "    <Parent>%d</Parent>\n" % int(parent_id)
	if form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))
	update_string += "  </LinkReview>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
