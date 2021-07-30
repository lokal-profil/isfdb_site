#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2021   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended titlelication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
from viewers import DisplayMakeVariant
	
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Make Variant Submission'
        submission.cgi_script = 'mkvariant'
        submission.type = MOD_TITLE_MKVARIANT
        submission.viewer = DisplayMakeVariant

	new = titles(db)
	new.cgi2obj()

	if new.error:
                submission.error(new.error)

	if not submission.user.id:
                submission.error("", new.title_id)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <MakeVariant>\n"
	update_string += "    <Record>%d</Record>\n" % (int(new.title_id))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.title_title))
	update_string += "    <Title>%s</Title>\n" % (db.escape_string(new.title_title))
	if new.title_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.title_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (db.escape_string(trans_title))
                update_string += "    </TransTitles>\n"
	update_string += "    <Year>%s</Year>\n" % (db.escape_string(new.title_year))
	update_string += "    <TitleType>%s</TitleType>\n" % (db.escape_string(new.title_ttype))
	update_string += "    <Language>%s</Language>\n" % (db.escape_string(new.title_language))
	if new.title_note:
		update_string += "    <Note>%s</Note>\n" % db.escape_string(new.title_note)
	if new.form.has_key('mod_note'):
                # Unlike the attributes of the new object, the form data is not XML-escaped, so we need to escape it here
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))
	
	#############################################################

	update_string += "    <Authors>\n"
	counter = 0
	while counter < new.num_authors:
		update_string += "      <Author>%s</Author>\n" % (db.escape_string(new.title_authors[counter]))
		counter += 1
	update_string += "    </Authors>\n"
	update_string += "  </MakeVariant>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
