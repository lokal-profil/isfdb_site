#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import viewers
from isfdb import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission_id = SESSION.Parameter(0, 'int')
        submission = SQLloadSubmission(submission_id)
	if not submission:
                SESSION.DisplayError('Specified submission ID does not exist')

        sub_type = submission[SUB_TYPE]
        sub_user = submission[SUB_SUBMITTER]
        sub_reviewer = submission[SUB_REVIEWER]
        sub_state = submission[SUB_STATE]
        sub_reason = submission[SUB_REASON]
        sub_data = submission[SUB_DATA]
        sub_time = submission[SUB_TIME]
        sub_reviewed = submission[SUB_REVIEWED]
        approval_script = SUBMAP[sub_type][0]
        xml_tag = SUBMAP[sub_type][1]
        displayPage = SUBMAP[sub_type][2]

        # Parse the XML record and get the "true" submission type for display purposes
        try:
                doc = minidom.parseString(XMLunescape2(sub_data))
        except:
                SESSION.DisplayError('Submission contains invalid XML and cannot be displayed')

        try:
                doc2 = doc.getElementsByTagName(xml_tag)
                subject = GetElementValue(doc2, 'Subject')
        except:
                SESSION.DisplayError('Submission contains invalid XML and cannot be displayed')

        display_tag = DetermineRecordType(xml_tag, sub_type, doc2)
        # If the "corrected" display type is not the same as the XML tag, then display the former
        if display_tag != xml_tag:
                displayType = display_tag
        # Otherwise display the full type name stored in SUBMAP
        else:
                displayType = SUBMAP[sub_type][3]

        # Compose the header, which will depend on the submission type and its approval status
        if sub_state == 'N':
                header = 'Pending'
        elif sub_state == 'I':
                header = 'Approved'
        elif sub_state == 'R':
                header = 'Canceled/Rejected'
        elif sub_state == 'P':
                header = 'In Progress or Errored Out'
        else:
                header = 'INVALID SUBMISSION STATUS!!!'
        header += ' %s Submission' % displayType
        PrintHeader(header)
        PrintNavbar('recent', 0, 0, 'view_submission.cgi', 0)
        
        if sub_state == 'R':
                print '<b>Cancellation/Rejection Reason</b>: %s<p>' % sub_reason

        print '<b>Note</b>: For "Edit" submissions, the "Current" column shows the data as it currently exists in the database,'
        print 'not as it existed when the submission was created.<p>'

        function_name = SUBMAP[sub_type][5]
        function_to_call = getattr(viewers, function_name)
        submitter = function_to_call(submission_id)

        if sub_state == 'I':
                (subjectLink, new_record) = getSubjectLink(submission, doc2, sub_type)
                if new_record:
                        print '<p><b>New record:</b> %s' % subjectLink

        print '<p>View <a href="http:/%s/dumpxml.cgi?%d">the submission as raw XML</a>.' % (HTFAKE, int(submission_id))
        
        print '<p><b>Submitted by</b> %s on %s' % (WikiLink(submitter), sub_time)

        (userID, username, usertoken) = GetUserData()
        # If the viewing user is the submitter and the submission is "N"ew, allow the user to cancel
        if int(userID) == int(sub_user) and sub_state == 'N':
                print ' [<a href="http:/%s/cancelsubmission.cgi?%d">Cancel submission</a>]' % (HTFAKE, submission_id)
        # If the submission has been reviewed, display the reviewer's name
        elif sub_reviewer:
                moderator_name = SQLgetUserName(sub_reviewer)
                if sub_state == 'R':
                        status = 'Rejected'
                else:
                        status = 'Approved'
                print '<p><b>%s by</b> %s on %s' % (status, WikiLink(moderator_name), sub_reviewed)

        if SQLisUserModerator(userID):
                if sub_state == 'R':
                        print '<p>%s' % ISFDBLink('mod/unreject.cgi', submission_id, 'Unreject Submission')
                elif sub_state == 'N':
                        print '<p>%s' % ISFDBLink('mod/%s.cgi' % approval_script, submission_id, 'Moderator View')

	PrintTrailer('recent', 0, 0)

