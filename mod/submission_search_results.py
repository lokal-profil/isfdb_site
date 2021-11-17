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

        form = cgi.FieldStorage()
        try:
                submitter_name = form['submitter_name'].value
        except:
                SESSION.DisplayError('User name not specified')

        submitter_id = SQLgetSubmitterID(submitter_name)
        if not submitter_id:
                SESSION.DisplayError('An ISFDB user with this name does not exist. Note that user names are case sensitive and the first letter is always capitalized.')

        try:
                start = int(form['start'].value)
        except:
                start = 0

        PrintPreMod('Submission Search Results')
        PrintNavBar()

        query = """select *
                from submissions
                where sub_submitter = %d
                and sub_state = 'I'
                order by sub_reviewed desc
                limit %d, 200""" % (submitter_id, start)

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

