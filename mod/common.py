#
#     (C) COPYRIGHT 2006-2021   Al von Ruff, Bill Longley, Ahasuerus and Dirk Stoecker
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import MySQLdb
from isfdb import *
from SQLparsing import *
from library import *
from login import *
from urlparse import urlparse

debug = 0


def findReferralLang(pub_id):
        # Find the language of the "referral" title record in this publication
        #
        # Retrieve publication data for this pub
        pub = SQLGetPubById(pub_id)
        # Retrieve the "referral" title for this pub
        # Pass a third parameter to SQLgetTitleReferral to indicate that we want EDITOR titles for magazines/fanzines
        referral_id = SQLgetTitleReferral(pub_id, pub[PUB_CTYPE], 1)
        # If a referral title record has been found, then load its data
        if referral_id != 0:
                referral_title = SQLloadTitle(referral_id)
                # Extract the referral title's language
                referral_lang = referral_title[TITLE_LANGUAGE]
        # If there is no referral title for this pub, then set the language code to None
        else:
                referral_lang = None
        return referral_lang

def UserNameLink(user_name):
        return '<a href="%s://%s/index.php/User:%s">%s</a>' % (PROTOCOL, WIKILOC, user_name, user_name)
        
def ApproveOrReject(app, submission_id):

        print '<p>'

        # First get the user information for the reviewing/approving moderator
        (reviewer_id, username, usertoken) = GetUserData()

        # Check the current status of the submission
        submission = SQLloadSubmission(submission_id)
        submitter_id = submission[SUB_SUBMITTER]
        hold_id = submission[SUB_HOLDID]
        sub_state = submission[SUB_STATE]
        sub_time = submission[SUB_TIME]
        sub_reviewed = submission[SUB_REVIEWED]
        sub_reviewer = submission[SUB_REVIEWER]
        submitting_user = SQLgetUserName(submitter_id)

        reviewer_is_moderator = SQLisUserModerator(reviewer_id)

        if sub_state in ('I', 'R'):
                print '<h3>This submission was created on %s and ' % sub_time
                if sub_state == 'R':
                        print 'rejected'
                else:
                        print 'approved'
                moderator_name = SQLgetUserName(sub_reviewer)
                print ' by %s on %s</h3>' % (WikiLink(moderator_name), sub_reviewed)
                return

        # Check if the submission was created by another moderator; if so, disallow approving
        if (int(submitter_id) != int(reviewer_id)) and SQLisUserModerator(submitter_id):
                print '<h3>Submission created by %s</h3>' % UserNameLink(submitting_user)
                return

        wiki_edits = SQLWikiEditCount(submitting_user)
        if wiki_edits < 20:
                print '<h3>New editor with %d Wiki edits.</h3><p>' % wiki_edits

        # Check if the submission is currently on hold by another moderator
        if hold_id:
                #If the submission is currently on hold by another moderator, don't allow moderation
                if int(hold_id) != int(reviewer_id):
                        holding_user = SQLgetUserName(hold_id)
                        print '<h3>Submission is currently on hold by %s</h3>' % WikiLink(holding_user)
                        # Let bureaucrats unhold submissions held by other moderators
                        if SQLisUserBureaucrat(reviewer_id):
                                print '%s <p>' % ISFDBLinkNoName('mod/unhold.cgi', submission_id, 'UNHOLD', False, 'class="hold" ')
                        return
                #If the submission is currently on hold by the reviewing moderator, allow to remove from hold
                print '<h3>Submission is currently on hold by you.</h3><p>'
                print '%s  ' % ISFDBLinkNoName('mod/unhold.cgi', submission_id, 'UNHOLD', False, 'class="hold" ')

        # If the submission is not currently on hold and the reviewer is a moderator as opposed to a self-approver, allow putting it on hold
        elif reviewer_is_moderator:
                print '%s  ' % ISFDBLinkNoName('mod/hold.cgi', submission_id, 'HOLD', False, 'class="hold" ')

        print ISFDBLinkNoName('mod/%s' % app, submission_id, 'Approve', False, 'class="approval" ')
        print '<span class="approval"><small>'
        print ISFDBLinkNoName('view_submission.cgi', submission_id, 'Public View', False, 'class="approval" ')
        print ISFDBLinkNoName('dumpxml.cgi', submission_id, 'View Raw XML', False, 'class="approval" ')
        print '</small></span>'
        print '<p><br>'
        PrintSubmissionLinks(submission_id, reviewer_id)
        print '<hr>'
        print '<form METHOD="POST" ACTION="/cgi-bin/mod/reject.cgi">'
        print '<p class="topspace"><b>Rejection Reason</b><p>'
        print '<p class="topspace"><textarea name="reason" rows="4" cols="45"></textarea>'
        print '<input name="sub_id" value="%d" type="HIDDEN">' % int(submission_id)
        print '<p class="topspace"><input id="rejection" type="SUBMIT" value="Reject">'
        print '</form>'

