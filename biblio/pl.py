#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2018   Al von Ruff, Kevin Pulliam (kevin.pulliam@gmail.com), Bill Longley, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string
import urllib
from isfdb import *
from common import *
from SQLparsing import *
from library import *
from isbn import convertISBN
from pubClass import pubs

def DoError(message):
        PrintHeader('Unknown Publication Record')
        PrintNavbar(0, 0, 0, 'pl.cgi', 0)
        print "<h3>%s</h3>" % message
        PrintTrailer('publication', 0, 0)
        sys.exit(0)

def PrintTitleLine(title, pub, page, reference_lang, reference = 0):
        if not reference:
                print '<li>'
        output = ''

        ##################################################
        # PAGES
        ##################################################
        if page:
                output += page
                output += " &#8226; "

        ##################################################
        # TITLE
        ##################################################
        if title[TITLE_TTYPE] == 'REVIEW':
                output += " &#8194; "
                parent_id = SQLfindReviewedTitle(title[TITLE_PUBID])
                output += '<a href="http:/%s/title.cgi?%d" dir="ltr">Review</a>: ' % (HTFAKE, title[TITLE_PUBID])
                if parent_id:
                        trans_titles = SQLloadTransTitles(title[TITLE_PUBID])
                        trans_titles_dict = {parent_id: trans_titles}
                        output += ISFDBLink('title.cgi', parent_id, title[TITLE_TITLE], False, '', trans_titles_dict)
                else:
                        output += '<i>%s</i>' % (title[TITLE_TITLE])
                authors = SQLReviewBriefAuthorRecords(title[TITLE_PUBID])
                output += " by "
                output += FormatAuthors(authors)
        elif title[TITLE_TTYPE] == 'INTERIORART' or (title[TITLE_TTYPE] == 'ESSAY' and title[TITLE_TITLE][0:6] == 'Letter'):
                output += '&#8194;%s' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])
        else:
                output += ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])

        # If this title's language is different from the language of the pub's
        # reference title, display it
        if reference_lang and title[TITLE_LANGUAGE]:
                language_id = int(title[TITLE_LANGUAGE])
                if language_id != int(reference_lang):
                        output += ' [%s]' % LANGUAGES[language_id]

        if title[TITLE_JVN] == 'Yes':
                output += " &#8226; juvenile"

        if title[TITLE_NVZ] == 'Yes':
                output += " &#8226; novelization"

        if title[TITLE_NON_GENRE] == 'Yes':
                output += " &#8226; non-genre"
        
        if title[TITLE_GRAPHIC] == 'Yes':
                output += " &#8226; graphic format"

        if title[TITLE_SERIES]:
                output += " &#8226; "
                seriesname = SQLgetSeriesName(title[TITLE_SERIES])
                output += '[<a href="http:/%s/pe.cgi?%d" dir="ltr">%s</a>' % (HTFAKE, title[TITLE_SERIES], seriesname)
                if title[TITLE_SERIESNUM] is not None:
                        output += " &#8226; %d" % title[TITLE_SERIESNUM]
                        if title[TITLE_SERIESNUM_2] is not None:
                                output += ".%s" % title[TITLE_SERIESNUM_2]
                output += ']'
        else:
                if title[TITLE_PARENT]:
                        parent_title = SQLloadTitle(title[TITLE_PARENT])
                        if parent_title != []:
                                if parent_title[TITLE_SERIES]:
                                        seriesname = SQLgetSeriesName(parent_title[TITLE_SERIES])
                                        if seriesname:
                                                output += " &#8226; "
                                                output += '[<a href="http:/%s/pe.cgi?%d" dir="ltr">%s</a>' % (HTFAKE, parent_title[TITLE_SERIES], seriesname)
                                                if parent_title[TITLE_SERIESNUM] is not None:
                                                        output += " &#8226; %d" % parent_title[TITLE_SERIESNUM]
                                                        if parent_title[TITLE_SERIESNUM_2] is not None:
                                                                output += ".%s" % parent_title[TITLE_SERIESNUM_2]
                                                output += ']'

        if title[TITLE_TTYPE] != 'COVERART':
                output += " &#8226; "
        else:
                output += ' '

        if title[TITLE_YEAR] != pub.pub_year:
                output += '(%s)' % (convertYear(title[TITLE_YEAR][:4]))
                output += " &#8226; "

        ##################################################
        # TTYPE
        ##################################################
        if title[TITLE_TTYPE] == 'COLLECTION':
                output += 'collection'
        elif title[TITLE_TTYPE] == 'ANTHOLOGY':
                output += 'anthology'
        elif title[TITLE_TTYPE] == 'SHORTFICTION':
                if title[TITLE_STORYLEN]:
                        output += title[TITLE_STORYLEN]
                else:
                        output += 'short fiction'
        elif title[TITLE_TTYPE] == 'ESSAY':
                output += 'essay'
        elif title[TITLE_TTYPE] == 'NOVEL':
                output += 'novel'
        elif title[TITLE_TTYPE] == 'OMNIBUS':
                output += 'omnibus'
        elif title[TITLE_TTYPE] == 'NONFICTION':
                output += 'nonfiction'
        elif title[TITLE_TTYPE] == 'CHAPBOOK':
                output += 'chapbook'
        elif title[TITLE_TTYPE] == 'POEM':
                output += 'poem'
        elif title[TITLE_TTYPE] == 'SERIAL':
                output += 'serial'
        elif title[TITLE_TTYPE] == 'INTERIORART':
                output += 'interior artwork'
        elif title[TITLE_TTYPE] == 'REVIEW':
                output += 'review'
        elif title[TITLE_TTYPE] == 'INTERVIEW':
                output += ' interview of '
                authors = SQLInterviewBriefAuthorRecords(title[TITLE_PUBID])
                output += FormatAuthors(authors)
                output += " &#8226; "
                output += 'interview'
        elif title[TITLE_TTYPE] == 'EDITOR':
                output += 'edited'
        elif title[TITLE_TTYPE] == 'COVERART':
                pass
        else:
                output += title[TITLE_TTYPE]
        output += ' by '

        print output

        if title[TITLE_PARENT]:
                PrintAllAuthors(title[TITLE_PARENT])
                parent_title = SQLloadTitle(title[TITLE_PARENT])
                if parent_title == []:
                        print " <b>[PARENT TITLE ERROR]</b> "
                else:
                        output = ''
                        printpseudonym = LIBsameParentAuthors(title)
                        display_parent = 1
                        parent_lang = parent_title[TITLE_LANGUAGE]
                        variant_lang = title[TITLE_LANGUAGE]
                        title_type = title[TITLE_TTYPE]
                        parent_type = parent_title[TITLE_TTYPE]
                        
                        # If the two language codes are different and the variant is not interior art
                        # and not cover art, it's a translation
                        if (parent_lang and variant_lang and parent_lang != variant_lang
                            and title_type not in ('INTERIORART', 'COVERART')):
                                translation = 1
                        else:
                                translation = 0

                        # Determine the linking element between the variant title and its parent
                        if translation:
                                aka = "trans. of"
                        elif title_type == 'SERIAL':
                                aka = "book publication as"
                        else:
                                aka = "variant of"

                        # If this is an interior art title and its parent is a cover art title, add "cover art for"
                        if (title_type == 'INTERIORART') and (parent_type == 'COVERART'):
                                aka += ' cover art for'
                                interior_cover_vt = 1
                        else:
                                interior_cover_vt = 0
                        
                        # Do not display the variant title for SERIALs if:
                        #   the VT is NOT a translation
                        #   and the parent title is a Novel or Shortfiction
                        #   and the two titles are identical up to the first left parenthesis
                        if title_type == 'SERIAL' and not translation and parent_type in ('NOVEL', 'SHORTFICTION'):
                                position = title[TITLE_TITLE].find(' (')
                                if position > 0 and parent_title[TITLE_TITLE] == title[TITLE_TITLE][:position]:
                                        display_parent = 0
                        
                        #  Display the parent title only if the titles are different
                        #    or if they have different language codes
                        #    or it's an INTERIORART/COVERART variant
                        if display_parent and ((parent_title[TITLE_TITLE] != title[TITLE_TITLE]) or translation or interior_cover_vt):
                                output += ' (%s <i>%s</i>' % (aka, ISFDBLink('title.cgi', parent_title[TITLE_PUBID], parent_title[TITLE_TITLE]))
                                if parent_title[TITLE_YEAR][:4] != title[TITLE_YEAR][:4]:
                                        output += " %s" % (convertYear(parent_title[TITLE_YEAR][:4]))
                                output += ")"
                        print output
                        if printpseudonym:
                                PrintAllAuthors(title[TITLE_PUBID], ' [as by ', ']')
        else:
                PrintAllAuthors(title[TITLE_PUBID])


