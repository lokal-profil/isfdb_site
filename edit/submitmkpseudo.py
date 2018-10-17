#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2018   Al von Ruff, Bill Longley and Ahasuerus
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
from SQLparsing import *
from login import *
from library import *
from viewers import DisplayMakePseudonym
	
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Make Alternate Name Submission'
        submission.cgi_script = 'mkpseudo'
        submission.type = MOD_AUTHOR_PSEUDO
        submission.viewer = DisplayMakePseudonym

	form = cgi.FieldStorage()

	parent_id = 0
	
	if form.has_key('ParentRec'):
		parent_id = string.strip(form['ParentRec'].value)
	elif form.has_key('ParentName'):
		parent_name = string.strip(form['ParentName'].value)
	else:
                submission.error('Parent record or name must be specified')

	if form.has_key('author_id'):
		author_id = string.strip(form['author_id'].value)
		author_data = SQLloadAuthorData(int(author_id))
	else:
                submission.error('Author record must be specified')

	if not submission.user.id:
                submission.error('', author_id)

	if parent_id == 0:
		parent_data = SQLgetAuthorData(parent_name)
		if parent_data:
			parent_id = parent_data[0]
		else:
                        submission.error('Unknown parent author: %s' % parent_name)

        else:
                #The 'try' clause will generate an error if the entered number is not an integer
                try:
                        # Drop everything to the left of the last question mark in case an author URL was entered
                        parent_id = parent_id.split('?')[-1]
                        parent_data = SQLloadAuthorData(int(parent_id))
                        if not parent_data:
                                submission.error('Unknown parent author number: %s' % parent_id)

                except:
                        submission.error('Parent record must be an integer number')

        if int(author_id) == int(parent_id):
                submission.error('Author record can not be an alternate name of itself')

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <MakePseudonym>\n"

	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))

	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(author_data[AUTHOR_CANONICAL])))
	update_string += "    <Record>%d</Record>\n" % (int(author_id))
	update_string += "    <Parent>%d</Parent>\n" % (int(parent_id))
	if form.has_key('mod_note'):
		update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(form['mod_note'].value)))
	update_string += "  </MakePseudonym>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