def PrintSubmissionLinks(submission_id, reviewer_id):
        # If the reviewer is a self-approver and not a moderator, do not display submission links
        if not SQLisUserModerator(reviewer_id):
                return
        next_sub = SQLloadNextSubmission(submission_id, reviewer_id)
        if next_sub:
                subtype = next_sub[SUB_TYPE]
                if SUBMAP.has_key(subtype):
                        next_approval_script = SUBMAP[subtype][0]
                        print ISFDBLink('mod/%s.cgi' % next_approval_script, next_sub[SUB_ID], 'Next Submission', False, 'class="approval"')
        print ISFDBLink('mod/list.cgi', 'N', 'Submission List', False, 'class="approval"')

########################################################################
#                      T I T L E   F I E L D S
########################################################################
def createNewTitle(title):
	query = "insert into titles(title_title) values('%s');" % (db.escape_string(title))
	print "<li> ", query
	if debug == 0:
		db.query(query)
	Record = db.insert_id()
	return(Record)

def setTitleName(record, title):
	update = 'update titles set title_title="%s" where title_id=%d' % (db.escape_string(title), int(record))
	print "<li>", update
	if debug == 0:
		db.query(update)

def setTitleDate(record, date):
	update = 'update titles set title_copyright="%s" where title_id=%d' % (db.escape_string(date), int(record))
	print "<li>", update
	if debug == 0:
		db.query(update)

def setTitleType(record, type):
	update = 'update titles set title_ttype="%s" where title_id=%d' % (db.escape_string(type), int(record))
	print "<li>", update
	if debug == 0:
		db.query(update)

def setTitleLength(record, length):
        if not length:
                update = 'update titles set title_storylen=NULL where title_id=%d' % int(record)
        else:
                update = 'update titles set title_storylen="%s" where title_id=%d' % (db.escape_string(length), int(record))
	print "<li>", update
	if debug == 0:
		db.query(update)

def setTitlePage(record, page, pub_id):
	query = "select * from pub_content where pub_id=%d and title_id=%d;" % (int(pub_id), int(record))
	db.query(query)
	result = db.store_result()
	if result.num_rows() == 0:
		update = "insert into pub_content(pub_id, title_id, pubc_page) values(%d, %d, '%s');" % (int(pub_id), int(record), db.escape_string(page))
	elif page == '':
		update = "update pub_content set pubc_page=NULL where title_id=%d and pub_id=%d" % (int(record), int(pub_id))
	else:
		update = "update pub_content set pubc_page='%s' where title_id=%d and pub_id=%d" % (db.escape_string(page), int(record), int(pub_id))
	print "<li>", update
	if debug == 0:
		db.query(update)

def setTitleLang(record, referral_lang):
        # Only update the language field if the language code is not None
        if not referral_lang:
                return
	update = 'update titles set title_language=%d where title_id=%d' % (int(referral_lang), int(record))
	print "<li>", update
	if debug == 0:
		db.query(update)

########################################################################
#                      T I T L E   A U T H O R
########################################################################

def addTitleAuthor(author, title_id, status):
        if not author:
                return

	##############################################
	# STEP 1 - Get the author_id for this name,
	#          or else create one
	##############################################
	query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
	if result.num_rows():
        	record = result.fetch_row()
		author_id = record[0][0]
	else:
		author_id = insertAuthorCanonical(author)

	##############################################
	# STEP 2 - Insert author mapping into 
	#          title_authors
	##############################################
	if status == 'CANONICAL':
		ca_status = 1
	elif status == 'INTERVIEWEE':
		ca_status = 2
	elif status == 'REVIEWEE':
		ca_status = 3
	insert = "insert into canonical_author(title_id, author_id, ca_status) values('%d', '%d', '%d');" % (int(title_id), author_id, ca_status)
	print "<li> ", insert
	if debug == 0:
		db.query(insert)

