#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision: 1.4 $
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
from awardClass import *
from viewers import DisplayAwardLink


if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Link Award Submission'
        submission.cgi_script = 'linkaward'
        submission.type = MOD_AWARD_LINK
        submission.viewer = DisplayAwardLink

	form = cgi.FieldStorage()

	try:
		title_id = form['title_id'].value
                # Drop everything to the left of the last question mark in case a title URL was entered
                title_id = int(title_id.split('?')[-1])
                if title_id < 0:
                        raise
                if title_id == 0:
                        title_title = 'Unlink award'
                else:
                        title = SQLloadTitle(title_id)
                        if not title:
                                raise
                        title_title = title[TITLE_TITLE]
	except:
                submission.error('Non-existent title record specified')

	try:
		award_id = int(form['award_id'].value)
		award = awards(db)
		award.load(award_id)
		if not award.award_title:
                        raise
	except:
                submission.error('Non-existent award record specified')

	if not submission.user.id:
                submission.error('', award_id)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <LinkAward>\n"

	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(title_title)))
	update_string += "    <Award>%d</Award>\n" % (award_id)
	update_string += "    <Title>%d</Title>\n" % (title_id)
	if form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))
	update_string += "  </LinkAward>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
