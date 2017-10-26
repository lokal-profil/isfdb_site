#
#     (C) COPYRIGHT 2005-2017   Al von Ruff, Kevin Pulliam (kevin.pulliam@gmail.com), Bill Longley and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.31 $
#     Date: $Date: 2017/04/19 00:33:52 $


import MySQLdb
import string
from isfdb import *
from login import *
from library import *
from navbar import *
from SQLparsing import *


def Date_or_None(s):
    return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)

def isModerator(username):
	pass

##################################################################
# These routines start and end the HTML page
##################################################################
def PrintPreMod(title):
        print 'Content-type: text/html\n'
	print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
	print '<html lang="en-us">'
        print '<head>'
        print '<meta http-equiv="content-type" content="text/html; charset=' +UNICODE+ '" >'
        print '<title>%s</title>' % (title)
        print '<style type="text/css" media="screen">'
	print '  @import url("http://%s/biblio.css");' % (HTMLHOST)
        print '</style></head>'
        print '<body>'
        print '<div id="wrap">'
        print '<a class="topbanner" href="http:/%s/index.cgi"></a>' % (HTFAKE)
        print '<div id="statusbar">'
        print '<h2>%s</h2>' % (title)
        print '</div>'

##################################################
#
#	Function appears in three different locations
#	See /edit/isfdblib.py for Edit PrintUserInfo function
#	see /biblio/common.py for Regular PrintUserInfo function
#
##################################################
def PrintUserInfo():
	(userid, username, usertoken) = GetUserData()
	if username:
                PrintLoggedIn(userid, username)
	else:
                PrintNotLoggedIn(0,0)
	return username
#######################################################
#
#	Function appears in three different locations
#	Moderator NavBar function.
#	See /edit/isfdblib.py for Edit NavBar function
#	see /biblio/common.py for Regular NavBar function
#
#######################################################
def PrintNavBar():
	print '<div id="nav">'

        # Print the search box from module navbar
        PrintSearchBox('')
	
	username = PrintUserInfo()

        # Print the Other Pages section from module navbar
	PrintOtherPages('')

	print '<div class="divider">'
	print 'Moderator Links:'
	print '</div>'
	print '<ul class="navbar">'
	print '<li><a href="http:/%s/mod/list.cgi?N">Moderator</a>' % (HTFAKE)
	print '<li><a href="http:/%s/mod/recent.cgi?0+R">Recent Rejections</a>' % (HTFAKE)
	print '<li><a href="http:/%s/mod/recent.cgi?0+I">Recent Approvals</a>' % (HTFAKE)
	print '<li><a href="http:/%s/mod/recent.cgi?0+P">Errored Out Submissions</a>' % (HTFAKE)
	print '<li><a href="http:/%s/mod/cpanel.cgi">Control Panel</a>' % (HTFAKE)
	print '<li><a href="http:/%s/mod/editrefs.cgi">Edit Ref List</a>' % (HTFAKE)
	print '</ul>'
        print '</div>'
        print '<div id="main2">'
        onlineVersion = SQLgetSchemaVersion()
        if onlineVersion != SCHEMA_VER:
                print "<h3>Warning: database schema mismatch (%s vs %s)</h3>" % (onlineVersion, SCHEMA_VER)
        if username == 0:
                print '<h2>Login required to moderate changes</h2>'
                print 'You have to <a href="http:/%s/dologin.cgi?mod/list.cgi+N">login</a> to edit data.' % (HTFAKE)
                PrintPostMod()
                sys.exit(0)

        (userid, username, usertoken) = GetUserData()
        # Let Dirk P. Broer access the Missing Authors script
        if int(userid) == 15233 and 'missing_author_urls.cgi' in sys.argv[0]:
                return
	if SQLisUserModerator(userid) == 0:
                print '<h2>Moderator privileges are required for this option</h2>'
                PrintPostMod()
                sys.exit(0)


def PrintPostMod():
	print "</table>\n"

        print '</div>'
        print '<div id="bottom">'
        print COPYRIGHT
        print '<br>'
        print ENGINE
        print '</div>'
        print '</div>'
        print '</body>'
        print '</html>'
	db.close()

def markIntegrated(db, sub_id, new_record_id = None, pub_id = None):
    (reviewerid, username, usertoken) = GetUserData()
    update = "update submissions set sub_state='I', sub_reviewer='%d', sub_reviewed=NOW() where sub_id=%d" %  (int(reviewerid), int(sub_id))
    print "<li> ", update
    db.query(update)

    # For submissions that created a new database record in the database,
    # add the record number to the bofy of the submission
    if new_record_id:
        update = "update submissions set new_record_id=%d where sub_id=%d" %  (int(new_record_id), int(sub_id))
        print "<li> ", update
        db.query(update)

    # For changed publications, update the Changed Verified Pubs table and the user_status table
    if pub_id:
        # Get the ID of the submitter
        user_id = SQLGetSubmitterId(sub_id)
        # Retrieve the list of primary verifiers for this publication
        VerificationList = SQLPrimaryVerifiers(pub_id)
        for verifier in VerificationList:
            verifier_id = verifier[0]
            # If this primary verifier is the user who created the submission,
            # do not update the "changed verified pubs" table
            if verifier_id == user_id:
                continue
            update = """insert into changed_verified_pubs(pub_id, sub_id, verifier_id, change_time)
                       values(%d, %d, %d, NOW())""" % (int(pub_id), int(sub_id), int(verifier_id))
            print "<li> ", update
            db.query(update)
            SQLUpdate_last_changed_verified_pubs_DTS(verifier_id)

def NotApprovable(submission):
    if SQLloadState(submission) != 'N':
            print '<div id="ErrorBox">'
            print "<h3>Submission %d not in NEW state</h3>" % (int(submission))
            print '</div>'
            PrintPostMod()
            return 1
    (reviewerid, username, usertoken) = GetUserData()
    hold_id = SQLGetSubmissionHoldId(submission)
    if hold_id:
            if int(hold_id) != int(reviewerid):
                    holding_user = SQLgetUserName(hold_id)
                    print '<div id="ErrorBox">'
                    print "<h3>Submission can't be moderated because it is on hold by "
                    print '<a href=http://%s/index.php/User:%s>%s</a> ' % (WIKILOC, holding_user, holding_user)
                    print '<a href=http://%s/index.php/User_talk:%s>(Talk)</a></h3>' % (WIKILOC, holding_user)
                    print '</div>'
                    PrintPostMod()
                    return 1
    # If we are here, then this submission is approvable. Temporarily set its status to "inProgress".
    SQLmarkInProgress(submission)
    return 0

def PrintTableColumns(columns):
	print "<table cellpadding=0 BGCOLOR=\"#FFFFFF\">"
	print "<tr align=left bgcolor=\"#d6d6d6\">"
	for column in columns:
            if not column:
                data = '&nbsp;'
            else:
                data = column
            print "<td><b>%s</b></td>" % data
 	print "</tr>"