#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2014/11/15 00:31:04 $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from login import *
from library import *
from awardcatClass import *
from SQLparsing import *
from navbar import *
from viewers import DisplayAwardCatDelete
	
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Award Category Delete Submission'
        submission.cgi_script = 'deleteawardcat'
        submission.type = MOD_AWARD_CAT_DELETE
        submission.viewer = DisplayAwardCatDelete

        form = cgi.FieldStorage()

        try:
		record = int(form['award_cat_id'].value)
		awardCat = award_cat()
		awardCat.award_cat_id = record
		awardCat.load()
		if not awardCat.award_cat_name:
                        raise
        except:
                submission.error('Invalid award category')
        
        if form.has_key('reason'):
		reason = form['reason'].value
	else:
		reason = 'No reason given.'

	if not submission.user.id:
                submission.error('', awardCat.award_cat_id)

	update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
	update_string += "<IsfdbSubmission>\n"
	update_string += "  <AwardCategoryDelete>\n"
	update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(XMLescape(awardCat.award_cat_name)))
	update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
	update_string += "    <AwardCategoryId>%d</AwardCategoryId>\n" % (awardCat.award_cat_id)
	update_string += "    <Reason>%s</Reason>\n" % db.escape_string(XMLescape(reason))
	update_string += "  </AwardCategoryDelete>\n"
	update_string += "</IsfdbSubmission>\n"

	submission.file(update_string)