def PrintContents(titles, pub, concise):
	print '<div class="ContentBox">'

	# Display the Container title if there is one
	reference_title = None
        reference_lang = None
	if pub.pub_ctype:
                referral_title_id = SQLgetTitleReferral(pub.pub_id, pub.pub_ctype, 1)
                if referral_title_id:
                        reference_title = SQLloadTitle(referral_title_id)
                        reference_lang = reference_title[TITLE_LANGUAGE]
                        # NOVEL reference titles are not displayed here; they will be displayed in the Contents section below
                        if reference_title[TITLE_TTYPE] != 'NOVEL':
                                print '<span class="containertitle">%s Title:</span>' % reference_title[TITLE_TTYPE].title()
                                PrintTitleLine(reference_title, pub, None, reference_lang, 1)

        # Determine if there are Contents titles to display
	display_contents = 0
	for title in titles:
                # Non-NOVEL reference titles are displayed on a separate line above
                if reference_title and (title[TITLE_PUBID] == reference_title[TITLE_PUBID]) and title[TITLE_TTYPE] != 'NOVEL':
                        continue
                # COVERART titles are not to be displayed in the Contents section
                if title[TITLE_TTYPE] == 'COVERART':
                        continue
                # We have found a Contents title, so we break out of the loop
                display_contents = 1
                break

        # Display Contents items if there are any
	if display_contents:
                # Get a list of pub_content records sorted by page number
                pages = getPubContentList(pub.pub_id)

                if concise:
                        mode_word = 'Full'
                        mode_letter = 'f'
                        label = 'Fiction and Essays'
                else:
                        mode_word = 'Concise'
                        mode_letter = 'c'
                        label = 'Contents'
                output = '<h2>%s <a href="http:/%s/pl.cgi?%d+%s">' % (label, HTFAKE, pub.pub_id, mode_letter)
                output += '<span class="listingtext">(view %s Listing)</span></a></h2>' % mode_word
                print output
                print '<ul>'
                printed = []
                containers = ('OMNIBUS', 'COLLECTION', 'ANTHOLOGY', 'NONFICTION', 'CHAPBOOK')
                first_container = 1
                for item in pages:
                        content_title_id = item[PUB_CONTENTS_TITLE]
                        displayed_page_num = item[PUB_CONTENTS_PAGE]
                        # For display purposes, only use the part of the page number to the left of the first pipe (|) character
                        if displayed_page_num:
                                displayed_page_num = displayed_page_num.split('|')[0]
                        for title in titles:
                                if title[TITLE_PUBID] == content_title_id:
                                        # If this user has chosen concise display, skip INTERIORART and REVIEW records
                                        if concise and (title[TITLE_TTYPE] in ('INTERIORART', 'REVIEW')):
                                                continue
                                        # If this title has already been printed, do not print 2+ occurrences
                                        if title[TITLE_PUBID] in printed:
                                                continue
                                        # Do not display COVERART and magazine editor titles in the Content section
                                        if title[TITLE_TTYPE] in ('COVERART', 'EDITOR', 'MAGAZINE', 'FANZINE'):
                                                continue
                                        # Skip titles without a title type -- this should never happen
                                        if not title[TITLE_TTYPE]:
                                                continue
                                        # Suppress the display of the FIRST container title which matches this publication's type;
                                        # subsequent container titles of the same type will be displayed
                                        if (title[TITLE_TTYPE] in containers) and (pub.pub_ctype == title[TITLE_TTYPE]):
                                                if first_container:
                                                        first_container = 0
                                                        continue
                                        PrintTitleLine(title, pub, displayed_page_num, reference_lang)
                                        printed.append(title[TITLE_PUBID])
                print '</ul>'

        print '</div>'