def update_directory(lastname):
	lastname = string.replace(lastname, '.', '')
	lastname = string.replace(lastname, ',', '')
	lastname = string.replace(lastname, '"', '')
	#lastname = string.replace(lastname, "'", '')
	lastname = string.replace(lastname, "(", '')
	lastname = string.replace(lastname, ")", '')
	lastname = string.replace(lastname, " ", '')
	section  = lastname[0:2]

	# Bullet proofing section - Make sure section is in the range Aa-Zz
	if len(section) != 2:
		return

	if section[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
		return

	# Allow an apostrophe in the second place
	if section[1] not in "abcdefghijklmnopqrstuvwxyz'":
		return

	if section[1] == "'":
		query = 'select COUNT(author_lastname) from authors where author_lastname like "%s\'%%" order by author_lastname, author_canonical' % (section[0:1])
	else:
		query = 'select COUNT(author_lastname) from authors where author_lastname like "%s%%" order by author_lastname, author_canonical' % (section[0:2])
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()

	count = int(record[0][0])
	print "<li> count %d for section [%s]" % (count, section)

	query = "select directory_mask from directory where directory_index='%s'" % (section[0])
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	bitmap = record[0][0]
	print "<li> Old bitmap: %08x" % bitmap
	bitmask = 1
	for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'"]:
		if x == section[1]:
			if count == 0:
				bitmap &= ~bitmask
			else:
				bitmap |= bitmask
			print "<li> New bitmap: %08x" % bitmap
			query = "update directory set directory_mask='%d' where directory_index='%s'" % (bitmap, section[0])
			print "<li> ", query
			db.query(query)
			return
		else:
			bitmask = bitmask<<1

def deleteFromAuthorTable(author_id):
	query = "select author_lastname from authors where author_id='%d'" % int(author_id)
        db.query(query)
        result = db.store_result()
	if result.num_rows():
        	record = result.fetch_row()
		author_lastname = str(record[0][0])
		print "<li>LASTNAME: [%s]" % author_lastname
	else:
		return

	query = "delete from authors where author_id='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete this author from the Pseudonym table where the author is the parent
	query = "delete from pseudonyms where author_id='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete this author from the Pseudonym table where the author is the alternate name
	query = "delete from pseudonyms where pseudonym='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete author's webpages
	query = "delete from webpages where author_id='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete author's emails
	query = "delete from emails where author_id='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete author's transliterated legal names
	query = "delete from trans_legal_names where author_id='%d'" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	#Delete author's transliterated canonical names
	query = "delete from trans_authors where author_id=%d" % (int(author_id))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	update_directory(author_lastname)

def deleteTitleAuthor(author, title_id, status):

	if status == 'CANONICAL':
		ca_status = 1
	elif status == 'INTERVIEWEE':
		ca_status = 2
	elif status == 'REVIEWEE':
		ca_status = 3

	##############################################
	# STEP 1 - Get the author_id for this name
	##############################################
	query = "select author_id from authors where author_canonical='%s'" % (db.escape_string(author))
        db.query(query)
        result = db.store_result()
	if result.num_rows():
        	record = result.fetch_row()
		author_id = record[0][0]
	else:
		return

	##############################################
	# STEP 2 - Delete the author entry for this
	#          title from canonical_author
	##############################################
	query = "delete from canonical_author where author_id='%d' and title_id='%d' and ca_status='%d'" % (int(author_id), int(title_id), int(ca_status))
	print "<li> ", query
	if debug == 0:
        	db.query(query)

	##############################################
	# STEP 3 - If the author still has an entry
	#          in any of the mapping tables, done.
	##############################################
	for i in ['canonical_author', 'pub_authors']:
		query = 'select COUNT(author_id) from %s where author_id=%d' % (i, author_id)
		print "<li> ", query
       		db.query(query)
       		res = db.store_result()
       		record = res.fetch_row()
		if record[0][0]:
			return

	##############################################
	# STEP 4 - If no one references the author,
	#          delete it.
	##############################################
	deleteFromAuthorTable(author_id)


def setTitleAuthors(Record, NewAuthors):
	OldAuthors = SQLTitleAuthors(int(Record))
	for author in OldAuthors:
                if author not in NewAuthors:
                        deleteTitleAuthor(author, Record, 'CANONICAL')
	for author in NewAuthors:
                if author not in OldAuthors:
                        addTitleAuthor(author, Record, 'CANONICAL')

def setReviewees(Record, NewReviewees):
	OldReviewees = SQLReviewAuthors(int(Record))
	for author in OldReviewees:
                if author not in NewReviewees:
                        deleteTitleAuthor(author, Record, 'REVIEWEE')
	for author in NewReviewees:
                if author not in OldReviewees:
                        addTitleAuthor(author, Record, 'REVIEWEE')

def setInterviewees(Record, NewInterviewees):
	OldInterviewees = SQLInterviewAuthors(int(Record))
	for author in OldInterviewees:
                if author not in NewInterviewees:
                        deleteTitleAuthor(author, Record, 'INTERVIEWEE')
	for author in NewInterviewees:
                if author not in OldInterviewees:
                        addTitleAuthor(author, Record, 'INTERVIEWEE')

########################################################################
#                    A U T H O R   T A B L E
########################################################################

def insertAuthorCanonical(author):

	# STEP 1: Insert the author into the author table
	insert = "insert into authors(author_canonical) values('%s');" % db.escape_string(author)
	print "<li> ", insert
	if debug == 0:
		db.query(insert)
	author_id = db.insert_id()

	# STEP 2: Make a first pass at calculating the author's lastname
	#
	# Step 2.1: Remove everything to the right of the first parenthesis since it's a disambiguator.
	#       The only exception is when the first parenthesis is also the first character in the name
        first_parent = author.find('(')
        if first_parent > 0:
                author = author[0:first_parent]
                author = string.strip(author)
	# Step 2.2: Get the last space-delimited segment of the author's name
	fields = string.split(author, " ")
	lastname = fields[-1]
	# If the last segment is a recognized suffix, skip it and get the previous segment
	# ('Jr.', 'Sr.', 'M.D.', 'Ph.D.', 'II', 'III', 'IV', 'D.D.', 'B.Sc.', 'B.A.', 'M.A.')
	if len(fields) > 1 and lastname in RECOGNIZED_SUFFIXES:
		lastname = fields[-2]
	# Strip trailing comma
        if lastname[-1] == ',':
                lastname = lastname[0:-1]
	update = "update authors set author_lastname='%s' where author_id='%d'" %  (db.escape_string(lastname), author_id)
	print "<li> ", update
	if debug == 0:
		db.query(update)

	# STEP 3: Update the directory bitmap
	update_directory(lastname)

	return author_id


########################################################################
#                          H I S T O R Y
########################################################################

doHistory = 1

def setHistory(table, record, field, submission, submitter, orig, to):

	(reviewer, xxx, yyy) = GetUserData()

	table      = int(table)
	record     = int(record)
	field      = int(field)
	submission = int(submission)
	submitter  = int(submitter)
	reviewer   = int(reviewer)

	if orig:
		orig       = db.escape_string(orig)
	else:
		orig = 'NULL'
	if to:
		to         = db.escape_string(to)
	else:
		to = 'NULL'

	insert = "insert into history(history_time, history_table, history_record, history_field, history_submission, history_submitter, history_reviewer, history_from, history_to) values(NOW(), %d, %d, %d, %d, %d, %d,'%s', '%s');" % (table, record, field, submission, submitter, reviewer, orig, to)
	if (debug == 0) and (doHistory == 1):
		db.query(insert)

def display_sources(submission_id):
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewPub')

        isbn = GetElementValue(merge, 'Isbn')
        format = GetElementValue(merge, 'Binding')

        if not isbn:
                return
        
        pseudo = pseudoISBN(isbn)
        if not pseudo:
                return

        # Retrieve all Web sites that ISFDB knows about
        websites = SQLLoadWebSites(isbn, None, format)
        print '<b>Additional sources:</b> '
        print '<ul>'
        for website in websites:
                print '<li><a href="%s" target="_blank">%s</a>' % (website[1], website[0])
        print '</ul>'
