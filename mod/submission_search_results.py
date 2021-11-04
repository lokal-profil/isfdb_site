#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 751 $
#     Date: $Date: 2021-09-17 17:33:29 -0400 (Fri, 17 Sep 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *
import cgi


if __name__ == '__main__':

        submitter_name = SESSION.Parameter(0, 'str')
        start = SESSION.Parameter(1, 'int', 0)

        form = cgi.FieldStorage()
        try:
                submitter_name = form['submitter_name'].value
        except:
                SESSION.DisplayError('Submitter Name Not Specified')

        try:
                start = int(form['start'].value)
        except:
                start = 0

        PrintPreMod('Submission Search Results')
        PrintNavBar()

        query = """select s.*
                from submissions s, mw_user mw
                where s.sub_submitter = mw.user_id
                and mw.user_name='%s'
                and s.sub_state = 'I'
                order by s.sub_reviewed desc
                limit %d, 200""" % (db.escape_string(submitter_name), start)

	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		print '<h3>No submissions present for the specified search criteria.</h3>'
        else:
                print '<h3>Approved submissions created by user %s (%d - %d)</h3>' % (submitter_name, start+1, start+200)
                ISFDBprintSubmissionTable(result, 'I')
                if result.num_rows() > 199:
                        print '<p> %s' % ISFDBLinkNoName('mod/submission_search_results.cgi',
                                                         'submitter_name=%s&amp;start=%d' % (submitter_name, start+200), 'Next page (%d - %d)' % (start+201, start+400), True)

	PrintPostMod(0)