#==========================================================
#                       M A I N
#==========================================================

if __name__ == '__main__':

	try:
		tag = unescapeLink(sys.argv[1])
	except:
                DoError('Invalid Publication ID specified')

        arg2 = ''
	try:
		arg2 = sys.argv[2]
	except:
		pass

        #Retrieve this user's data
        (userid, username, usertoken) = GetUserData()

        #If the format, i.e. 'c'oncise or 'f'ull, was specified explicitly in the second paratemer,
        #it overrides the default
        if arg2 == 'c':
                concise = 1
        elif arg2 == 'f':
                concise = 0
        else:
                #Retrieve this user's preferences to determine whether to use the Concise format by default
                preferences = SQLLoadUserPreferences(userid)
                concise = preferences[USER_CONCISE_DISP]

	try:
		pubid = int(tag)
		publication = SQLGetPubById(pubid)
	except:
		publication = SQLGetPubByTag(tag)

	if not publication:
                DoError('Specified publication does not exist')

	pub = pubs(db)
	pub.load(publication[PUB_PUBID])
	title = 'Publication: %s' % pub.pub_title
	PrintHeader(title)
	PrintNavbar('publication', publication, concise, 'pl.cgi', sys.argv[1])

	print '<div class="ContentBox">'

	if pub.pub_image:
		print '<table>'
		print '<tr class="scan">'
		print '<td>'
		if "|" in pub.pub_image:
                        image = pub.pub_image.split("|")[0]
                        link = pub.pub_image.split("|")[1]
                else:
                        image = pub.pub_image
                        link = pub.pub_image
		print '<a href="%s"><img src="%s" ' % (link, image)
		print 'alt="picture" class="scan"></a></td>'
		print '<td class="pubheader">'

	print '<ul>'
	print '<li><b>Publication:</b>', ISFDBMouseover(pub.pub_trans_titles, pub.pub_title, '')
	printRecordID('Publication', pub.pub_id, userid)

	titles = SQLloadTitlesXBT(pub.pub_id)
	# Display a link to other issues for Magazines
	if pub.pub_ctype in ('MAGAZINE', 'FANZINE'):
                editor = ''
                #Find the EDITOR Title in this Magazine issues
        	for title in titles:
                        if title[TITLE_TTYPE] != 'EDITOR':
                                continue
                        editor = title
                #Check that the editor Title was found -- some issues may not have it
                if editor:
                        #If there is a parent EDITOR record, load it instead of the child EDITOR record
                        if editor[TITLE_PARENT]:
                                editor = SQLloadTitle(editor[TITLE_PARENT])
                        #If this EDITOR record is in a Series, link to that Series
                        if editor[TITLE_SERIES]:
                                print '<a href="http:/%s/pe.cgi?%s">(View All Issues)</a>' % (HTFAKE, editor[TITLE_SERIES])
                                print '<a href="http:/%s/seriesgrid.cgi?%s">(View Issue Grid)</a>' % (HTFAKE, editor[TITLE_SERIES])
                        #If the EDITOR record is not in a Series, check the number of magazine pubs for the record
                        else:
                                pubs_for_editor = SQLGetPubsByTitle(editor[TITLE_PUBID])
                                #Link the EDITOR record directly if it has more than 1 issue
                                if len(pubs_for_editor) > 1:
                                        print '<a "href=http:/%s/title.cgi?%s">(View All Issues)</a>' % (HTFAKE, editor[TITLE_PUBID])
	print '<li>'
        authors = SQLPubBriefAuthorRecords(pub.pub_id)
	if pub.pub_ctype in ('ANTHOLOGY', 'MAGAZINE', 'FANZINE'):
                displayPersonLabel('Editor', authors, '')
	else:
                displayPersonLabel('Author', authors, '')
        displayAuthorList(authors)

	if pub.pub_year:
		print '<li> <b>Date:</b> %s' % (convertDate(pub.pub_year, 1))

	if pub.pub_isbn:
                compact = string.replace(pub.pub_isbn, '-', '')
                compact = string.replace(compact, ' ', '')
                compactlen = len(compact)

                pseudo = pseudoISBN(pub.pub_isbn)
                invalid = validISBN(pub.pub_isbn) ^ 1
                # Bad ISBN format
                if not pseudo:
                        print '  <li id="badISBN">ISBN: %s  (Bad format)' % pub.pub_isbn
                else:
                        # ISBN fails checlsum validation
                        if invalid:
                                print '  <li id="badISBN">ISBN: %s  (Bad Checksum)' % pub.pub_isbn
                        # ISBN-10: display the ISBN-10 as well as the ISBN-13 in "small"
                        elif compactlen == 10:
                                print '  <li><b>ISBN:</b> %s [<small>%s</small>]' % (convertISBN(compact), convertISBN(toISBN13(compact)))
                        # ISBN-13
                        else:
                                # ISBN-13s which start with 978 can be converted to ISBN-10, so we display the ISBN-10
                                if compact[:3] == '978':
                                        print '  <li><b>ISBN:</b> %s [<small>%s</small>]' % (convertISBN(compact), convertISBN(toISBN10(compact)))
                                # ISBN-13s that do not start with 978 (currently 979), can't be converted to ISBN-10s
                                else:
                                        print '  <li><b>ISBN:</b> %s' % convertISBN(compact)

	if pub.pub_catalog:
                print '  <li><b>Catalog ID:</b>', pub.pub_catalog

	if pub.pub_publisher_id:
		print '<li>'
		print '  <b>Publisher:</b> %s' % ISFDBLink('publisher.cgi', pub.pub_publisher_id, pub.pub_publisher)

	if pub.pub_series_id:
		print '<li>'
		print '  <b>Pub. Series:</b> %s' % ISFDBLink('pubseries.cgi', pub.pub_series_id, pub.pub_series)

	if pub.pub_series_num:
		print '<li>'
		print '  <b>Pub. Series #:</b>', pub.pub_series_num

	if pub.pub_price:
		print '<li>'
		print '  <b>Price:</b>', pub.pub_price
	if pub.pub_pages:
		print '<li>'
		print '  <b>Pages:</b>', pub.pub_pages
	if pub.pub_ptype:
		print '<li>'
		print '  <b>Format:</b>', ISFDBPubFormat(pub.pub_ptype)
	if pub.pub_ctype:
		print '<li>'
		print '  <b>Type:</b>', pub.pub_ctype

	cover_art_titles = []
	cover_count = 1
	for title in titles:
		if title[TITLE_TTYPE] == 'COVERART':
                        cover_indicator = ''
                        if cover_count > 1:
                                cover_indicator = str(cover_count)
                        print '<li><b>Cover%s:</b>' % cover_indicator
			cover_art_titles.append(title[TITLE_PUBID])
			#PrintAllAuthors(title[TITLE_PUBID])
                        PrintTitleLine(title, pub, None, None, 1)
			cover_count += 1

	if pub.pub_note:
		print '<li>'
		print FormatNote(pub.pub_note, 'Notes', 'short', pub.pub_id, 'Publication')

	if pub.identifiers:
                print '<li>'
                print '  <b>External IDs:</b>'
                pub.printExternalIDs()

	if pub.pub_tag and SQLwikiLinkExists('Publication', pub.pub_tag):
                print "<li><b>Bibliographic Comments:</b>"
                print '<a href="http://%s/index.php/Publication:%s" dir="ltr"> View Publication comment</a> (%s)' % (WIKILOC, pub.pub_tag, pub.pub_tag)

        #Only display the image upload link if the user is logged in
        if userid:
                tag = str(pub.pub_tag)
                if pub.pub_publisher:
                        publisher_string = pub.pub_publisher
                else:
                        publisher_string = 'Unknown'
                if pub.pub_ptype:
                        format = pub.pub_ptype
                else:
                        format = ''
                pub_year = convertYear(pub.pub_year)
                if pub_year == 'unknown':
                        pub_year = 'Unknown year'
                cover_artists = []
                #Retrieve the cover artists for the Cover Art Titles
                for cover_art_title in cover_art_titles:
                        artists_for_title = SQLTitleBriefAuthorRecords(cover_art_title)
                        #Create a list of unique cover artists
                        for cover_artist in artists_for_title:
                                if cover_artist not in cover_artists:
                                        cover_artists.append(cover_artist)

                #For 0 or 1 cover artist, use template CID1
                if len(cover_artists) == 0:
                        template = 'CID1'
                elif len(cover_artists) == 1:
                        template = 'CID1'
                elif len(cover_artists) == 2:
                        template = 'CID1-2'
                #When 3 or more artists, use template CID1-3; only the first 3 artists will be defaulted
                else:
                        template = 'CID1-3'

                param = template + '\n|Title=' + pub.pub_title
                param += '\n|Edition=' + publisher_string
                if publisher_string == 'Unknown':
                        param += ' publisher'
                param += ' ' + pub_year
                if format:
                        param += ' ' + format
                param += '\n|Pub=' + tag
                if publisher_string:
                        param += '\n|Publisher=' + publisher_string
                if template == 'CID1':
                        if len(cover_artists) == 0:
                                param += '\n|Artist=' + 'Unknown'
                        else:
                                param += '\n|Artist=%s\n|ArtistId=%d' % (cover_artists[0][1], cover_artists[0][0])
                elif template == 'CID1-2':
                        param += '\n|Artist1=%s\n|Artist2=%s' % (cover_artists[0][1], cover_artists[1][1])
                elif template == 'CID1-3':
                        param += '\n|Artist1=%s\n|Artist2=%s' % (cover_artists[0][1], cover_artists[1][1])
                        param += '\n|Artist3=%s' % cover_artists[2][1]
                param += '\n|Source=Scanned by [[User:' + username + ']]'
                param = urllib.quote("{{%s}}" % param)
                upload = 'wpDestFile=%s.jpg&amp;wpUploadDescription=%s' % (tag, param)
                print "<li>"
                if not pub.pub_image:
                        message = 'Upload cover scan'
                else:
                        message = 'Upload new cover scan'
                print '<a href="http://%s/index.php/Special:Upload?%s" target="_blank">%s</a>' % (WIKILOC, upload, message)

	print '</ul>'
	if pub.pub_image:
        	print '</td>'
        	print '</table>'
                domains = RecognizedDomains()
                (webpage, credit, home_page) = BuildDisplayedURL(pub.pub_image, domains)
                print 'Cover art supplied by <a href="http://%s" target="_blank">%s</a>' % (home_page, credit)

       	print '</div>'

	PrintContents(titles, pub, concise)

        pub.PrintPrimaryVerifications()
        pub.PrintAllSecondaryVerifications()

	PrintTrailer('publication', 0, 0)


