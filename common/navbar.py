#
#     (C) COPYRIGHT 2009-2019   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from SQLparsing import *

################################################################
# The routines found here are used across all ISFDB directories
# to display navigation-related menu functions.
################################################################

def PrintMessagesLink(userid, username):
	if SQLhasNewTalk(userid):
		# diff=cur causes the page to display in "diff" mode, with the
		# most recent change highlighted in a diff region at the top.
		print '<li><div class="newtalk"><a href="http://%s/index.php/User_talk:%s">My Messages</a> (new)</div>' % (WIKILOC, username)
	else:
		print '<li><a href="http://%s/index.php/User_talk:%s">My Messages</a>' % (WIKILOC, username)

def PrintWikiPointer(submitter):
	#If the count of Wiki edits is greater than X, then do not display the Wiki pointer
        if SQLWikiEditCount(submitter) > 100:
                return
	wikipointer = """<h1>Your submission must be approved by a moderator before it enters the database.</h1>
                        If the moderator has questions or comments about your submission,
                        they will be posted on your Wiki Talk page: """
	wikipointer += '<a href="http://%s/index.php/User_talk:%s">' % (WIKILOC, submitter)
	wikipointer += 'http://%s/index.php/User_talk:%s</a>.' % (WIKILOC, submitter)
	wikipointer += " Please check this page frequently for comments or questions."
	print wikipointer
        return


# Display the Search box in the navigation bar
def PrintSearchBox(page, search_value = '', search_type = ''):
        from library import ISFDBLink
        print '<div id="search">'
       	print '<a href="http:/%s/index.cgi">' % (HTFAKE)
	if page == 'frontpage':
		print '<img src="http://%s/isfdb_logo.jpg" width="129" height="85" alt="ISFDB logo">' % (HTMLHOST)
	else:
		print '<img src="http://%s/isfdb.gif" width="130" height="77" alt="ISFDB logo">' % (HTMLLOC)
        print '</a>'
	print 'Search the database'
        print '<form method="get" action="http:/%s/se.cgi" name="searchform" id="searchform">' % (HTFAKE)
	print '<p>'
	print '<input name="arg" id="searchform_arg" class="search" value="%s">' % search_value
	print '<select name="type" class="search">'
	options = ('Name', 'Fiction Titles', 'All Titles', 'Year of Title',
                   'Month of Title', 'Month of Publication', 'Series',
                   'Publication Series', 'Magazine', 'Publisher', 'ISBN',
                   'Tag', 'Award')
	for option in options:
                if option == search_type:
                        selected = ' selected="selected"'
                else:
                        selected = ''
                print '<option%s>%s</option>' % (selected, option)
        print '</select>'
        print '<input value="Go" type="submit" >'
        print '</form>'
        print '<p class="bottomlinks">'
        print ISFDBLink("adv_search_menu.cgi","","Advanced Search", argument='class="inverted"')
        print '</div>'
        return

#Display the Other Pages section in the navigation bar
def PrintOtherPages(choice):
	print '<div class="divider">'
	print 'Other Pages:'
	print '</div>'
	print '<ul class="navbar">'
	if choice != 'frontpage':
        	print '<li><a href="http:/%s/index.cgi">Home Page</a>' % (HTFAKE)
	if choice == 'Moderator':
        	print '<li><a href="http:/%s/mod/list.cgi?N">Moderator</a>' % (HTFAKE)
	print '<li><a href="http://%s/index.php/Main_Page">ISFDB Wiki</a>' % (WIKILOC)
	print '<li><a href="http://%s/index.php/ISFDB:FAQ">ISFDB FAQ</a>' % (WIKILOC)
        print '<li><a href="http:/%s/directory.cgi?author">Author Directory</a>' % (HTFAKE)
	print '<li><a href="http:/%s/award_directory.cgi">Award Directory</a>' % (HTFAKE)
        print '<li><a href="http:/%s/directory.cgi?publisher">Publisher Directory</a>' % (HTFAKE)
	print '<li><a href="http:/%s/directory.cgi?magazine">Magazine Directory</a>' % (HTFAKE)
        print '<li><a href="http:/%s/stats-and-tops.cgi">Statistics/Top Lists</a>' % (HTFAKE)
	print '<li><a href="http:/%s/recent.cgi">Recent Edits</a>' % (HTFAKE)
	print '<li><a href="http:/%s/recent_primary_ver.cgi">Primary Verifications</a>' % (HTFAKE)
	print '<li><a href="http:/%s/recentver.cgi">Secondary Verifications</a>' % (HTFAKE)
        print '<li><a href="http:/%s/edit/cleanup.cgi">Cleanup Reports</a>' % (HTFAKE)
	print '</ul>'
        return

def PrintLoggedIn(userid,username):
	print '<div class="divider">'
	print 'Logged In As'
	print '</div>'
	print '<ul class="navbar">'
	print '<li>', username
	print '<li><a href="http:/%s/dologout.cgi">Log Out</a>' % (HTFAKE)
	print '<li><a href="http://%s/index.php/Help:Navigation_Bar">Help Navigating</a>' % (WIKILOC)
	PrintMessagesLink( userid, username )
        print '<li><a href="http:/%s/mypreferences.cgi">My Preferences</a>' % (HTFAKE)
        print '<li><a href="http:/%s/myrecent.cgi?0+I">My Recent Edits</a>' % (HTFAKE)
        print '<li><a href="http:/%s/myrecent.cgi?0+N">My Pending Edits</a>' % (HTFAKE)
        print '<li><a href="http:/%s/myrecent.cgi?0+R">My Rejected Edits</a>' % (HTFAKE)
        print '<li><a href="http:/%s/myrecent.cgi?0+P">My Errored Out Edits</a>' % (HTFAKE)
        print '<li><a href="http:/%s/myvotes.cgi">My Votes</a>' % (HTFAKE)
        print '<li><a href="http:/%s/usertag.cgi?%d">My Tags</a>' % (HTFAKE, int(userid))
        print '<li><a href="http:/%s/userver.cgi">My Primary Verifications</a>' % (HTFAKE)
        print '<li><a href="http:/%s/changed_verified_pubs.cgi">My Changed Primary Verifications</a>' % (HTFAKE)
        # Display a "New" message if this user has new changes to primary-verified publications
        if SQLChangedVerifications(userid):
                print ' <span class="inverted">New!</span>'
	print '</ul>'
        return

def PrintNotLoggedIn(executable,argument):
	print '<div class="divider">'
	print 'Not Logged In'
	print '</div>'
	print '<ul class="navbar">'
	print '<li><a href="http:/%s/dologin.cgi?%s+%s">Log In</a>' % (HTFAKE, str(executable), str(argument))
	print '<li><a href="http://%s/index.php/Help:Navigation_Bar">Help Navigating</a>' % (WIKILOC)
	print '</ul>'
        return
