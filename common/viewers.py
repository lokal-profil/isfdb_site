# -*- coding: cp1252 -*-
#
#     (C) COPYRIGHT 2007-2021   Al von Ruff, Ahasuerus, Bill Longley and Klaus Elsbernd
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import re
import string
from xml.dom import minidom
from xml.dom import Node
from library import *


###########################################################
# The following functions check the existence of entered
# values in the database
###########################################################

def CheckSeries(value):
        warning = ''
        series_id = SQLFindSeriesId(value)
        if not series_id:
                warning = 'Unknown Series'
        else:
                value = ISFDBLink('pe.cgi', series_id, value)
        return (value, warning)

def CheckPubSeries(value):
        warning = ''
        pubseries = SQLFindPubSeries(value, 'exact')
        if not pubseries:
                warning = 'Unknown Publication Series'
        else:
                if len(pubseries) == 1:
                        value = ISFDBLink('pubseries.cgi', pubseries[0][PUB_SERIES_ID], value)
        return (value, warning)

def CheckPublisher(value):
        warning = ''
        publisher = SQLFindPublisher(value, 'exact')
        if not publisher:
                warning = 'Unknown Publisher'
        else:
                if len(publisher) == 1:
                        value = ISFDBLink('publisher.cgi', publisher[0][PUBLISHER_ID], value)
        return (value, warning)

def CheckPrice(value):
        warning = ''
        if 'CDN' in value.upper():
                warning = 'CDN is invalid. Use leading C$ for prices in Canadian dollars.'
        if 'EUR' in value.upper():
                warning = 'EUR is invalid. Use %s for prices in euros.' % EURO_SIGN
        for currency_sign in ('$', BAHT_SIGN, EURO_SIGN, PESO_SIGN, POUND_SIGN, YEN_SIGN):
                if (currency_sign + ' ') in value:
                        warning = 'Spaces after the %s sign are not allowed.' % currency_sign
                        break
        if EURO_SIGN in value and not value.startswith(EURO_SIGN):
                warning = 'Euro sign must be at the beginning of the price value.'
        if EURO_SIGN in value and ',' in value:
                warning = 'Euro prices must not include commas.'
        for currency_sign in ('$', POUND_SIGN):
                if currency_sign in value and ',' in value and '.' not in value:
                        warning = 'For %s prices, a period must be used as the decimal separator.' % currency_sign
                        break
        if value.lower().startswith('http'):
                warning = 'Prices must not start with http.'
        if value.replace('.','').replace(',','').isdigit():
                warning = 'Prices should contain a currency symbol or abbreviation.'
        if re.search('^[0-9]{1,}', value) and '/' not in value:
                warning = 'Prices cannot start with a digit. The only exception is pre-decimilisation UK prices which must contain a slash.'
        if re.search('\.[0-9]{3,}$', value):
                warning = '4 or more consecutive digits must be separated with a comma, not a period.'
        if re.search('[0-9]{4,}$', value):
                warning = '4 or more consecutive digits must be separated with a comma.'
        if 'jp' in value.lower():
                warning = 'JP is not a valid currency code. Use the Yen sign instead.'
        if '&#20870;' in value:
                warning = '&#20870; is not a valid currency code. Use the Yen sign instead.'
        if value.count(' ') > 1:
                warning = 'More than one space character is not allowed in the price field'
        if ' $' in value:
                warning = 'Dollar sign cannot follow the space character in the price field'
        if '+' in value:
                warning = 'Plus signs are not allowed in the price field'
        if re.search('[0-9]{1,} ', value):
                warning = 'A space cannot follow a digit in the price field'
        return (value, warning)

def CheckISBN(value, XmlData):
        warning = ''
        invalid = validISBN(value) ^ 1
        if invalid:
                warning = 'Bad checksum'
        elif value:
                isbn_length = ISBNlength(value)
                pub_date = GetElementValue(XmlData, 'Year')
                # If there is no publication date in the body of the submission
                # AND the editor is NOT trying to remove the ISBN, then
                # retrieve the publication date from the publication record
                if not pub_date:
                        pub_id = GetElementValue(XmlData, 'Record')
                        pub_data = SQLGetPubById(pub_id)
                        if pub_data:
                                pub_date = pub_data[PUB_YEAR]
                if pub_date:
                        if Compare2Dates(pub_date, '2005-00-00') == 1 and isbn_length == 13:
                                warning = '13-digit ISBN for a pre-2005 publication'
                        if Compare2Dates('2007-00-00', pub_date) == 1 and isbn_length == 10:
                                warning = '10-digit ISBN for a post-2007 publication'
        return warning

def DuplicateCatalogId(value):
        warning = ''
        results = SQLFindPubsByCatalogId(value)
        if results:
                link = AdvSearchLink((('TYPE', 'Publication'),
                                      ('USE_1', 'pub_catalog'),
                                      ('OPERATOR_1', 'exact'),
                                      ('TERM_1', value),
                                      ('ORDERBY', 'pub_title'),
                                      ('C', 'AND')))
                warning = '%sCatalog ID already on file</a>' % link
        return warning

def DuplicateISBN(value, current_pub_id = 0):
        from isbn import isbnVariations
        warning = ''
        # Get possible ISBN variations
        targets = isbnVariations(value)
        results = SQLFindPubsByIsbn(targets, current_pub_id)
        if results:
                link = AdvSearchLink((('TYPE', 'Publication'),
                                      ('USE_1', 'pub_isbn'),
                                      ('OPERATOR_1', 'exact'),
                                      ('TERM_1', value),
                                      ('ORDERBY', 'pub_title'),
                                      ('C', 'AND')))
                warning = '%sISBN already on file</a>' % link
        return warning

def CheckImage(value, XmlData):
        from pubClass import pubs
        warning = ''
        domains = RecognizedDomains()
        valid_domain = 0
        for domain in domains:
                if (domain[0] in value) and (domain[3] == 1):
                        # If a required URL segment is not in this URL, it's not valid
                        if len(domain) > 4 and domain[4] and domain[4] not in value:
                                continue
                        valid_domain = 1
                        if len(domain) > 5 and domain[5] and '|' not in value:
                                warning = "For images hosted by this site, the URL of the associated Web page must be entered after a '|'."
                        break
        if not valid_domain:
                warning = 'Image hosted by a site which we do not have permission to link to'
        if 'sf-encyclopedia.uk' in value and '/clute/' not in value and '/langford/' not in value and '/robinson/' not in value:
                warning += 'For SFE-hosted images, only links to /clute/, /langford/ and /robinson/ sub-directories are allowed.'
        
        # For Amazon images, only cropping ("_CR") suffixes are allowed
        if (not warning
            and 'amazon.' in value
            and not re.match('.*/images/[PIG]/[0-9A-Za-z+-]{10}[LS]?(\._CR[0-9]+,[0-9]+,[0-9]+,[0-9]+)?\.(gif|png|jpg)$', value.replace('%2B','+'))
            and not re.match('.*\.images-amazon\.com/images/G/0[1-3]/ciu/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{22,24}\.L\.(gif|png|jpg)$', value)
            and not re.match('.*\.ssl-images-amazon\.com/images/S/amzn-author-media-prod/[0-9a-z]{26}\.(gif|png|jpg)$', value)):
                warning = 'Unsupported formatting in an Amazon URL. Only properly structured _CR formatting codes are currently allowed.'
        if (not warning
            and 'amazon.' in value
            and not re.match('.*/images/I/[0-9A-Za-z+-]{10}[LS]', value.replace('%2B','+'))):
                warning = 'Note that Amazon URLs which do not start with "/images/I/" may not be stable.'

        if not warning and WIKILOC in value:
                pub_id = GetElementValue(XmlData, 'Record')
                cloned = GetElementValue(XmlData, 'ClonedTo')
                if pub_id and not cloned:
                        current = pubs(db)
                        current.load(int(pub_id))
                        if current.pub_tag not in value:
                                warning = 'Wiki-hosted image URL %s doesn\'t match the internal publication tag %s.' % (value, current.pub_tag)

        if value and not cloningFlag(XmlData):
                results = SQLDuplicateImageURL(value)
                if results:
                        link = AdvSearchLink((('TYPE', 'Publication'),
                                              ('USE_1', 'pub_frontimage'),
                                              ('O_1', 'exact'),
                                              ('TERM_1', value),
                                              ('ORDERBY', 'pub_title'),
                                              ('C', 'AND')))
                        warning = '%sImage URL already on file</a>' % link

        return warning

#################################################################
# The following functions are used to show a single field of data
# with no side-by-side changes.
#################################################################

def PrintLabel(Label):
        if Label in SUBMISSION_DISPLAY:
                display_label = SUBMISSION_DISPLAY[Label]
        else:
                display_label = Label
        print '<td class="label"><b>%s</b></td>' % display_label

def PrintField1(Label, Used, Value):
        print '<tr>'
        PrintLabel(Label)
        if Used:
                print '<td class="keep">'
                print Value
                print '</td>'
        else:
                print '<td class="drop">'
                print '-'
                print '</td>'
        print '</tr>'

def PrintField2Columns(Label, Used, Value, Warning):
        print '<tr>'
        PrintLabel(Label)
        if Used:
                print '<td class="keep">'
                print Value
                print '</td>'
        else:
                print '<td class="drop">'
                print '-'
                print '</td>'
        if Warning:
                print '<td class="warn">%s</td>' % Warning
        else:
                print '<td class="blankwarning">&nbsp;</td>'
        print '</tr>'

def PrintField1XML(Label, XmlData, title = 0):
        warning = ''
        value = GetElementValue(XmlData, Label)
        if TagPresent(XmlData, Label):
                ui = isfdbUI()
                if Label == 'Image':
                        warning = CheckImage(value, XmlData)
                        value = FormatImage(value)
                
                elif Label == 'Publisher':
                        (value, warning) = CheckPublisher(value)

                elif Label == 'Price':
                        (value, warning) = CheckPrice(value)

                elif Label == 'PubSeries':
                        (value, warning) = CheckPubSeries(value)

                elif Label == 'Year':
                        if title:
                                date_status = Compare2Dates(value, title[TITLE_YEAR])
                                if date_status == 1:
                                        warning = 'Pub date earlier than title date'
                                elif date_status == 2:
                                        warning = 'Pub date more exact than title date'
                        if not warning and ISFDBdaysFromToday(value) > MAX_FUTURE_DAYS:
                                warning = 'Date more than %d days in the future' % MAX_FUTURE_DAYS

                elif Label == 'Isbn':
                        warning = CheckISBN(value, XmlData)
                        if not warning and value and not cloningFlag(XmlData):
                                warning = DuplicateISBN(value)

                elif Label == 'Catalog':
                        if value and not cloningFlag(XmlData):
                                warning = DuplicateCatalogId(value)

                elif Label == 'Binding':
                        if value and (value not in FORMATS):
                                warning = 'Uncommon format'
                        elif value == 'unknown':
                                warning = 'Format is "unknown"'
                        elif value == 'ebook':
                                pub_date = GetElementValue(XmlData, 'Year')
                                if Compare2Dates(pub_date, '2000-01-01') == 1:
                                        warning = 'Pre-2000 e-book submitted'

                elif Label in ('TitleNote', 'Note', 'Synopsis'):
                        warnings = []
                        warnings.append(ui.invalidHtmlInNotes(value))
                        warnings.append(ui.mismatchedBraces(value))
                        warnings.append(ui.unrecognizedTemplate(value))
                        for match in warnings:
                                if not match:
                                        continue
                                if warning:
                                        warning += '. %s' % match
                                else:
                                        warning = match
                        value = FormatNote(value, '', 'edit')

                elif Label == 'Series':
                        (value, warning) = CheckSeries(value)
                
                elif Label == 'Title':
                        if title and value != title[TITLE_TITLE]:
                                # This should only happen with Web API submissions
                                # because regular AddPub submissions default the pub
                                # title to the title title and do not allow title editing
                                warning = 'Pub title doesn\'t match the Title title'
                        if ui.goodHtmlTagsPresent(value):
                                warning = 'HTML tag(s) in title'
                               
		PrintField2Columns(Label, 1, value, warning)

        else:
		PrintField2Columns(Label, 0, 0, warning)


###########################################################
# These routines show current value / changed value 
# side-by-side
###########################################################

def PrintField2(Label, value, Changed, ExistsNow, Current, warning = '', warning_column = 0, warning_class = 'warn'):
        (unknown, pseudonym, disambig) = 0, 0, 0
        if Label in ('Artists', 'Authors', 'Book Authors', 'Reviewers', 'Interviewees', 'Interviewers'):
                display_author = 1
        else:
                display_author = 0
        print '<tr>'
        PrintLabel(Label)
        if Changed:
                print '<td class="drop">'
                if ExistsNow:
                        if display_author:
                                names = Current.split('+')
                                PrintAuthorNames(names, '+')
                        else:
                                print Current
                else:
                        print "-"
                print "</td>"
                print '<td class="keep">'
                if display_author:
                        names = value.split('+')
                        (unknown, pseudonym, disambig) = PrintAuthorNames(names, '+')
                else:
                        print value
                print "</td>"
                # If the editor is trying to change a "container" title type, display a warning
                if Label == 'Type' and (value != Current):
                        if Current in ('ANTHOLOGY', 'COLLECTION', 'CHAPBOOK', 'EDITOR', 'OMNIBUS'):
                                warning = 'Changed container title type'
                elif Label == 'Year':
                        if not warning and ISFDBdaysFromToday(value) > MAX_FUTURE_DAYS:
                                warning = 'Date more than %d days in the future' % MAX_FUTURE_DAYS
        else:
                print '<td class="keep">'
                if ExistsNow:
                        if display_author:
                                names = Current.split('+')
                                PrintAuthorNames(names, '+')
                        else:
                                print Current
                else:
                        print "-"
                print "</td>"
                print '<td class="drop">'
                print "-"
                print "</td>"

        if warning_column:
                if warning:
                        print '<td class="%s">%s</td>' % (warning_class, warning)
                elif display_author:
                        # Drop the last 's' in the field name
                        PrintWarning(Label[:-1], unknown, pseudonym, disambig)
                else:
                        print '<td class="blankwarning">&nbsp;</td>'
        print "</tr>"

def PrintField2XML(Label, XmlData, ExistsNow, Current, pub_id = None, suppress_diff = 0):
        ui = isfdbUI()
        value = GetElementValue(XmlData, Label)
        value2 = Current
        warning = ''
        warning_class = 'warn'
        if Label == 'Image':
                if value:
                        warning = CheckImage(value, XmlData)
                value = FormatImage(value)
                value2 = FormatImage(Current)
        elif Label in ('TitleNote', 'Note', 'Synopsis'):
                warning = ui.invalidHtmlInNotes(value)
                # If an existing note is being modified, display differences in the Warnings column
                # without using the yellow background reserved for warnings
                if not warning and not suppress_diff and value and value2:
                        from difflib import unified_diff
                        diff_generator = unified_diff(value2.splitlines(), value.splitlines(),
                                                      fromfile='before', tofile='after', n=0, lineterm='<br>')
                        for line in diff_generator:
                                if line.startswith('--- before') or line.startswith('+++ after') or line.startswith('@@ '):
                                        continue
                                warning += '<br>%s' % XMLescape(line)
                                warning_class = 'info'
                value = FormatNote(value, '', 'edit')
                value2 = FormatNote(Current, '', 'edit')
        elif Label == 'Series':
                if value2:
                        (value2, warning) = CheckSeries(value2)
                if value:
                        (value, warning) = CheckSeries(value)
                
        elif Label == 'PubSeries':
                if value2:
                        (value2, warning) = CheckPubSeries(value2)
                if value:
                        (value, warning) = CheckPubSeries(value)

        elif Label == 'Publisher':
                if value2:
                        (value2, warning) = CheckPublisher(value2)
                if value:
                        (value, warning) = CheckPublisher(value)

        elif Label == 'Price':
                if value2:
                        (value2, warning) = CheckPrice(value2)
                if value:
                        (value, warning) = CheckPrice(value)

        elif Label == 'Isbn':
                if value:
                        warning = CheckISBN(value, XmlData)
                        if not warning:
                                warning = DuplicateISBN(value, pub_id)

        elif Label == 'Catalog':
                if value and not cloningFlag(XmlData):
                        warning = DuplicateCatalogId(value)

        elif Label == 'Title':
                if ui.goodHtmlTagsPresent(value):
                        warning = 'HTML tag(s) in title'

        elif Label == 'Binding':
                if value == 'unknown':
                        warning = 'Format is "unknown"'

        elif Label == 'Year':
                if not warning and ISFDBdaysFromToday(value) > MAX_FUTURE_DAYS:
                        warning = 'Date more than %d days in the future' % MAX_FUTURE_DAYS

        if TagPresent(XmlData, Label):
		PrintField2(Label, value, 1, ExistsNow, value2, warning, 1, warning_class)
        else:
		PrintField2(Label, 0, 0, ExistsNow, value2, warning, 1, warning_class)


def PrintComparison2(Label, Proposed, Original, warning = ''):
	if Proposed:
		if Original:
			PrintField2(Label, Proposed, 1, 1, Original, warning, 1)
		else:
			PrintField2(Label, Proposed, 1, 0, '', warning, 1)
	else:
		if Original:
			PrintField2(Label, '', 0, 1, Original, warning, 1)
		else:
			PrintField2(Label, '', 0, 0, '', warning, 1)

###########################################################

def PrintComparison3(Label, XmlData, KeepId, KeepUsed, DropUsed, KeepData, DropData):
        print '<tr>'
        PrintLabel(Label)
        id = GetElementValue(XmlData, Label)
	if id == '':
		id = KeepId
        if id != KeepId:
                print '<td class="drop">'
                if KeepUsed:
                        print KeepData
                else:
                        print "-"
                print "</td>"
                print '<td class="keep">'
                if DropUsed:
                        print DropData
                else:
                        print "-"
                print "</td>"
        else:
                print '<td class="keep">'
                if KeepUsed:
                        print KeepData
                else:
                        print "-"
                print "</td>"
                print '<td class="drop">'
                if DropUsed:
                        print DropData
                else:
                        print "-"
                print "</td>"
        print "</tr>"

###########################################################

def PrintMultField1(ParentLabel, ChildLabel, Separator, Used, Current, warnings = 0):
        # Change the formatting of 'pluses' to look nicer
        if Separator == '+':
                Separator = '<span class="mergesign">+</span>'

	print '<tr>'
        PrintLabel(ParentLabel)
	print '<td class="keep">'
	if Used:
                if ParentLabel == 'Authors':
                        # Ignore warnings returned by PrintAuthorNames since the Authors logic
                        # is only used to display single column tables for Delete submissions
                        PrintAuthorNames(Current, Separator)
                else:
                        notfirst = 0
                        multfield = ''
                        for item in Current:
                                if item:
                                        multfield = BuildMultiLine(multfield, item, ParentLabel, Separator)
                                else:
                                        break
                                notfirst = 1
                        print multfield
	else:
		print "-"
	print '</td>'
	# Optionally display a warnings column
	if warnings:
		print '<td class="blankwarning">&nbsp;</td>'


def PrintMultField2XML(ParentLabel, ChildLabel, Separator, doc, XmlData):
        # Change the formatting of 'pluses' to look nicer
        if Separator == '+':
                Separator = '<span class="mergesign">+</span>'

	print '<tr>'
        PrintLabel(ParentLabel)
	value = GetElementValue(XmlData, ParentLabel)
	if value:
		print '<td class="keep">'
		children = doc.getElementsByTagName(ChildLabel)
		names = []
		for child in children:
                        names.append(child.firstChild.data.encode('iso-8859-1'))
                (unknown, pseudonym, disambig) = PrintAuthorNames(names, Separator)
		print '</td>'
		PrintWarning(ChildLabel, unknown, pseudonym, disambig)
	else:
		print '<td class="drop">-</td>'
		print '<td class="blankwarning">&nbsp;</td>'

def PrintMultFieldRaw(merge, doc, parent, child):
        value = GetElementValue(merge, parent)
        if value:
                counter = 0
                values = doc.getElementsByTagName(child)
                display = []
                for value in values:
                        data = XMLunescape(value.firstChild.data.encode('iso-8859-1'))
                        display.append(data)
                PrintMultField1(parent, child, '<br>', 1, display, 1)

def PrintAuthorNames(names, Separator):
        # Change the formatting of 'pluses' to look nicer
        if Separator == '+':
                Separator = '<span class="mergesign">+</span>'

        displayed_names = ''
        unknown = 0
        pseudonym = 0
        disambig = 0
        for name in names:
                if SQLMultipleAuthors(name):
                        disambig += 1
                author = SQLgetAuthorData(name)
                if author:
                        # If the author is already on file, change the plain text name to an HTML link to the author record
                        name = ISFDBLink('ea.cgi', author[AUTHOR_ID], author[AUTHOR_CANONICAL])
                        if SQLauthorIsPseudo(author[AUTHOR_ID]):
                                pseudonym += 1
                else:
                        unknown += 1
                
                if displayed_names == '':
                        displayed_names = name
                else:
                        displayed_names = displayed_names + Separator + name
        print displayed_names
        return (unknown, pseudonym, disambig)

def PrintWarning(Label, unknown, pseudonym, disambig, title_date = '', pub_date = ''):
        output = ''
        if unknown:
                output = 'New %s' % Label
                if unknown > 1:
                        output += 's'
        if disambig:
                if output:
                        output += ', '
                output += 'Disambiguated %s' % Label
                if disambig > 1:
                        output += "s"
        if pseudonym:
                if output:
                        output += ', '
                output += 'Alternate name'
                if pseudonym > 1:
                        output += 's'
                output += ' submitted'
        # Display a warning if the title date is after the publication date
        if title_date and pub_date and (Compare2Dates(pub_date, title_date) == 1):
                if output:
                        output += ", "
                output += 'Title date after publication date'

        if ISFDBdaysFromToday(title_date) > MAX_FUTURE_DAYS:
                if output:
                        output += ", "
                output += 'Date more than %d days in the future' % MAX_FUTURE_DAYS

        if output:
                print '<td class="warn">%s</td>' % output
        else:
                print '<td class="blankwarning">&nbsp;</td>'
        return

def BuildMultiLine(lines, newline, ParentLabel, Separator):
        if lines:
                lines += Separator
        if 'Webpages' in ParentLabel:
                lines += '<a href="%s" target="_blank">%s</a>' % (newline, newline)
        else:
                lines += newline
        return lines

def PrintMultField(ParentLabel, ChildLabel, Separator, doc, XmlData, Used, Current):
        (unknown, pseudonym, disambig) = 0, 0, 0
        if ParentLabel in ('Authors', 'BookAuthors', 'AwardAuthors', 'Interviewees', 'Artists'):
                display_author = 1
        else:
                display_author = 0
        # Change the formatting of 'pluses' to look nicer
        if Separator == '+':
                Separator = '<span class="mergesign">+</span>'
	print '<tr>'
        PrintLabel(ParentLabel)
	value = GetElementValue(XmlData, ParentLabel)
       	if value:
		print '<td class="drop">'
		if Used:
                        if display_author:
                                PrintAuthorNames(Current, Separator)
                        else:
                                multfield = ''
                                for item in Current:
                                        if item:
                                                multfield = BuildMultiLine(multfield, item, ParentLabel, Separator)
                                        else:
                                                break
                                print multfield
		else:
			print "-"
		print "</td>"
		print '<td class="keep">'
		children = doc.getElementsByTagName(ChildLabel)
                if display_author:
                        names = []
                        for child in children:
                                names.append(child.firstChild.data.encode('iso-8859-1'))
                        (unknown, pseudonym, disambig) = PrintAuthorNames(names, Separator)
                else:
                        multfield = ''
                        for child in children:
                                item = child.firstChild.data.encode('iso-8859-1')
                                multfield = BuildMultiLine(multfield, item, ParentLabel, Separator)
                        print multfield
		print "</td>"
	else:
		print '<td class="keep">'
		if Used:
                        if display_author:
                                PrintAuthorNames(Current, Separator)
                        else:
                                multfield = ''
                                for item in Current:
                                        if item:
                                                multfield = BuildMultiLine(multfield, item, ParentLabel, Separator)
                                        else:
                                                break
                                print multfield
		else:
			print "-"
		print "</td>"
		print '<td class="drop">'
		print "-"
		print "</td>"

        PrintWarning(ChildLabel, unknown, pseudonym, disambig)


def InvalidSubmission(submission_id, message = ''):
        from login import GetUserData
        print '</table>'
        error_text = 'This submission is no longer valid. %s.' % message
        print '<div id="ErrorBox">'
        submission = SQLloadSubmission(submission_id)
        submitter_id = submission[SUB_SUBMITTER]
        submitter = SQLgetUserName(submitter_id)
        print '<b>Submitted by:</b> <a href="%s://%s/index.php/User:%s">%s</a>' % (PROTOCOL, WIKILOC, submitter, submitter)
        print '<a href="%s://%s/index.php/User_Talk:%s">(Talk)</a>' % (PROTOCOL, WIKILOC, submitter)
        print '<h3>Error: %s</h3>' % error_text
        print '<h3>You can %s.' % ISFDBLink('dumpxml.cgi', submission_id, 'view the submission as raw XML')
	(userid, username, usertoken) = GetUserData()
	# If the user is a moderator and the submission is "N"ew, allow the user to hard reject it
        if SQLisUserModerator(userid) and submission[SUB_STATE] == 'N':
        	print '<br>Use %s to reject it.' % ISFDBLink('mod/hardreject.cgi', submission_id, 'Hard Reject')
        print '</h3>'
        print '</div>'
        print '</div>'
        print '</div>'
        sys.exit(0)

def PrintMerge(Label, value1, value2):
        print '<tr>'
        print '<td class="label"><b>%s</b></td>' % Label
        print '<td class="keep">%s</td>' % value1
        print '<td class="keep">%s</td>' % value2
        print '</tr>'
        return

def DisplayPublisherChanges(submission_id):
	from publisherClass import publishers

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('PublisherUpdate'):
                merge = doc.getElementsByTagName('PublisherUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print "<tr>"
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('publisher.cgi', Record, Record)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print "</tr>"

                current = publishers(db)
                current.load(int(Record))
                if not current.publisher_id:
                        InvalidSubmission(submission_id, 'This publisher no longer exists')

                PrintField2XML('Name',  merge, current.used_name,  current.publisher_name)
                PrintMultField('PublisherTransNames',   'PublisherTransName',   '<br>', doc, merge,
                               current.used_trans_names,   current.publisher_trans_names)
                PrintField2XML('Note',  merge, current.used_note,  current.publisher_note)

		PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.publisher_webpages)

        print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

	return submitter

def DisplayPubSeriesChanges(submission_id):
	from pubseriesClass import pub_series

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('PubSeriesUpdate'):
                merge = doc.getElementsByTagName('PubSeriesUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('pubseries.cgi', Record, Record)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                current = pub_series(db)
                current.load(int(Record))
                if not current.pub_series_id:
                        InvalidSubmission(submission_id, 'This publication series no longer exists')

                PrintField2XML('Name',  merge, current.used_name,  current.pub_series_name)
                PrintMultField('PubSeriesTransNames',   'PubSeriesTransName',   '<br>', doc, merge,
                               current.used_trans_names,   current.pub_series_trans_names)
                PrintField2XML('Note',  merge, current.used_note,  current.pub_series_note)

		PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.pub_series_webpages)

        print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

	return submitter


def DisplayAuthorChanges(submission_id):
	from authorClass import authors

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('AuthorUpdate'):
                merge = doc.getElementsByTagName('AuthorUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print "<tr>"
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('ea.cgi', Record, Record)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print "</tr>"

                current = authors(db)
                current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, 'This author no longer exists')

                PrintField2XML('Canonical',  merge, current.used_canonical,  current.author_canonical)
                PrintMultField('AuthorTransNames',   'AuthorTransName',   '<br>', doc, merge,
                               current.used_trans_names,   current.author_trans_names)
                PrintField2XML('Legalname',  merge, current.used_legalname,  current.author_legalname)
                PrintMultField('AuthorTransLegalNames',   'AuthorTransLegalName',   '<br>', doc, merge,
                               current.used_trans_legal_names,   current.author_trans_legal_names)
                PrintField2XML('Familyname',   merge, current.used_lastname,   current.author_lastname)
                PrintField2XML('Birthplace', merge, current.used_birthplace, current.author_birthplace)
                PrintField2XML('Birthdate',  merge, current.used_birthdate,  current.author_birthdate)
                PrintField2XML('Deathdate',  merge, current.used_deathdate,  current.author_deathdate)
                PrintField2XML('Language',   merge, current.used_language,   current.author_language)
                PrintField2XML('Image',      merge, current.used_image,      current.author_image)
                PrintMultField('Emails',   'Email',   '<br>', doc, merge, current.used_emails,   current.author_emails)
                PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.author_webpages)
                PrintField2XML('Note',      merge, current.used_note,        current.author_note)
		print '</table>'

		mod_note = GetElementValue(merge, 'ModNote')
		if mod_note:
                        print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

	return submitter
	
def DisplayAuthorMerge(submission_id):
	from authorClass import authors

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('AuthorMerge'):
		merge = doc.getElementsByTagName('AuthorMerge')
        	KeepId = GetElementValue(merge, 'KeepId')
        	DropId = GetElementValue(merge, 'DropId')
        	submitter = GetElementValue(merge, 'Submitter')

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Keepid [Record #%s]</b></td>' % ISFDBLinkNoName('ea.cgi', KeepId, KeepId)
		print '<td class="label"><b>Dropid [Record #%s]</b></td>' % ISFDBLinkNoName('ea.cgi', DropId, DropId)
                print '</tr>'

		keep = authors(db)
		keep.load(int(KeepId))
                if keep.error:
                        InvalidSubmission(submission_id, 'One of the authors no longer exists')
		drop = authors(db)
		drop.load(int(DropId))
                if drop.error:
                        InvalidSubmission(submission_id, 'One of the authors no longer exists')

		PrintComparison3('Canonical', merge, KeepId, keep.used_canonical, drop.used_canonical, 
			keep.author_canonical, drop.author_canonical)
                PrintMerge('AuthorTransNames', '<br>'.join(keep.author_trans_names), '<br>'.join(drop.author_trans_names))
		PrintComparison3('Legalname', merge, KeepId, keep.used_legalname, drop.used_legalname, 
			keep.author_legalname, drop.author_legalname)
                PrintMerge('AuthorTransLegalNames', '<br>'.join(keep.author_trans_legal_names), '<br>'.join(drop.author_trans_legal_names))
		PrintComparison3('Familyname', merge, KeepId, keep.used_lastname, drop.used_lastname, 
			keep.author_lastname, drop.author_lastname)
		PrintComparison3('Birthplace', merge, KeepId, keep.used_birthplace, drop.used_birthplace, 
			keep.author_birthplace, drop.author_birthplace)
		PrintComparison3('Birthdate', merge, KeepId, keep.used_birthdate, drop.used_birthdate, 
			keep.author_birthdate, drop.author_birthdate)
		PrintComparison3('Deathdate', merge, KeepId, keep.used_deathdate, drop.used_deathdate, 
			keep.author_deathdate, drop.author_deathdate)

                PrintMerge('Emails', '<br>'.join(keep.author_emails), '<br>'.join(drop.author_emails))
                PrintMerge('Webpages', '<br>'.join(keep.author_webpages), '<br>'.join(drop.author_webpages))
		
		PrintComparison3('Image', merge, KeepId, keep.used_image, drop.used_image, 
			keep.author_image, drop.author_image)
		PrintComparison3('Language', merge, KeepId, keep.used_language, drop.used_language, 
			keep.author_language, drop.author_language)
		PrintComparison3('Note', merge, KeepId, keep.used_note, drop.used_note, 
			keep.author_note, drop.author_note)

	print '</table>'
	print '<p>'
	return submitter

def DisplaySeriesChanges(submission_id):
	from seriesClass import series

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('SeriesUpdate'):
                merge = doc.getElementsByTagName('SeriesUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print "<tr>"
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s</b></td>' % ISFDBLinkNoName('pe.cgi', Record, Record)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print "</tr>"

                current = series(db)
                current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, 'Series no longer exists')

                PrintField2XML('Name',            merge, current.used_name,            current.series_name)
                PrintMultField('SeriesTransNames','SeriesTransName',   '<br>', doc, merge,
                               current.used_trans_names,   current.series_trans_names)
                PrintField2XML('Parent',          merge, current.used_parent,          current.series_parent)
                PrintField2XML('Parentposition',  merge, current.used_parentposition,  current.series_parentposition)
                PrintField2XML('Note',            merge, current.used_note,            current.series_note)

		PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.series_webpages)

        print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

	return submitter

def DisplayAwardLink(submission_id):
	from awardClass import awards
	from titleClass import titles
        xml = SQLloadXML(submission_id)
        print '<table border="2" class="generic_table">'
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('LinkAward'):
                merge = doc.getElementsByTagName('LinkAward')
                award_id = int(GetElementValue(merge, 'Award'))
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
                print '<td class="label"><b>%s</b></td>' % ISFDBLinkNoName('award_details.cgi', award_id, 'Award')

                award = awards(db)
                award.load(award_id)
                if award.error:
                        InvalidSubmission(submission_id, 'Award no longer exists')
                if TagPresent(merge, 'Title'):
                        title_id = int(GetElementValue(merge, 'Title'))
                        print '<td class="label">'
                        if title_id:
                                print '<b>Link Award to Title #%s</b>' % ISFDBLinkNoName('title.cgi', title_id, title_id)
                        else:
                                print '<b>Unlink Award</b>'
                        print '</td>'
                        print '</tr>'
                        title = titles(db)
                        title.load(title_id)
                        if title.error:
                                InvalidSubmission(submission_id, 'Title no longer exists')

                        PrintField2('Title', title.title_title, 1, 1, award.award_title)
                        print "<tr>"
                        print '<td class="label"><b>Authors</b></td>'
                        print '<td class="drop">'
                        notfirst = 0
                        multfield = ''
                        for author in award.award_authors:
                                if author:
                                        if notfirst:
                                                multfield += '+'
                                        multfield += author
                                else:
                                        break
                                notfirst = 1
                        print multfield
                        print "</td>"
                        print '<td class="keep">'
                        notfirst = 0
                        multfield = ''
                        for author in title.title_authors:
                                if author:
                                        if notfirst:
                                                multfield += '+'
                                        multfield += author
                                else:
                                        break
                                notfirst = 1
                        print multfield

                        PrintField2('Year', title.title_year, 1, 1, award.award_year)
                        PrintField2('Award name', '', 1, 1, award.award_type_name)
                        PrintField2('Category', '', 1, 1, award.award_cat_name)
                        PrintField2('Award level', '', 1, 1, award.award_displayed_level)
                        PrintField2('IMDB link', '', 1, 1, award.award_movie)
                        PrintField2('Note', '', 1, 1, award.award_note)

                else:
                        pass
	print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

        return submitter

def DisplayNewAwardType(submission_id):
	from awardtypeClass import award_type

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('NewAwardType'):
                merge = doc.getElementsByTagName('NewAwardType')
                submitter = GetElementValue(merge, 'Submitter')

                print "<tr>"
                print '<td class="label"><b>Short Name</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'ShortName'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Full Name</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'FullName'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Awarded For</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'AwardedFor'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Awarded By</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'AwardedBy'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Poll</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'Poll'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Non-Genre</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'NonGenre'))
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Note</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'Note'))
                print "</tr>"

                pagestring = ''
                value = GetElementValue(merge, 'Webpages')
                if value:
                        counter = 0
                        webpages = doc.getElementsByTagName('Webpage')
                        display = []
                        for webpage in webpages:
                                data = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                display.append(data)
                        PrintMultField1('Webpages', 'Webpage', '<br>', 1, display)

	print '</table>'

	return submitter

def DisplayAwardTypeChanges(submission_id):
	from awardtypeClass import award_type

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('AwardTypeUpdate'):
                merge = doc.getElementsByTagName('AwardTypeUpdate')

                current = award_type()
                current.award_type_id = GetElementValue(merge, 'AwardTypeId')
                current.load()
                if current.error:
                        InvalidSubmission(submission_id, 'Award Type no longer exists')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('awardtype.cgi', current.award_type_id, current.award_type_id)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                PrintField2XML('ShortName',         merge, current.used_short_name, current.award_type_short_name)
                PrintField2XML('FullName',          merge, current.used_name,       current.award_type_name)
                PrintField2XML('AwardedBy',         merge, current.used_by,         current.award_type_by)
                PrintField2XML('AwardedFor',        merge, current.used_for,        current.award_type_for)
                PrintField2XML('Poll',              merge, current.used_poll,       current.award_type_poll)
                PrintField2XML('NonGenre',          merge, current.used_non_genre,  current.award_type_non_genre)
                PrintField2XML('Note',              merge, current.used_note,       current.award_type_note)

		PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.award_type_webpages)

        print '</table>'
	return submitter

def DisplayAwardTypeDelete(submission_id):
	from awardtypeClass import award_type

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
        if doc.getElementsByTagName('AwardTypeDelete'):
		delete = doc.getElementsByTagName('AwardTypeDelete')
        	AwardTypeId = int(GetElementValue(delete, 'AwardTypeId'))
        	submitter = GetElementValue(delete, 'Submitter')
        	reason = GetElementValue(delete, 'Reason')

		current = award_type()
		current.award_type_id = AwardTypeId
		current.load()
                if current.error:
                        InvalidSubmission(submission_id, 'Award Type no longer exists')

                print '<p>'
                print '<table border="2" class="generic_table">'
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: %s</b></td>' % ISFDBLinkNoName('awardtype.cgi', AwardTypeId, AwardTypeId)
		print '</tr>'

		PrintField1('Short Name',    current.used_short_name, current.award_type_short_name)
		PrintField1('Full Name',     current.used_name,       current.award_type_name)
		PrintField1('Awarded For',   current.used_for,        current.award_type_for)
		PrintField1('Awarded By',    current.used_by,         current.award_type_by)
		PrintField1('Poll',          current.used_poll,       current.award_type_poll)
		PrintField1('NonGenre',      current.used_non_genre,  current.award_type_non_genre)
		PrintMultField1('WebPages', 'Web page', '<br>', current.used_webpages, current.award_type_webpages)
		PrintField1('Note',          current.used_note,       current.award_type_note)
		PrintField1('Deletion Reason', 1, reason)

        	print '</table>'

        return submitter

def DisplayNewLanguage(submission_id):
	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('NewLanguage'):
                merge = doc.getElementsByTagName('NewLanguage')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Language Name</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'LanguageName')
                print '</tr>'

                print '<tr>'
                print '<td class="label"><b>Language Code</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'LanguageCode')
                print '</tr>'

                print '<tr>'
                print '<td class="label"><b>Latin-Derived</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'Latin')
                print '</tr>'
	print '</table>'

	return submitter

def DisplayNewAwardCat(submission_id):
	from awardcatClass import award_cat
	from awardtypeClass import award_type

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('NewAwardCat'):
                merge = doc.getElementsByTagName('NewAwardCat')
                submitter = GetElementValue(merge, 'Submitter')

                print "<tr>"
                print '<td class="label"><b>Category Name</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'AwardCatName')
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Award Type</b></td>'
                awardType = award_type()
                awardType.award_type_id = GetElementValue(merge, 'AwardTypeId')
                awardType.load()
                print '<td class="keep">%s</td>' % awardType.award_type_short_name
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Display Order</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'DisplayOrder')
                print "</tr>"

                print "<tr>"
                print '<td class="label"><b>Note</b></td>'
                print '<td class="keep">%s</td>' % (GetElementValue(merge, 'Note'))
                print "</tr>"

                pagestring = ''
                value = GetElementValue(merge, 'Webpages')
                if value:
                        counter = 0
                        webpages = doc.getElementsByTagName('Webpage')
                        display = []
                        for webpage in webpages:
                                data = XMLunescape(webpage.firstChild.data.encode('iso-8859-1'))
                                display.append(data)
                        PrintMultField1('Webpages', 'Webpage', '<br>', 1, display)

	print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

	return submitter

def DisplayAwardCatDelete(submission_id):
	from awardcatClass import award_cat
	from awardtypeClass import award_type

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
        if doc.getElementsByTagName('AwardCategoryDelete'):
		delete = doc.getElementsByTagName('AwardCategoryDelete')
        	AwardCatId = int(GetElementValue(delete, 'AwardCategoryId'))
        	submitter = GetElementValue(delete, 'Submitter')
        	reason = GetElementValue(delete, 'Reason')

		current = award_cat()
		current.award_cat_id = AwardCatId
		current.load()
                if current.error:
                        InvalidSubmission(submission_id, 'Award Category no longer exists')

                print '<p>'
                print '<table border="2" class="generic_table">'
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: %s</b></td>' % ISFDBLinkNoName('award_category.cgi', '%d+1' % AwardCatId, AwardCatId)
		print '</tr>'

		PrintField1('Category Name', current.used_cat_name, current.award_cat_name)

		awardType = award_type()
		awardType.award_type_id = current.award_cat_type_id
		awardType.load()
                if awardType.error:
                        InvalidSubmission(submission_id, 'Award Type no longer exists')

		PrintField1('Award Type', awardType.used_name, awardType.award_type_name)
		PrintField1('Display Order', current.used_cat_order, current.award_cat_order)
		PrintMultField1('WebPages', 'Web page', '<br>', current.used_webpages, current.award_cat_webpages)
		PrintField1('Note',          current.used_note,       current.award_cat_note)
		PrintField1('Deletion Reason', 1, reason)

        	print '</table>'

        return submitter

def DisplayAwardCatChanges(submission_id):
	from awardcatClass import award_cat

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('AwardCategoryUpdate'):
                merge = doc.getElementsByTagName('AwardCategoryUpdate')

                current = award_cat()
                current.award_cat_id = GetElementValue(merge, 'AwardCategoryId')
                current.load()
                if current.error:
                        InvalidSubmission(submission_id, 'Award Category no longer exists')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('award_category.cgi', current.award_cat_id, current.award_cat_id)
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                PrintField2XML('CategoryName',         merge, current.used_cat_name,  current.award_cat_name)
                PrintField2XML('DisplayOrder',         merge, current.used_cat_order, current.award_cat_order)
                PrintField2XML('Note',                 merge, current.used_note,      current.award_cat_note)
		PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.award_cat_webpages)

        print '</table>'
	return submitter

def DisplaySeriesDelete(submission_id):
	from seriesClass import series

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('SeriesDelete'):
		delete = doc.getElementsByTagName('SeriesDelete')
        	Record = GetElementValue(delete, 'Record')
        	reason = GetElementValue(delete, 'Reason')
        	submitter = GetElementValue(delete, 'Submitter')

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: #%s</b></td>' % (Record)
		print '</tr>'

                #Check if the series has already been deleted
                seriesRecord = SQLget1Series(int(Record))
                if seriesRecord == 0:
                        InvalidSubmission(submission_id, 'This series no longer exists')

                # Check if sub-series have been added to this series since the time the submission was created
                subseries = SQLFindSeriesChildren(int(Record))
                if len(subseries) > 0:
                        InvalidSubmission(submission_id, 'At least one sub-series has been added to this Series since the time this submission was created. This series can\'t be deleted until all sub-series have been removed')

                # Check if titles have been added to this series since the time the submission was created
                titles = SQLloadTitlesXBS(int(Record))
                if len(titles) > 0:
                        InvalidSubmission(submission_id, 'At least one title has been added to this series since the time this submission was created. This series can\'t be deleted until all titles have been removed')

		current = series(db)
		current.load(int(Record))

		PrintField1('Series',       current.used_name,        current.series_name)
		PrintMultField1('SeriesTransNames', 'SeriesTransName', '<br>', current.used_trans_names, current.series_trans_names)
		PrintField1('Parent',       current.used_parent,      current.series_parent)
                PrintField1('Parent Position',  current.used_parentposition,  current.series_parentposition)
		PrintMultField1('Webpages', 'Web page', '<br>', current.used_webpages, current.series_webpages)
                PrintField1('Note',         current.used_note,        current.series_note)

        print '</table>'
        print '<br><b>Reason for deletion:</b> %s<br>' % reason

        return submitter

def DisplayTitleEdit(submission_id):
	from titleClass import titles

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('TitleUpdate'):
                merge = doc.getElementsByTagName('TitleUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')
        
                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
                print '<td class="label"><b>Current [Record #%s]</b></td>' % ISFDBLinkNoName('title.cgi', Record, Record)	
                print '<td class="label"><b>Proposed Changes</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                current = titles(db)
                current.load(int(Record))
                if not current.used_id:
                        InvalidSubmission(submission_id, 'The title no longer exists in the database')

                PrintField2XML('Title',     merge, current.used_title,     current.title_title)
                PrintMultField('TranslitTitles',   'TranslitTitle',   '<br>', doc, merge,
                               current.used_trans_titles,   current.title_trans_titles)

                if current.title_ttype == 'REVIEW':
                        PrintMultField('Authors', 'Author', '+', doc, merge, current.num_authors, current.title_authors)
                        PrintMultField('BookAuthors', 'BookAuthor', '+', doc, merge, current.num_subjauthors, current.title_subjauthors)
                elif current.title_ttype == 'INTERVIEW':
                        PrintMultField('Authors', 'Author', '+', doc, merge, current.num_authors, current.title_authors)
                        PrintMultField('Interviewees', 'Interviewee', '+', doc, merge, current.num_subjauthors, current.title_subjauthors)
                else:
                        PrintMultField('Authors', 'Author', '+', doc, merge, current.num_authors, current.title_authors)

                PrintField2XML('Year',      merge, current.used_year,      current.title_year)
                PrintField2XML('Synopsis',  merge, current.used_synop,     current.title_synop)
                PrintField2XML('Series',    merge, current.used_series,    current.title_series)
                PrintField2XML('Seriesnum', merge, current.used_seriesnum, current.title_seriesnum)
                PrintField2XML('TitleType', merge, current.used_ttype,     current.title_ttype)
                PrintField2XML('Storylen',  merge, current.used_storylen,  current.title_storylen)
                PrintField2XML('ContentIndicator',  merge, current.used_content,  current.title_content)
                PrintField2XML('NonGenre',  merge, current.used_non_genre, current.title_non_genre)
                PrintField2XML('Juvenile',  merge, current.used_jvn,       current.title_jvn)
                PrintField2XML('Novelization', merge, current.used_nvz,    current.title_nvz)
                PrintField2XML('Graphic',   merge, current.used_graphic,   current.title_graphic)
                PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.title_webpages)
                PrintField2XML('Language',  merge, current.used_language,  current.title_language)
                PrintField2XML('Note',      merge, current.used_note,      current.title_note)

                print '</table>'
                mod_note = GetElementValue(merge, 'ModNote')
                if mod_note:
                        print '<h3>Note to Moderator: </h3>%s<p><p>' % mod_note
                # Get all publications for this title (but not its parent)
                pubs = SQLGetPubsByTitleNoParent(int(Record))
                if not len(pubs):
                        print '<br>There are no publications associated with this title.'
                        print '<br>'
                else:
                        print '<br>This title appears in %d publications:' % len(pubs)
                        DisplayPubsForTitle(pubs)
                # Get all publications for this title's parent
                children_pubs = SQLGetPubsForChildTitles(int(Record))
                if len(children_pubs):
                        print '<br>This title\'s VARIANTS appear in %d publications:' % len(children_pubs)
                        DisplayPubsForTitle(children_pubs)

        return submitter

def DisplayPubsForTitle(pub_list):
        print '<table border="1">'
        print '<tr>'
        print '<th>Publication</th>'
        print '<th>Verification Type</th>'
        print '<th>Primary Verifiers</th>'
        print '</tr>'
        for pub in pub_list:
                print '<tr>'
                print '<td>%s (%s)</td>' % (ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE]), pub[PUB_YEAR])
                verificationstatus = SQLVerificationStatus(pub[PUB_PUBID])
                if verificationstatus == 1:
                        print '<td class="warn">Primary</td>'
                        print '<td>'
                        verifiers = SQLPrimaryVerifiers(pub[PUB_PUBID])
                        for verifier in verifiers:
                                print '<a href="%s://%s/index.php/User:%s">%s</a><br>' % (PROTOCOL, WIKILOC, verifier[1], verifier[1])
                        print '</td>'                                
                elif verificationstatus == 2:
                        print '<td>Secondary</td>'
                        print '<td></td>'
                else:
                        print '<td>Not verified</td>'
                        print '<td></td>'
        print '</table>'


def DisplayTitleDelete(submission_id):
	from titleClass import titles

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
	reviews = []
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('TitleDelete'):
		delete = doc.getElementsByTagName('TitleDelete')
        	Record = GetElementValue(delete, 'Record')
        	reason = GetElementValue(delete, 'Reason')
        	submitter = GetElementValue(delete, 'Submitter')
        	reviews = SQLloadTitleReviews(int(Record))

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: %s</b></td>'  % ISFDBLinkNoName('title.cgi', Record, Record)	
		print '</tr>'

		current = titles(db)
		current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, 'This title no longer exists')

		PrintField1('Title',      current.used_title,     current.title_title)
		PrintMultField1('TransliteratedTitles', 'TransliteratedTitle', '<br>', current.used_trans_titles, current.title_trans_titles)
		PrintField1('Year',       current.used_year,      current.title_year)
		PrintField1('Synopsis',   current.used_synop,     current.title_synop)
		PrintField1('Series',     current.used_series,    current.title_series)
		PrintField1('Seriesnum',  current.used_seriesnum, current.title_seriesnum)
		PrintField1('TitleType',  current.used_ttype,     current.title_ttype)
		PrintField1('Storylen',   current.used_storylen,  current.title_storylen)
		PrintField1('ContentIndicator', current.used_content, current.title_content)
		PrintField1('NonGenre',   current.used_non_genre, current.title_non_genre)
		PrintField1('Juvenile',   current.used_jvn,       current.title_jvn)
		PrintField1('Novelization', current.used_nvz,     current.title_nvz)
		PrintField1('Graphic',    current.used_graphic,   current.title_graphic)

		PrintMultField1('Webpages', 'Web page', '<br>', current.used_webpages, current.title_webpages)
		PrintMultField1('Authors',  'Author',   '+', current.num_authors,   current.title_authors)
		PrintField1('Language',   current.used_language,  current.title_language)
		PrintField1('Note',       current.used_note,      current.title_note)

        print '</table>'
        print '<br><b>Reason for deletion:</b> %s<br>' % reason

	if reviews:
        	print '<p><div id="WarningBox">'
                print '<br><b>Reviews of this title:</b>'
                print '<ul>'
                for review in reviews:
                        print '<li>%s' % ISFDBLinkNoName('title.cgi', review[0], review[0])
                print '</ul>'
                print '</div>'
        print '<p>'

        return submitter

def DisplayNewAward(submission_id):
        
	xmlData = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xmlData))

        print '<table border="2" class="generic_table">'
        submitter = ''
        if doc.getElementsByTagName('NewAward'):
                merge = doc.getElementsByTagName('NewAward')
                submitter = GetElementValue(merge, 'Submitter')
                austring = ''

                if TagPresent(merge, 'Record'):
                        Record = GetElementValue(merge, 'Record')
                        title = SQLloadTitle(int(Record))
                        if not title:
                                InvalidSubmission(submission_id, 'Title no longer exists')
                        print '<tr>'
                        print '<td class="label"><b>Add Award to %s</a></b></td>' % ISFDBLinkNoName('title.cgi', Record, 'Title #%s' % Record, True)
                        print '<td class="label">%s</td>' % (title[TITLE_TITLE])
                        print '</tr>'
                        print '<tr>'
                        print '<td class="label">Award Title</td>'
                        print '<td class="keep">%s</td>' % (title[TITLE_TITLE])
                        print '</tr>'
                        authors = SQLTitleAuthors(int(Record))
                        counter = 0
                        for author in authors:
                                if counter:
                                        austring +=  "+"
                                austring += author
                                counter += 1

                else:
                        AwardTitle = GetElementValue(merge, 'AwardTitle')
                        print '<tr>'
                        print '<td class="label">Award Title</td>'
                        print '<td class="keep">%s</td>' % (AwardTitle)
                        print '</tr>'
                        value = GetElementValue(merge, 'AwardAuthors')
                        if value:
                                counter = 0
                                authors = doc.getElementsByTagName('AwardAuthor')
                                for author in authors:
                                        data = XMLunescape(author.firstChild.data.encode('iso-8859-1'))
                                        if counter:
                                                austring +=  "+"
                                        austring += data
                                        counter += 1

                print '<tr>'
                print '<td class="label">Award Authors</td>'
                print '<td class="keep">%s</td>' % (austring)
                print '</tr>'


                award_type_id = GetElementValue(merge, 'AwardType')
                award_type = SQLGetAwardTypeById(award_type_id)
                award_type_name = award_type[AWARD_TYPE_NAME]
                print '<tr>'
                print '<td class="label">Award Type</td>'
                print '<td class="keep">%s</td>' % (award_type_name)
                print '</tr>'

                AwardYear = GetElementValue(merge, 'AwardYear')
                print '<tr>'
                print '<td class="label">Award Year</td>'
                print '<td class="keep">%s</td>' % (AwardYear)
                print '</tr>'

                AwardCategoryId = GetElementValue(merge, 'AwardCategory')
                print '<tr>'
                print '<td class="label">Award Category</td>'
                AwardCategoryName = SQLGetAwardCatById(AwardCategoryId)[AWARD_CAT_NAME]
                print '<td class="keep">%s</td>' % (AwardCategoryName)
                print '</tr>'

                AwardLevel = GetElementValue(merge, 'AwardLevel')
                print '<tr>'
                print '<td class="label">Award Level</td>'
                print '<td class="keep">%s</td>' % (AwardLevelDescription(AwardLevel, award_type[AWARD_TYPE_ID]))
                print '</tr>'

                AwardMovie = GetElementValue(merge, 'AwardMovie')
                print '<tr>'
                print '<td class="label">Award Movie</td>'
                print '<td class="keep">%s</td>' % (AwardMovie)
                print '</tr>'

                AwardNote = GetElementValue(merge, 'AwardNote')
                print '<tr>'
                print '<td class="label">Award Note</td>'
                print '<td class="keep">%s</td>' % (AwardNote)
                print '</tr>'

	print '</table>'
        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note != '': 
                print '<h3>Note to Moderator: </h3>%s<p><p>' % mod_note

	return submitter

def DisplayAwardEdit(submission_id):
        from awardClass import awards

	xmlData = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xmlData))

        print '<table border="2" class="generic_table">'
        submitter = ''
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('AwardUpdate'):
                merge = doc.getElementsByTagName('AwardUpdate')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
                print '<td class="label"><b>Current [Record #%s]</b></td>' % (Record)
                print '<td class="label"><b>Proposed Changes</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                current = awards(db)
                current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, current.error)

                PrintField2XML('AwardTitle',    merge, current.used_title, current.award_title)
                PrintField2XML('AwardYear',     merge, current.used_year,  current.award_year)

                # Check if the award code has changed and, if so, retrieve its name
                if TagPresent(merge, 'AwardType'):
                        award_type_id = GetElementValue(merge, 'AwardType')
                        award_type = SQLGetAwardTypeById(award_type_id)
                        award_type_name = award_type[AWARD_TYPE_NAME]
                        PrintField2('AwardType', award_type_name, 1, 1, current.award_type_name, None, 1)
                else:
                        PrintField2('AwardType', '', 0, 1, current.award_type_name, None, 1)
                        award_type_id = current.award_type_id

                # Check if the award category has changed and, if so, retrieve its name
                if TagPresent(merge, 'AwardCategory'):
                        award_cat_id = GetElementValue(merge, 'AwardCategory')
                        award_cat = SQLGetAwardCatById(award_cat_id)
                        award_cat_name = award_cat[AWARD_CAT_NAME]
                        PrintField2('AwardCategory', award_cat_name, 1, 1, current.award_cat_name, None, 1)
                else:
                        PrintField2('AwardCategory', '', 0, 1, current.award_cat_name, None, 1)
                        award_cat_id = current.award_cat_id

                # Retrieve the award level name
                current_level_desc = AwardLevelDescription(current.award_level, current.award_type_id)

                if TagPresent(merge, 'AwardLevel'):
                        new_level = GetElementValue(merge, 'AwardLevel')
                        award_type = SQLGetAwardTypeById(award_type_id)
                        new_level_desc = AwardLevelDescription(new_level, award_type[AWARD_TYPE_ID])
                        PrintField2('AwardLevel', new_level_desc, 1, 1, current_level_desc, None, 1)
                else:
                        PrintField2('AwardLevel', '', 0, 1, current_level_desc, None, 1)

                PrintField2XML('AwardMovie',    merge, current.used_movie, current.award_movie)

                PrintMultField('AwardAuthors', 'AwardAuthor', '+', doc, merge, current.num_authors, current.award_authors)

                PrintField2XML('AwardNote',    merge, current.used_note, current.award_note)

	print '</table>'
        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note != '': 
                print '<h3>Note to Moderator: </h3>%s<p><p>' % mod_note

        return submitter

def DisplayAwardDelete(submission_id):
        from awardClass import awards

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
        if doc.getElementsByTagName('AwardDelete'):
		delete = doc.getElementsByTagName('AwardDelete')
        	Record = GetElementValue(delete, 'Record')
        	submitter = GetElementValue(delete, 'Submitter')
        	reason = GetElementValue(delete, 'Reason')

		current = awards(db)
		current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, current.error)

                if current.title_id:
                        print '<h3>This submission deletes an award for Title record #%s</h3>' % ISFDBLinkNoName('title.cgi', current.title_id, current.title_id)
                else:
                        print '<h3>This award is not associated with an ISFDB title</h3>'
                print '<p>'
                print '<table border="2" class="generic_table">'
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: #%s</b></td>' % (Record)
		print '</tr>'

		PrintField1('Title',    current.used_title, current.award_title)
		PrintField1('Year',     current.used_year,  current.award_year)
		PrintField1('Type',	current.used_type_name, current.award_type_name)
		PrintField1('Category', current.used_cat_name, current.award_cat_name)
		PrintField1('Level',    current.used_level, AwardLevelDescription(current.award_level, current.award_type_id))
		PrintField1('IMDB Title',    current.used_movie, current.award_movie)
		PrintMultField1('Authors', 'Author', '+', current.num_authors, current.award_authors)
		PrintField1('Note',    current.used_note, current.award_note)

                print '</table>'
                print '<br><b>Reason for deletion:</b> %s<br>' % reason

        return submitter

def DisplayLinkReview(submission_id):
        from titleClass import titles

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        if doc.getElementsByTagName('LinkReview'):
                merge = doc.getElementsByTagName('LinkReview')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<table border="2" class="generic_table">'
                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
                print '<td class="label"><b>Review [Record #%s]</b></td>' % ISFDBLink('title.cgi', Record, Record)

                theReview = titles(db)
                theReview.load(int(Record))
                if theReview.error:
                        InvalidSubmission(submission_id, theReview.error)
                if TagPresent(merge, 'Parent'):
                        parent = GetElementValue(merge, 'Parent')
                        print '<td class="label"><b>Link Review to [Title #%s]</b></td>' % ISFDBLink('title.cgi', parent, parent)
                        print '</tr>'
                        reviewedTitle = titles(db)
                        reviewedTitle.load(int(parent))
                        if reviewedTitle.error:
                                InvalidSubmission(submission_id, reviewedTitle.error)

                        PrintField2('Title', reviewedTitle.title_title, 1, 1, theReview.title_title)
                        PrintField2('Year', reviewedTitle.title_year, 1, 1, theReview.title_year)
                        PrintField2('TitleType', reviewedTitle.title_ttype, 1, 1, theReview.title_ttype)

                        ###################################
                        # Book Authors
                        ###################################
                        print '<tr>'
                        print '<td class="label"><b>Book Authors</b></td>'
                        print '<td class="drop">'
                        notfirst = 0
                        multfield = ''
                        for author in theReview.title_subjauthors:
                                if author:
                                        if notfirst:
                                                multfield += '+'
                                        multfield += author
                                else:
                                        break
                                notfirst = 1
                        print multfield
                        print '</td>'
                        print '<td class="keep">'
                        notfirst = 0
                        multfield = ''
                        for author in reviewedTitle.title_authors:
                                if author:
                                        if notfirst:
                                                multfield += '+'
                                        multfield += author
                                else:
                                        break
                                notfirst = 1
                        print multfield
                        print '</td>'

                        ###################################
                        # Reviewer
                        ###################################
                        print '<tr>'
                        print '<td class="label"><b>Reviewers</b></td>'
                        print '<td class="drop">'
                        notfirst = 0
                        multfield = ''
                        for author in theReview.title_authors:
                                if author:
                                        if notfirst:
                                                multfield += '+'
                                        multfield += author
                                else:
                                        break
                                notfirst = 1
                        print multfield
                        print '</td>'
                        print '<td class="keep">'
                        print ' - '
                        print '</td>'

                        print '<tr>'
                        print '<td class="label"><b>Language</b></td>'
                        print '<td class="drop">'
                        if theReview.title_language:
                                print theReview.title_language
                        else:
                                print ' - '
                        print '</td>'

                        print '<td class="keep">'
                        if reviewedTitle.title_language:
                                print reviewedTitle.title_language
                        else:
                                print ' - '
                        print '</td>'
                        print '</tr>'
                else:
                        pass
                print '</table>'
                mod_note = GetElementValue(merge, 'ModNote')
                if mod_note: 
                        print '<h3>Note to Moderator: </h3>%s<p><p>' % mod_note

        return submitter

def DisplayPublisherMerge(submission_id):
        from publisherClass import publishers

        KeepId    = 0
        Records   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        RecordIds = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        MaxIds    = 1

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        if doc.getElementsByTagName('PublisherMerge'):
		try:
			Document = doc.getElementsByTagName('PublisherMerge')
        		KeepId = int(GetElementValue(Document, 'KeepId'))
        		submitter = GetElementValue(Document, 'Submitter')
		except:
			InvalidSubmission(submission_id, 'Missing Required XML tags')

                print '<table border="2" class="generic_table">'
		RecordIds[0] = KeepId
		dropIds = doc.getElementsByTagName('DropId')
		for dropid in dropIds:
			RecordIds[MaxIds] = int(dropid.firstChild.data)
			MaxIds += 1

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>KeepId %s</b></td>' % ISFDBLinkNoName('publisher.cgi', KeepId, KeepId, True)
	
		index = 1
		while RecordIds[index]:
			print '<td class="label"><b>DropId %s</b></td>' % ISFDBLinkNoName('publisher.cgi', RecordIds[index], RecordIds[index], True)
			index += 1
		print '</tr>'

		try:
			Records[0] = publishers(db)
			Records[0].load(RecordIds[0])
			if Records[0].error:
                                raise
		except:
			InvalidSubmission(submission_id, "Can't load record: %s" % KeepId)

		index = 1
		while RecordIds[index]:
			try:
				Records[index] = publishers(db)
				Records[index].load(RecordIds[index])
                                if Records[index].error:
                                        raise
			except:
				InvalidSubmission(submission_id, "Can't load record: %s" % RecordIds[index])
			index += 1

		PrintPublisherMerge('Publisher', Document, KeepId, Records, RecordIds)
		PrintPublisherMerge('Trans_names', Document, KeepId, Records, RecordIds)
		PrintPublisherMerge('Webpages', Document, KeepId, Records, RecordIds)
		PrintPublisherMerge('Note', Document, KeepId, Records, RecordIds)

                print '</table>'
        
        return submitter

def PrintPublisherMerge(Label, XmlData, KeepId, Records, RecordIds):
	print "<tr>"
	print '<td class="label"><b>' +Label+ '</b></td>'
	try:
		keepId = int(GetElementValue(XmlData, Label))
	except:
		keepId = KeepId

	index = 0
	while Records[index]:
		if (RecordIds[index] == keepId) or (Label == 'Webpages') or (Label == 'Trans_names'):
			print '<td class="keep">'
		else:
			print '<td class="drop">'

		if Label == 'Publisher':
			if Records[index].used_name:
				print Records[index].publisher_name
			else:
				print "-"
		elif Label == 'Trans_names':
			if Records[index].used_trans_names:
				print '<br>'.join(Records[index].publisher_trans_names)
			else:
				print "-"
		elif Label == 'Webpages':
			if Records[index].used_webpages:
				print '<br>'.join(Records[index].publisher_webpages)
			else:
				print "-"
		elif Label == 'Note':
			if Records[index].used_note:
				print Records[index].publisher_note
			else:
				print "-"
		print "</td>"
		index += 1
	print "</tr>"

def DisplayMakePseudonym(submission_id):
	submitter = ''
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('MakePseudonym'):
                merge = doc.getElementsByTagName('MakePseudonym')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<table border="2" class="generic_table">'
                print '<tr>'
                print '<td class="label"><b>Alternate Name Record %s</b></td>' % ISFDBLinkNoName('ea.cgi', Record, Record, True)

                if TagPresent(merge, 'Parent'):
                        parent = GetElementValue(merge, 'Parent')
                        print '<td class="label"><b>Parent Author Record %s</b></td>' % ISFDBLinkNoName('ea.cgi', parent, parent, True)
                        print '</tr>'

                        print '<tr>'
                        try:
                                author = SQLloadAuthorData(int(Record))
                                print '<td class="drop">%s</td>' % (author[AUTHOR_CANONICAL])
                        except:
                                InvalidSubmission(submission_id, "Alternate name not found: %d" % int(Record))
                        try:
                                author = SQLloadAuthorData(int(parent))
                                print '<td class="keep">%s</td>' % (author[AUTHOR_CANONICAL])
                        except:
                                InvalidSubmission(submission_id, "Parent author not found: %d" % int(parent))
                        print '</tr>'
                print '</table>'
                mod_note = GetElementValue(merge, 'ModNote')
                if mod_note:
                        print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        duplicate = ''
	other_authors = SQLgetActualFromPseudo(int(Record))
	if other_authors:
		print 'This name is currently labeled as an alternate name for the following authors:'
		print '<ul>'
                for other_author in other_authors:
                        other_author_data = SQLgetAuthorData(other_author[0])
			print '<li>%s' % ISFDBLink('ea.cgi', other_author_data[AUTHOR_ID], other_author[0])
			if int(parent) == int(other_author_data[AUTHOR_ID]):
                                duplicate = other_author_data[AUTHOR_CANONICAL]
		print '</ul>'
	if duplicate:
                InvalidSubmission(submission_id, 'This author record is already set up as an alternate name of %s' % duplicate)

        return submitter

def DisplayRemovePseudonym(submission_id):
	submitter = ''
        print '<table border="2" class="generic_table">'
	try:
		xml = SQLloadXML(submission_id)
		doc = minidom.parseString(XMLunescape2(xml))
        	if doc.getElementsByTagName('RemovePseud'):
			merge = doc.getElementsByTagName('RemovePseud')
        		Record = GetElementValue(merge, 'Record')
        		submitter = GetElementValue(merge, 'Submitter')
	
			print '<tr>'
			print '<td class="label"><b>Alternate Name %s</b></td>' % ISFDBLinkNoName('ea.cgi', Record, 'Record #%s' % Record, True)
	
       			if TagPresent(merge, 'Parent'):
        			parent = GetElementValue(merge, 'Parent')
                                print '<td class="label"><b>Parent Author %s</b></td>' % ISFDBLinkNoName('ea.cgi', parent, 'Record #%s' % parent, True)
				print '</tr>'

				print '<tr>'
				try:
					author = SQLloadAuthorData(int(Record))
					print '<td class="drop">%s</td>' % (author[AUTHOR_CANONICAL])
				except:
                                        InvalidSubmission(submission_id, 'Alternate name record no longer exists')
				try:
					author = SQLloadAuthorData(int(parent))
					print '<td class="keep">%s</td>' % (author[AUTHOR_CANONICAL])
				except:
                                        InvalidSubmission(submission_id, 'Parent author record no longer exists')
				print '</tr>'
			else:
                                InvalidSubmission(submission_id, 'Parent record not specified')

	except:
                InvalidSubmission(submission_id)

	print '</table>'
	mod_note = GetElementValue(merge, 'ModNote')
	if mod_note:
		print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        pseud_id = SQLGetPseudIdByAuthorAndPseud(parent,Record)
        if not pseud_id:
                InvalidSubmission(submission_id, 'This alternate name association no longer exists')

	authors = SQLgetActualFromPseudo(int(Record))
	if authors:
		print 'This name is currently labeled as an alternate name for the following authors:'
		print '<ul>'
                for author in authors:
                        author_data = SQLgetAuthorData(author[0])
			print '<li>%s' % ISFDBLink('ea.cgi', author_data[AUTHOR_ID], author[0])
		print '</ul>'

        return submitter

def DisplayDeletePub(submission_id):
        from pubClass import pubs

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	reason = ''
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('PubDelete'):
		delete = doc.getElementsByTagName('PubDelete')
        	Record = GetElementValue(delete, 'Record')
        	submitter = GetElementValue(delete, 'Submitter')
        	reason = GetElementValue(delete, 'Reason')

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Record to Delete: #%s</b></td>' % ISFDBLinkNoName('pl.cgi', Record, Record)
		print '</tr>'

		current = pubs(db)
		current.load(int(Record))
		if current.error:
                        InvalidSubmission(submission_id, current.error)

		PrintField1('Title',     current.used_title,     current.pub_title)
		PrintMultField1('TransliteratedTitles', 'TransliteratedTitle', '<br>', current.used_trans_titles, current.pub_trans_titles)
		PrintMultField1('Authors', 'Author', '+', current.num_authors, current.pub_authors)
		PrintField1('Tag',       current.used_tag,       current.pub_tag)
		PrintField1('Year',      current.used_year,      current.pub_year)
		PrintField1('Publisher', current.used_publisher, current.pub_publisher)
		PrintField1('Pub. Series', current.used_series,  current.pub_series)
		PrintField1('Pub. Series #', current.used_series_num, current.pub_series_num)
		PrintField1('Pages',     current.used_pages,     current.pub_pages)
		PrintField1('Binding',   current.used_ptype,     current.pub_ptype)
		PrintField1('PubType',   current.used_ctype,     current.pub_ctype)
		PrintField1('Isbn',      current.used_isbn,      current.pub_isbn)
		PrintField1('Catalog',   current.used_catalog,   current.pub_catalog)
		PrintField1('Price',     current.used_price,     current.pub_price)
		PrintField1('Image',     current.used_image,     current.pub_image)
		PrintMultField1('Webpages', 'Web page', '<br>', current.used_webpages, current.pub_webpages)
		PrintField1('Note',      current.used_note,      current.pub_note)
		PrintDeleteExternalIDs(current)

	print '</table>'
	print '<br><b>Reason for deletion:</b>', reason
	print '<p>'

        return submitter

def DisplayRemoveTitle(submission_id):
        from pubClass import pubs
        from titleClass import titles
	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        if doc.getElementsByTagName('TitleRemove'):
		merge = doc.getElementsByTagName('TitleRemove')
		subject = GetElementValue(merge, 'Subject')
        	Record = GetElementValue(merge, 'Record')
		pub_id = int(Record)
        	submitter = GetElementValue(merge, 'Submitter')

		pub = pubs(db)
		pub.load(pub_id)
		if pub.error:
                        InvalidSubmission(submission_id, pub.error)

		# Add a link to existing Publication
		print 'Removing titles from %s<p>' % ISFDBLinkNoName('pl.cgi', pub_id, subject)

                DisplayVerifications(pub_id, 0)

        	# Get the list of titles in this pub and sort them by page number
        	current_contents = getPubContentList(pub_id)

        	if doc.getElementsByTagName('CoverRecord'):

			# Build a list of cover art IDs to be removed
			removalList = []
			children = doc.getElementsByTagName('CoverRecord')
			if len(children):
				for child in children:
					record = int(child.firstChild.data)
					if not TitleInPub(record, current_contents):
                                                InvalidSubmission(submission_id, 'Cover no longer in the publication')
					removalList.append(record)

                        PrintTitleRemoveHeader("Cover Art")
                        
			for item in current_contents:
                                PrintTitleRemoveOneRow(item, removalList, "COVERART")
                        
			print '</table>'

        	if doc.getElementsByTagName('TitleRecord'):

			# Build a list of regular content IDs to be removed
			removalList = []
			children = doc.getElementsByTagName('TitleRecord')
			if len(children):
				for child in children:
					record = int(child.firstChild.data)
					if not TitleInPub(record, current_contents):
                                                InvalidSubmission(submission_id, 'Title no longer in the publication')
					removalList.append(record)

                        PrintTitleRemoveHeader("Regular Titles")
                        
			for item in current_contents:
                                PrintTitleRemoveOneRow(item, removalList, "TITLE")
                        
			print '</table>'

        	if doc.getElementsByTagName('ReviewRecord'):
			# Build a list of review content IDs to be removed
			removalList = []
			children = doc.getElementsByTagName('ReviewRecord')
			if len(children):
				for child in children:
					record = int(child.firstChild.data)
					if not TitleInPub(record, current_contents):
                                                InvalidSubmission(submission_id, 'Review no longer in the publication')
					removalList.append(record)

			print '<p>'
                        PrintTitleRemoveHeader("Reviews")
                        
			for item in current_contents:
                                PrintTitleRemoveOneRow(item, removalList, "REVIEW")
                        
			print '</table>'

        	if doc.getElementsByTagName('InterviewRecord'):
			# Build a list of interview content IDs to be removed
			removalList = []
			children = doc.getElementsByTagName('InterviewRecord')
			if len(children):
				for child in children:
					record = int(child.firstChild.data)
					if not TitleInPub(record, current_contents):
                                                InvalidSubmission(submission_id, 'Interview no longer in the publication')
					removalList.append(record)

			print '<p>'
                        PrintTitleRemoveHeader("Interviews")

			for item in current_contents:
                                PrintTitleRemoveOneRow(item, removalList, "INTERVIEW")

			print '</table>'
				
                mod_note = GetElementValue(merge, 'ModNote')
                if mod_note:
                        print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        return submitter

def TitleInPub(record, current_contents):
        found = 0
        for content_item in current_contents:
                if int(content_item[PUB_CONTENTS_ID]) == record:
                        found = 1
                        break
        return found

def PrintTitleRemoveHeader(section):
        print '<h2>'
        print section
        print '</h2>'
        print '<table border="2" class="generic_table">'
        print '<tr>'
        print '<td class="label"><b>Keep</b></td>'
        print '<td class="label"><b>Drop</b></td>'
        print '</tr>'
        return

def PrintTitleRemoveOneRow(contents_item, removalList, type):
        # Get the title id of the current pub_content record
        title_id = contents_item[PUB_CONTENTS_TITLE]
        # Load the title record
        title = SQLloadTitle(title_id)
        authors = []
        if type == 'COVERART':
                if title[TITLE_TTYPE] != 'COVERART':
                        return
                authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])

        if type == 'TITLE':
                if title[TITLE_TTYPE] == 'COVERART':
                        return
                if title[TITLE_TTYPE] == 'REVIEW':
                        return
                if title[TITLE_TTYPE] == 'INTERVIEW':
                        return
                authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
        
        if type == "REVIEW":
                if title[TITLE_TTYPE] != 'REVIEW':
                        return
                authors = SQLReviewBriefAuthorRecords(title[TITLE_PUBID])

        if type == "INTERVIEW":
		if title[TITLE_TTYPE] != 'INTERVIEW':
			return
		authors = SQLInterviewBriefAuthorRecords(title[TITLE_PUBID])

        page = contents_item[PUB_CONTENTS_PAGE]
        print '<tr>'
        if contents_item[PUB_CONTENTS_ID] in removalList:
                print '<td class="drop">'
                print "-"
                print "</td>"
                print '<td class="keep">'
        	if page:
        		print '%s - ' % (str(page))
                line = '%s %s' % (ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]), title[TITLE_TTYPE])
        	for author in authors:
        		line += ', %s' % ISFDBLink('ea.cgi', author[0], author[1])
        	print line
                print "</td>"
        else:
                print '<td class="keep">'
        	if page:
        		print '%s - ' % (str(page))
                line = '%s, %s' % (ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]), title[TITLE_TTYPE])
        	for author in authors:
        		line += ', %s' % ISFDBLink('ea.cgi', author[0], author[1])
        	print line
        	print "</td>"
                print '<td class="drop">'
                print "-"
                print "</td>"
        print '</tr>'
        return

def DisplayAddVariant(submission_id):
        from titleClass import titles

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('VariantTitle'):
		merge = doc.getElementsByTagName('VariantTitle')
        	Parent = GetElementValue(merge, 'Parent')
        	submitter = GetElementValue(merge, 'Submitter')

		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current Parent #%s</b></td>' % ISFDBLinkNoName('title.cgi', Parent, Parent, True)
		print '<td class="label"><b>Proposed Variant Title</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
		print '</tr>'

		current = titles(db)
		current.load(int(Parent))
                if current.error:
                        InvalidSubmission(submission_id, current.error)
                if current.title_parent:
                        InvalidSubmission(submission_id, 'The proposed parent title is a variant of another title record')

		PrintField2XML('Title',     merge, current.used_title,     current.title_title)
                PrintMultField('TransTitles',   'TransTitle',   '<br>', doc, merge,
                               current.used_trans_titles,   current.title_trans_titles)
		PrintField2XML('Year',      merge, current.used_year,      current.title_year)
		PrintField2XML('TitleType', merge, current.used_ttype,     current.title_ttype)
		PrintField2XML('Storylen',  merge, current.used_storylen,  current.title_storylen)
		PrintField2XML('Language',  merge, current.used_language,  current.title_language)
		PrintField2XML('Note',      merge, current.used_note,      current.title_note)
		PrintMultField('Authors', 'Author', '+', doc, merge, current.num_authors, current.title_authors)
		print '</tr>'

	print '</table>'
	mod_note = GetElementValue(merge, 'ModNote')
	if mod_note:
		print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        return submitter

def DisplayUnmergeTitle(submission_id):
        from pubClass import pubs
	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
	if doc.getElementsByTagName('TitleUnmerge'):
		merge = doc.getElementsByTagName('TitleUnmerge')
		Record = GetElementValue(merge, 'Record')
		submitter = GetElementValue(merge, 'Submitter')

		print '<h3>Unmerging from the following title:</h3>'
		title = SQLloadTitle(int(Record))
		if not title:
                        InvalidSubmission(submission_id, 'Title record no longer valid')
		authors = SQLTitleAuthors(int(Record))
		print '<br><b>Title:</b> %s' % ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE])
		print '<br><b>Authors:</b>'
		for author in authors:
			print author
		print '<br><b>Date:</b>', title[TITLE_YEAR]
		print '<br><b>Type:</b>', title[TITLE_TTYPE]
		print '<hr>'

		print '<h3>Unmerging these works:</h3>'
                print '<table border="2" class="generic_table">'
		print '<tr>'
		print '<td class="label"><b>Publication</b></td>'
		print '<td class="label"><b>Unmerged Title Name</b></td>'
		print '</tr>'

		publications = SQLGetPubsByTitleNoParent(int(Record))
		if doc.getElementsByTagName('PubRecord'):
			unmergeList = []
			children = doc.getElementsByTagName('PubRecord')
			if len(children):
				for child in children:
					record = int(child.firstChild.data)
					unmergeList.append(record)
					pub = pubs(db)
					pub.load(record)
					if pub.error:
                                                InvalidSubmission(submission_id, pub.error)

			for pub in publications:
				if pub[PUB_PUBID] in unmergeList:
					print '<tr>'
					#print '<td class="drop"><b>%s</b></td>' % pub[PUB_TITLE]
					# Make a link to existing Publication
					print '<td class="drop">%s</td>' % ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE])
					if (title[TITLE_TTYPE] == 'SHORTFICTION') or (title[TITLE_TTYPE] == 'COVERART'):
                                                newtitle = title[TITLE_TITLE]
					else:
						newtitle = pub[PUB_TITLE]
					print '<td class="keep"><b>%s</b></td>' % newtitle
					print '</tr>'

		print '</table><p>'

                mod_note = GetElementValue(merge, 'ModNote')
                if mod_note:
                        print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        return submitter

def DisplayMergeTitles(submission_id):
        from titleClass import titles

	xml = SQLloadXML(submission_id)
	doc = minidom.parseString(XMLunescape2(xml))

	submitter = ''
        if doc.getElementsByTagName('TitleMerge'):
                KeepId    = 0
                Records   = {}
                Parent    = 0
		try:
			Document = doc.getElementsByTagName('TitleMerge')
        		KeepId = int(GetElementValue(Document, 'KeepId'))
        		submitter = GetElementValue(Document, 'Submitter')
		except:
                        InvalidSubmission(submission_id, 'Missing Required XML tags')

                Records[KeepId] = titles(db)
                Records[KeepId].load(KeepId)
                if Records[KeepId].error:
                        InvalidSubmission(submission_id, "Can't load title: %s" % KeepId)

		dropIds = doc.getElementsByTagName('DropId')
		for dropid in dropIds:
                        title_id = int(dropid.firstChild.data)
                        Records[title_id] = titles(db)
                        Records[title_id].load(title_id)
                        if Records[title_id].error:
				InvalidSubmission(submission_id, "Can't load title: %s" % title_id)

		for title_id_1 in Records:
                        for title_id_2 in Records:
                                if title_id_1 == title_id_2:
                                        continue
                                pubs1 = SQLGetPubsByTitleNoParent(int(title_id_1))
                                pubs2 = SQLGetPubsByTitleNoParent(int(title_id_2))
                                for pub1 in pubs1:
                                        for pub2 in pubs2:
                                                if pub1[PUB_PUBID] == pub2[PUB_PUBID]:
                                                        message = """Records %s and %s both appear in the publication <i>%s</i>.
                                                                Merging two titles that appear in the same publication would cause
                                                                the remaining title to appear twice in the publication, which is not allowed.
                                                                If the submission is trying to remove a duplicate title from a publication, edit
                                                                that publication, click on <b>Remove Titles From This Pub</b>, then select
                                                                the title that you wish to remove""" % (title_id_1, title_id_1, pub1[PUB_TITLE])
                                                        InvalidSubmission(submission_id, message)

                print '<table border="2" class="generic_table">'
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>KeepId %s</b></td>' % ISFDBLinkNoName('title.cgi', KeepId, KeepId, True)
		for title_id in sorted(Records.keys()):
                        if title_id != KeepId:
                                print '<td class="label"><b>DropId %s</b></td>' % ISFDBLinkNoName('title.cgi', title_id, title_id, True)
		print '</tr>'

		PrintMergeField('Title',     Document, KeepId, Records, submission_id)
		PrintMergeField('TranslitTitles',  Document, KeepId, Records, submission_id)
		PrintMergeField('Author',    Document, KeepId, Records, submission_id)
		PrintMergeField('Year',	     Document, KeepId, Records, submission_id)
		PrintMergeField('TitleType', Document, KeepId, Records, submission_id)
		PrintMergeField('Series',    Document, KeepId, Records, submission_id)
		PrintMergeField('Seriesnum', Document, KeepId, Records, submission_id)
		PrintMergeField('Storylen',  Document, KeepId, Records, submission_id)
		PrintMergeField('ContentIndicator',  Document, KeepId, Records, submission_id)
		PrintMergeField('NonGenre',  Document, KeepId, Records, submission_id)
		PrintMergeField('Juvenile',  Document, KeepId, Records, submission_id)
		PrintMergeField('Novelization',  Document, KeepId, Records, submission_id)
		PrintMergeField('Graphic',   Document, KeepId, Records, submission_id)
		PrintMergeField('Language',  Document, KeepId, Records, submission_id)
		PrintMergeField('Webpages',  Document, KeepId, Records, submission_id)
		PrintMergeField('Synopsis',  Document, KeepId, Records, submission_id)
		PrintMergeField('Note',      Document, KeepId, Records, submission_id)
		PrintMergeField('Parent',    Document, KeepId, Records, submission_id)
                print '</table>'

                mod_note = GetElementValue(Document, 'ModNote')
                if mod_note:
                        print '<h3>Note to Moderator: </h3>%s<p><p>' % (mod_note)

        return submitter

def PrintMergeField(Label, XmlData, KeepId, Records, submission_id):
	print '<tr>'
	print '<td class="label"><b>%s</b></td>' % Label
	# Try to retrieve the title ID whose data we will keep for this field
	try:
		keep_id = int(GetElementValue(XmlData, Label))
	# If the submission doesn't contain a title ID for this field,
	# then we will use the default "keep" title ID
	except:
		keep_id = KeepId

	for title_id in sorted(Records.keys()):
                output = '-'
                kept = '-'
		if Label == 'Title':
			if Records[title_id].used_title:
				output = Records[title_id].title_title
			if Records[keep_id].used_title:
				kept = Records[keep_id].title_title
		elif Label == 'TranslitTitles':
			if Records[title_id].used_trans_titles:
				output = '<br>'.join(Records[title_id].title_trans_titles)
		elif Label == 'Author':
                        output = Records[title_id].authors()
                        kept = Records[keep_id].authors()
		elif Label == 'Year':
			if Records[title_id].used_year:
				output = Records[title_id].title_year
			if Records[keep_id].used_year:
				kept = Records[keep_id].title_year
		elif Label == 'Series':
			if Records[title_id].used_series:
				output = Records[title_id].title_series
			if Records[keep_id].used_series:
				kept = Records[keep_id].title_series
		elif Label == 'Seriesnum':
			if Records[title_id].used_seriesnum:
				output = Records[title_id].title_seriesnum
			if Records[keep_id].used_seriesnum:
				kept = Records[keep_id].title_seriesnum
		elif Label == 'TitleType':
			if Records[title_id].used_ttype:
				if Records[title_id].title_ttype == 'COVERART':
                                        cover_pubs = SQLGetCoverPubsByTitle(title_id)
                                        if cover_pubs:
                                                for cover_pub in cover_pubs:
                                                        if cover_pub[PUB_IMAGE]:
                                                                if output == '-':
                                                                        output = ''
                                                                output += '<br>%s<br>' % ISFDBLinkNoName('pl.cgi', cover_pub[PUB_PUBID], FormatImage(cover_pub[PUB_IMAGE], 200))
                                else:
                                        output = Records[title_id].title_ttype
			if Records[keep_id].used_ttype:
				kept = Records[keep_id].title_ttype
		elif Label == 'Storylen':
			if Records[title_id].used_storylen:
				output = Records[title_id].title_storylen
			if Records[keep_id].used_storylen:
				kept = Records[keep_id].title_storylen
		elif Label == 'ContentIndicator':
			if Records[title_id].used_content:
				output = Records[title_id].title_content
			if Records[keep_id].used_content:
				kept = Records[keep_id].title_content
		elif Label == 'Juvenile':
			if Records[title_id].used_jvn:
				output = Records[title_id].title_jvn
			if Records[keep_id].used_jvn:
				kept = Records[keep_id].title_jvn
		elif Label == 'Novelization':
			if Records[title_id].used_nvz:
				output = Records[title_id].title_nvz
			if Records[keep_id].used_nvz:
				kept = Records[keep_id].title_nvz
		elif Label == 'NonGenre':
			if Records[title_id].used_non_genre:
				output = Records[title_id].title_non_genre
			if Records[keep_id].used_non_genre:
				kept = Records[keep_id].title_non_genre
		elif Label == 'Graphic':
			if Records[title_id].used_graphic:
				output = Records[title_id].title_graphic
			if Records[keep_id].used_graphic:
				kept = Records[keep_id].title_graphic
		elif Label == 'Translator':
			if Records[title_id].used_xlate:
				output = Records[title_id].title_xlate
			if Records[keep_id].used_xlate:
				kept = Records[keep_id].title_xlate
		elif Label == 'Language':
			if Records[title_id].used_language:
				output = Records[title_id].title_language
			if Records[keep_id].used_language:
				kept = Records[keep_id].title_language
		elif Label == 'Webpages':
			if Records[title_id].used_webpages:
				output = '<br>'.join(Records[title_id].title_webpages)
		elif Label == 'Synopsis':
			if Records[title_id].used_synop:
				output = Records[title_id].title_synop
			if Records[keep_id].used_synop:
				kept = Records[keep_id].title_synop
		elif Label == 'Note':
			if Records[title_id].used_note:
				output = Records[title_id].title_note
			if Records[keep_id].used_note:
				kept = Records[keep_id].title_note
		elif Label == 'Parent':
			if Records[title_id].used_parent:
				output = Records[title_id].title_parent
			if Records[keep_id].used_parent:
				kept = Records[keep_id].title_parent
				if kept == KeepId:
                                        InvalidSubmission(submission_id, 'The proposed parent title is the title record which will be kept after the merge')
		if Label in ('Webpages', 'TranslitTitles'):
                        css_class = 'keep'
		elif Label == 'TitleType' and Records[title_id].title_ttype == 'COVERART':
                        css_class = 'keep'
		elif title_id == keep_id:
                        css_class = 'keep'
                elif output == kept:
                        css_class = 'keep'
		else:
                        css_class = 'drop'
                print '<td class="%s">%s</td>' % (css_class, output)
	print '</tr>'

def DisplayMakeVariant(submission_id):
        from titleClass import titles
        print '<table border="2" class="generic_table">'
	submitter = ''
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('MakeVariant'):
                merge = doc.getElementsByTagName('MakeVariant')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
                print '<td class="label"><b>Make Variant Record #%s</b>]</td>' % ISFDBLinkNoName('title.cgi', Record, Record, True)
                theVariant = titles(db)
                theVariant.load(int(Record))
                if theVariant.error:
                        InvalidSubmission(submission_id, theVariant.error)
                if TagPresent(merge, 'Parent'):
                        parent = GetElementValue(merge, 'Parent')
                        if int(parent) != 0:
                                print '<td class="label"><b>Variant of Existing Record #%s</b></td>' % ISFDBLinkNoName('title.cgi', parent, parent, True)
                        else:
                                print '<td class="label"><b>Variant of Nothing</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        existingParent = titles(db)
                        existingParent.load(int(parent))
			if existingParent.error:
                                InvalidSubmission(submission_id, existingParent.error)
                        if existingParent.title_parent:
                                InvalidSubmission(submission_id, 'The proposed parent title is a variant of another title record')
                        PrintField2('Title', existingParent.title_title, 1, 1, theVariant.title_title, '', 1)
                        PrintField2('Year', existingParent.title_year, 1, 1, theVariant.title_year, '', 1)
                        if existingParent.title_ttype == 'COVERART' and theVariant.title_ttype == 'COVERART':
                                print '<tr><td class="label"><b>Covers</b></td>'
                                # Display the left column for the "Make Variant" title
                                print '<td class="drop">'
                                cover_pubs = SQLGetCoverPubsByTitle(int(Record))
                                for cover_pub in cover_pubs:
                                        if cover_pub[PUB_IMAGE]:
                                                print '<br>%s<br>' % ISFDBLinkNoName('pl.cgi', cover_pub[PUB_PUBID], FormatImage(cover_pub[PUB_IMAGE]))
                                print '</td>'

                                # Display the right column for the "Variant of" title
                                print '<td class="keep">'
                                cover_pubs = SQLGetCoverPubsByTitle(int(parent))
                                for cover_pub in cover_pubs:
                                        if cover_pub[PUB_IMAGE]:
                                                print '<br>%s<br>' % ISFDBLinkNoName('pl.cgi', cover_pub[PUB_PUBID], FormatImage(cover_pub[PUB_IMAGE]))
                                print '</td>'
                                print '<td class="blankwarning">&nbsp;</td>'
                                print '</tr>'
                        else:
                                warning = TitleTypeMismatch(existingParent.title_ttype, theVariant.title_ttype)
                                PrintField2('TitleType', existingParent.title_ttype, 1, 1, theVariant.title_ttype, warning, 1)

                        warning = ''
                        if existingParent.title_storylen != theVariant.title_storylen and int(parent):
                                if not (existingParent.title_ttype == 'SHORTFICTION' and theVariant.title_ttype == 'SERIAL'):
                                        warning = 'Length mismatch'
                        PrintField2('Length', existingParent.title_storylen, 1, 1, theVariant.title_storylen, warning, 1)

                        warning = ''
                        if existingParent.title_non_genre != theVariant.title_non_genre and int(parent):
                                warning = 'Non-Genre mismatch'
                        PrintField2('Non-Genre', existingParent.title_non_genre, 1, 1, theVariant.title_non_genre, warning, 1)

                        warning = ''
                        if existingParent.title_jvn != theVariant.title_jvn and int(parent):
                                warning = 'Juvenile flag mismatch'
                        PrintField2('Juvenile', existingParent.title_jvn, 1, 1, theVariant.title_jvn, warning, 1)

                        warning = ''
                        if existingParent.title_nvz != theVariant.title_nvz and int(parent):
                                warning = 'Novelization flag mismatch'
                        PrintField2('Novelization', existingParent.title_nvz, 1, 1, theVariant.title_nvz, warning, 1)

                        warning = ''
                        if existingParent.title_graphic != theVariant.title_graphic and int(parent):
                                warning = 'Graphic flag mismatch'
                        PrintField2('Graphic', existingParent.title_graphic, 1, 1, theVariant.title_graphic, warning, 1)

                        PrintField2('Language', existingParent.title_language, 1, 1, theVariant.title_language, '', 1)

                        ###################################
                        # Author
                        ###################################
                        print '<tr>'
                        print '<td class="label"><b>Authors</b></td>'
                        print '<td class="drop">'
                        PrintAuthorNames(theVariant.title_authors, '+')
                        print '</td>'
                        print '<td class="keep">'
                        PrintAuthorNames(existingParent.title_authors, '+')
                        print '</td>'
                        print '<td class="blankwarning">&nbsp;</td>'
                        print '</tr>'

                else:
                        print '<td class="label"><b>Variant of [New Title]</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        PrintField2XML('Title',     merge, theVariant.used_title,     theVariant.title_title)
                        PrintMultField('TransTitles',   'TransTitle',   '<br>', doc, merge,
                                        theVariant.used_trans_titles,   theVariant.title_trans_titles)
                        PrintField2XML('Year',      merge, theVariant.used_year,      theVariant.title_year)
                        # For title types we pre-check for type mismatch, so we use PrintField2 instead of PrintField2XML
                        parent_title_type = GetElementValue(merge, 'TitleType')
                        warning = TitleTypeMismatch(parent_title_type, theVariant.title_ttype)
                        PrintField2('TitleType', parent_title_type, 1, 1, theVariant.title_ttype, warning, 1)
                        PrintField2('Length', theVariant.title_storylen, 1, 1, theVariant.title_storylen, '', 1)
                        PrintField2('Non-Genre', theVariant.title_non_genre, 1, 1, theVariant.title_non_genre, warning, 1)
                        PrintField2('Juvenile', theVariant.title_jvn, 1, 1, theVariant.title_jvn, warning, 1)
                        PrintField2('Novelization', theVariant.title_nvz, 1, 1, theVariant.title_nvz, warning, 1)
                        PrintField2('Graphic', theVariant.title_graphic, 1, 1, theVariant.title_graphic, warning, 1)
                        PrintField2XML('Language',  merge, theVariant.used_language,  theVariant.title_language)
                        PrintMultField('Authors', 'Author', '+', doc, merge, theVariant.num_authors, theVariant.title_authors)
                        PrintField2XML('Note',  merge, theVariant.used_note,  theVariant.title_note, None, 1)

	print '</table>'

	mod_note = GetElementValue(merge, 'ModNote')
	if mod_note:
		print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        return submitter

def TitleTypeMismatch(parent_type, variant_type):
        if not parent_type:
                return ''
        if variant_type == parent_type:
                return ''
        if variant_type == 'SERIAL' and parent_type in ('NOVEL', 'SHORTFICTION'):
                return ''
        if variant_type == 'INTERIORART' and parent_type == 'COVERART':
                return ''
        if variant_type == 'COVERART' and parent_type == 'INTERIORART':
                return ''
        return 'Uncommon Title Type Combination'

def DisplayEditPub(submission_id):
        from pubClass import pubs
        from titleClass import titles

	xml = SQLloadXML(submission_id)
	try:
		doc = minidom.parseString(XMLunescape2(xml))
	except:
		InvalidSubmission("Badly formed XML")
	submitter = ''
	pub_id = 0
        print '<table border="2" class="generic_table">'
        if doc.getElementsByTagName('PubUpdate'):
		merge = doc.getElementsByTagName('PubUpdate')
        	Record = GetElementValue(merge, 'Record')
		pub_id = int(Record)
        	submitter = GetElementValue(merge, 'Submitter')
		
		print '<tr>'
		print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current Record #%s</b></td>' % ISFDBLinkNoName('pl.cgi', Record, Record, True)
		print '<td class="label"><b>Proposed Changes</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
		print '</tr>'

		current = pubs(db)
		current.load(int(Record))
                if current.error:
                        InvalidSubmission(submission_id, current.error)

		PrintField2XML('Title',     merge, current.used_title,     current.pub_title)
                PrintMultField('TransTitles',   'TransTitle',   '<br>', doc, merge,
                               current.used_trans_titles,   current.pub_trans_titles)
		PrintMultField('Authors', 'Author', '+', doc, merge, current.num_authors, current.pub_authors)
		PrintField2XML('Year',      merge, current.used_year,      current.pub_year)
		PrintField2XML('Publisher', merge, current.used_publisher, current.pub_publisher)
		PrintField2XML('PubSeries', merge, current.used_series, current.pub_series)
		PrintField2XML('PubSeriesNum', merge, current.used_series_num, current.pub_series_num)
		PrintField2XML('Pages',     merge, current.used_pages,     current.pub_pages)
		PrintField2XML('Binding',   merge, current.used_ptype,     current.pub_ptype)
		PrintField2XML('PubType',   merge, current.used_ctype,     current.pub_ctype)
		PrintField2XML('Isbn',      merge, current.used_isbn,      current.pub_isbn, pub_id)
		PrintField2XML('Catalog',   merge, current.used_catalog,   current.pub_catalog)
		PrintField2XML('Price',     merge, current.used_price,     current.pub_price)
		PrintField2XML('Image',     merge, current.used_image,     current.pub_image)
                PrintMultField('Webpages', 'Webpage', '<br>', doc, merge, current.used_webpages, current.pub_webpages)
		PrintField2XML('Note',      merge, current.used_note,      current.pub_note)
		PrintEditExternalIDs(merge, doc, current, submission_id)

		print '</table>'

        	if doc.getElementsByTagName('Content'):

                        ##########################################################
                        # Modified Cover Art
                        ##########################################################
                        children = doc.getElementsByTagName('Cover')
                        if len(children):
				needCover = 1
                                for child in children:
                                        record = GetChildValue(child, 'Record')
					if record:
						if needCover:
							needCover = 0
							print '<h2>Modified Cover Art</h2>'
                                                        print '<table border="2" class="generic_table">'
                                                displayCoverChanged(child, record, submission_id, current)
				if needCover == 0:
					print '</table>'

			##########################################################
			# Modified Regular Titles
			##########################################################
			children = doc.getElementsByTagName('ContentTitle')
			if len(children):
				needTitle = 1
				for child in children:
					record  = GetChildValue(child, 'Record')
					if record:
						if needTitle:
							needTitle = 0
							print '<h2>Modified Regular Titles</h2>'
                                                        print '<table border="2" class="generic_table">'
                                                displayTitleContentChanged(child, record, submission_id, current)
				if needTitle == 0:
					print '</table>'
				
			##########################################################
			# Modified Reviews
			##########################################################
			children = doc.getElementsByTagName('ContentReview')
			if len(children):
				needTitle = 1
				for child in children:
					record  = GetChildValue(child, 'Record')
					if record:
						if needTitle:
							needTitle = 0
							print '<h2>Modified Reviews</h2>'
                                                        print '<table border="2" class="generic_table">'
                                                displayOtherContentChanged(child, 'review', record, submission_id, current)
				if needTitle == 0:
					print '</table>'

			##########################################################
			# Modified Interviews
			##########################################################
			children = doc.getElementsByTagName('ContentInterview')
			if len(children):
				needTitle = 1
				for child in children:
					record  = GetChildValue(child, 'Record')
					if record:
						if needTitle:
							needTitle = 0
							print '<h2>Modified Interviews</h2>'
                                                        print '<table border="2" class="generic_table">'
                                                displayOtherContentChanged(child, 'interview', record, submission_id, current)
				if needTitle == 0:
					print '</table>'

                        ##########################################################
                        # New Cover Art
                        ##########################################################
                        children = doc.getElementsByTagName('Cover')
                        if len(children):
				needCover = 1
                                for child in children:
                                        record = GetChildValue(child, 'Record')
					if not record:
						if needCover:
							needCover = 0
							print '<h2>New Cover Art</h2>'
                                                        print '<table border="2" class="generic_table">'
							print '<tr>'
							print '<td class="label"><b>Title</b></td>'
							print '<td class="label"><b>Artists</b></td>'
							print '<td class="label"><b>Date</b></td>'
							print '<td class="label"><b>Warnings</b></td>'
							print '</tr>'
                                                displayCoverAdded(child, submission_id, current)
				if needCover == 0:
					print '</table>'

			##########################################################
			# New Regular Titles
			##########################################################
			children = doc.getElementsByTagName('ContentTitle')
			if len(children):
				needTitle = 1
				for child in children:
					record  = GetChildValue(child, 'Record')
					if record == '':
						if needTitle:
							needTitle = 0
							print '<h2>New Regular Titles</h2>'
                                                        print '<table border="2" class="generic_table">'
							print '<tr>'
							print '<td class="label"><b>Page</b></td>'
							print '<td class="label"><b>Title</b></td>'
							print '<td class="label"><b>Authors</b></td>'
							print '<td class="label"><b>Date</b></td>'
							print '<td class="label"><b>Type</b></td>'
							print '<td class="label"><b>Length</b></td>'
							print '<td class="label"><b>Warnings</b></td>'
							print '</tr>'
						displayTitleContentAdded(child, submission_id, current)

				if needTitle == 0:
					print '</table>'
				
			##########################################################
			# New Reviews
			##########################################################
			children = doc.getElementsByTagName('ContentReview')
			if len(children):
				needTitle = 1
				for child in children:
					record    = GetChildValue(child, 'Record')
					if record == '':
						if needTitle:
							needTitle = 0
							print '<h2>New Reviews</h2>'
                                                        print '<table border="2" class="generic_table">'
							print '<tr>'
							print '<td class="label"><b>Page</b></td>'
							print '<td class="label"><b>Title</b></td>'
							print '<td class="label"><b>Authors</b></td>'
							print '<td class="label"><b>Reviewers</b></td>'
							print '<td class="label"><b>Date</b></td>'
							print '<td class="label"><b>Warnings</b></td>'
							print '</tr>'
						displayOtherContentAdded(child, 'review', submission_id, current)
				if needTitle == 0:
					print '</table>'

			##########################################################
			# New Interviews
			##########################################################
			children = doc.getElementsByTagName('ContentInterview')
			if len(children):
				needTitle = 1
				for child in children:
					record       = GetChildValue(child, 'Record')
					if record == '':
						if needTitle:
							needTitle = 0
							print '<h2>New Interviews</h2>'
                                                        print '<table border="2" class="generic_table">'
							print '<tr>'
							print '<td class="label"><b>Page</b></td>'
							print '<td class="label"><b>Title</b></td>'
							print '<td class="label"><b>Interviewees</b></td>'
							print '<td class="label"><b>Interviewers</b></td>'
							print '<td class="label"><b>Date</b></td>'
							print '<td class="label"><b>Warnings</b></td>'
							print '</tr>'
						displayOtherContentAdded(child, 'interview', submission_id, current)
				if needTitle == 0:
					print '</table>'

        DisplayVerifications(Record)

	mod_note = GetElementValue(merge, 'ModNote')
	if mod_note:
		print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'

        return submitter

def getReviewees(review_id):
	reviewees = SQLReviewAuthors(int(review_id))
	newreviewees = ''
	count = 1
	for reviewee in reviewees:
		if count == 1:
			newreviewees += reviewee
		else:
			newreviewees += '+'+reviewee
		count += 1
	return(newreviewees)

def getInterviewees(interview_id):
	interviewees = SQLInterviewAuthors(int(interview_id))
	newinterviewees = ''
	count = 1
	for interviewee in interviewees:
		if count == 1:
			newinterviewees += interviewee
		else:
			newinterviewees += '+'+interviewee
		count += 1
	return(newinterviewees)

def displayCoverChanged(child, record, submission_id, current):
        title   = GetChildValue(child, 'cTitle')
        artists = GetChildValue(child, 'cArtists')
        date    = GetChildValue(child, 'cDate')
        print '<tr>'
        print '<td class="label"> </td>'
        print '<td class="label"><b>Current</b></td>'
        print '<td class="label"><b>Proposed</b></td>'
        print '<td class="label"><b>Warnings</b></td>'
        print '</tr>'

        checkTitleExistence(record, submission_id)
        titleData = SQLloadTitle(record)
        PrintComparison2('Title', title, titleData[TITLE_TITLE])
        oldartists = '+'.join(SQLTitleAuthors(record))
        PrintComparison2('Artists', artists, oldartists)
        warning = ''
        if Compare2Dates(current.pub_year, date) == 1:
                warning = 'Title date after publication date'
        PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)

def displayCoverAdded(child, submission_id, current):
        title   = GetChildValue(child, 'cTitle')
        artists = GetChildValue(child, 'cArtists')
        date    = GetChildValue(child, 'cDate')
        print '<tr>'
        print '<td class="keep">%s</td>' % title
        print '<td class="keep">'
        artist_list = artists.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(artist_list, '+')
        print '</td>'
        print '<td class="keep">%s</td>' % date
        PrintWarning('Artist', unknown, pseudonym, disambig, date, current.pub_year)
        print '</tr>'

def displayTitleContentChanged(child, record, submission_id, current):
        title   = GetChildValue(child, 'cTitle')
        authors = GetChildValue(child, 'cAuthors')
        date    = GetChildValue(child, 'cDate')
        page    = GetChildValue(child, 'cPage')
        type    = GetChildValue(child, 'cType')
        length  = GetChildValue(child, 'cLength')
        if page == '' and TagPresent(child, 'cPage'):
                page = '-'
        if length == '' and TagPresent(child, 'cLength'):
                length = '-'
        print '<tr>'
        print '<td class="label"> </td>'
        print '<td class="label"><b>Current</b></td>'
        print '<td class="label"><b>Proposed</b></td>'
        print '<td class="label"><b>Warnings</b></td>'
        print '</tr>'

        checkTitleExistence(record, submission_id)
        titleData = SQLloadTitle(record)
        oldauthors = '+'.join(SQLTitleAuthors(record))
        oldPage = SQLGetPageNumber(record, current.pub_id)

        PrintComparison2('Title', title, titleData[TITLE_TITLE])
        PrintComparison2('Authors', authors, oldauthors)
        warning = ''
        if Compare2Dates(current.pub_year, date) == 1:
                warning = 'Title date after publication date'
        PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)
        PrintComparison2('Type', type, titleData[TITLE_TTYPE])
        PrintComparison2('Length', length, titleData[TITLE_STORYLEN])
        PrintComparison2('Page', page, oldPage)

def displayTitleContentAdded(child, submission_id, current):
        title   = GetChildValue(child, 'cTitle')
        authors = GetChildValue(child, 'cAuthors')
        date    = GetChildValue(child, 'cDate')
        page    = GetChildValue(child, 'cPage')
        type    = GetChildValue(child, 'cType')
        length  = GetChildValue(child, 'cLength')
        print '<tr>'
        print '<td class="keep">%s</td>' % page
        print '<td class="keep">%s</td>' % title
        print '<td class="keep">'
        author_list = authors.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
        print '</td>'
        print '<td class="keep">%s</td>' % date
        print '<td class="keep">%s</td>' % type
        print '<td class="keep">%s</td>' % length
        PrintWarning('Author', unknown, pseudonym, disambig, date, current.pub_year)
        print '</tr>'

def displayOtherContentChanged(child, record_type, record, submission_id, current):
        title = GetChildValue(child, 'cTitle')
        page = GetChildValue(child, 'cPage')
        if (page == '') and TagPresent(child, 'cPage'):
                page = '-'
        date = GetChildValue(child, 'cDate')
        if record_type == 'review':
                primary_authors   = GetChildValue(child, 'cBookAuthors')
                secondary_authors = GetChildValue(child, 'cReviewers')
        else:
                primary_authors = GetChildValue(child, 'cInterviewees')
                secondary_authors = GetChildValue(child, 'cInterviewers')
        print '<tr>'
        print '<td class="label"> </td>'
        print '<td class="label"><b>Current</b></td>'
        print '<td class="label"><b>Proposed</b></td>'
        print '<td class="label"><b>Warnings</b></td>'
        print '</tr>'

        checkTitleExistence(record, submission_id)
        titleData = SQLloadTitle(record)
        PrintComparison2('Title', title, titleData[TITLE_TITLE])

        if titleData[TITLE_TTYPE] == 'REVIEW':
                oldauthors = getReviewees(record)
                PrintComparison2('Book Authors', primary_authors, oldauthors)
                oldreviewers = '+'.join(SQLTitleAuthors(record))
                PrintComparison2('Reviewers', secondary_authors, oldreviewers)
        elif titleData[TITLE_TTYPE] == 'INTERVIEW':
                oldauthors = getInterviewees(record)
                PrintComparison2('Interviewees', primary_authors, oldauthors)
                oldinterviewers = '+'.join(SQLTitleAuthors(record))
                PrintComparison2('Interviewers', secondary_authors, oldinterviewers)

        warning = ''
        if Compare2Dates(current.pub_year, date) == 1:
                warning = 'Title date after publication date'
        PrintComparison2('Year', date, titleData[TITLE_YEAR], warning)
        oldPage = SQLGetPageNumber(record, current.pub_id)
        PrintComparison2('Page', page, oldPage)

def displayOtherContentAdded(child, record_type, submission_id, current):
        from operator import add
        title = GetChildValue(child, 'cTitle')
        date = GetChildValue(child, 'cDate')
        page = GetChildValue(child, 'cPage')
        if record_type == 'review':
                primary_authors   = GetChildValue(child, 'cBookAuthors')
                secondary_authors = GetChildValue(child, 'cReviewers')
        else:
                primary_authors = GetChildValue(child, 'cInterviewees')
                secondary_authors = GetChildValue(child, 'cInterviewers')
        (unknown, pseudonym, disambig, unknown2, pseudonym2, disambig2) = 0, 0, 0, 0, 0, 0
        print '<tr>'
        print '<td class="keep">%s</td>' % page
        print '<td class="keep">%s</td>' % title
        print '<td class="keep">'
        author_list = primary_authors.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
        print '</td>'
        print '<td class="keep">'
        author_list = secondary_authors.split('+')
        (unknown2, pseudonym2, disambig2) = PrintAuthorNames(author_list, '+')
        print '</td>'
        print '<td class="keep">%s</td>' % date
        # Add the values of the unknown, pseudonym and disambig flags for primary and secondary authors 
        (unknown, pseudonym, disambig) = map(add, (unknown, pseudonym, disambig), (unknown2, pseudonym2, disambig2))
        PrintWarning('Author', unknown, pseudonym, disambig, date, current.pub_year)
        print '</tr>'

def cloningFlag(merge):
        if GetElementValue(merge, 'ClonedTo'):
                cloningContent = GetElementValue(merge, 'ClonedTo')
        else:
                cloningContent = 0
        return cloningContent

def DisplayClonePublication(submission_id):
        try:
                xml = SQLloadXML(submission_id)
        	doc = minidom.parseString(XMLunescape2(xml))
        except:
        	InvalidSubmission(submission_id, 'Invalid XML in the submission')

        if not doc.getElementsByTagName('NewPub'):
        	InvalidSubmission(submission_id, 'Expected data elements not found in the submission')

        merge = doc.getElementsByTagName('NewPub')
        submitter = GetElementValue(merge, 'Submitter')
        cloningContent = cloningFlag(merge)

        value = GetElementValue(merge, 'Parent')
        if TagPresent(merge, 'Parent'):
                title_data = SQLloadTitle(int(value))
                # If the title that the new pub is supposed to be auto-merged with no longer exists, hard reject the submission
                if title_data == []:
                        InvalidSubmission(submission_id, 'Title %d is no longer in the database' % int(value))
                else:	
                        if cloningContent:
                                print 'Import/Export -- automerging content from title %s' % ISFDBLink('title.cgi', value, title_data[TITLE_TITLE])
                        else:
                                print 'Clone Publication -- will be automerged with title %s' % ISFDBLink('title.cgi', value, title_data[TITLE_TITLE])
        else:
                if cloningContent:
                        pub = SQLGetPubById(cloningContent)
                        print 'Importing content into publication record %s' % ISFDBLink('pl.cgi', pub[PUB_PUBID], pub[PUB_TITLE])


        print '<h2>Publication data</h2>'
        print '<table border="1" cellpadding=2>'
        print "<tr>"
        print '<td class="label"><b>Column</b></td>'
        print '<td class="label"><b>Proposed Values</b></td>'
        print '<td class="label" align="center"><b>Warnings</b></td>'
        print "</tr>"

        ##########################################################
        # MetaData
        ##########################################################
        PrintField1XML('Title',     merge, 0)
        PrintMultFieldRaw(merge, doc, 'TransTitles', 'TransTitle')
        PrintMultField2XML('Authors', 'Author', '+', doc, merge)
        PrintField1XML('Year',      merge, 0)
        PrintField1XML('Publisher', merge, 0)
        PrintField1XML('PubSeries', merge, 0)
        PrintField1XML('PubSeriesNum', merge, 0)
        PrintField1XML('Pages',     merge, 0)
        PrintField1XML('Binding',   merge, 0)
        PrintField1XML('PubType',   merge, 0)
        PrintField1XML('Isbn',      merge, 0)
        PrintField1XML('Catalog',   merge, 0)
        PrintField1XML('Price',     merge, 0)
        PrintField1XML('Image',     merge, 0)
        PrintMultFieldRaw(merge, doc, 'Webpages', 'Webpage')
        PrintField1XML('Note',      merge, 0)
        PrintNewExternalIDs(merge, doc, submission_id)
        print '</table>'

        pub_date = GetElementValue(merge, 'Year')

        if doc.getElementsByTagName('Content'):
                ##########################################################
                # Cover Art
                ##########################################################
                children = doc.getElementsByTagName('Cover')
                if len(children):
                        print '<h2>Cover Art</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Artists</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Merge Method</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayCoverClone(pub_date, child, submission_id)
                        print '</table>'

                ##########################################################
                # Regular Titles
                ##########################################################
                children = doc.getElementsByTagName('ContentTitle')
                if len(children):
                        print '<h2>Regular Titles</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Authors</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Type</b></td>'
                        print '<td class="label"><b>Length</b></td>'
                        print '<td class="label"><b>Merge Method</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayTitleContentClone(pub_date, child, submission_id)
                        print '</table>'
                        
                ##########################################################
                # Reviews
                ##########################################################
                children = doc.getElementsByTagName('ContentReview')
                if len(children):
                        print '<h2>Book Reviews</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Book Authors</b></td>'
                        print '<td class="label"><b>Reviewers</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Merge Method</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayOtherContentClone(pub_date, child, submission_id, 'review')
                        print '</table>'

                ##########################################################
                # Interviews
                ##########################################################
                children = doc.getElementsByTagName('ContentInterview')
                if len(children):
                        print '<h2>Interviews</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Interviewees</b></td>'
                        print '<td class="label"><b>Interviewers</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Merge Method</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayOtherContentClone(pub_date, child, submission_id, 'interview')
                        print '</table>'

        DisplaySource(merge)

        if cloningContent:
                DisplayVerifications(pub[PUB_PUBID])

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note:
                print '<h3>Note to Moderator: </h3>' + mod_note + '<p><p>'
        
        return submitter

def DisplaySource(merge):
        source = GetElementValue(merge, 'Source')
        if source:
                print '<h3>Source used:</h3>'
                if source == 'Primary': 
                        print 'Data from an owned primary source (will be auto-verified)'
                elif source == 'Transient': 
                        print 'Data from a transient primary source (will be auto-verified)'
                elif source == 'PublisherWebsite': 
                        print 'Data from publisher\'s website (Note will be updated accordingly)'
                elif source == 'AuthorWebsite': 
                        print 'Data from author\'s website (Note will be updated accordingly)'
                elif source == 'Other':
                        print 'Data from another source (details should be provided in the submitted Note)'
                        if not GetElementValue(merge, 'Note'):
                                print ' <span class="warn">- No Note data</span>'
                print '<p>'
        
def checkTitleExistence(title_id, submission_id):
        # Check that each about-to-be-merged title is still in the database
        # If the title ID is not specified, skip this check
	if not int(title_id):
		return
        title_data = SQLloadTitle(int(title_id))
        # If the title record is no longer on file, display an error and abort
        if not title_data:
                InvalidSubmission(submission_id, 'Title %d is no longer in the database' % int(title_id))

def displayCoverClone(pub_date, child, submission_id):
        cover_id = GetChildValue(child, 'Record')
        title   = GetChildValue(child, 'cTitle')
        artists = GetChildValue(child, 'cArtists')
        title_date = GetChildValue(child, 'cDate')
        checkTitleExistence(cover_id, submission_id)
	print '<tr>'
	if int(cover_id):
                print '<td class="keep">%s</td>' % ISFDBLink('title.cgi', cover_id, title)
        else:
                print '<td class="keep">%s</td>' % title

	print '<td class="keep">'
	artist_list = artists.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(artist_list, '+')
        print '</td>'

	print '<td class="keep">%s</td>' % title_date
	if int(cover_id):
		print '<td class="keep">Auto Merge</td>'
		# Do not display moderator warnings for autho-merged titles
                PrintWarning('Artist', 0, 0, 0, title_date, pub_date)
	else:
		print '<td class="drop">Manual Merge</td>'
                PrintWarning('Artist', unknown, pseudonym, disambig, title_date, pub_date)
	print '</tr>'

def displayTitleContentClone(pub_date, child, submission_id):
        title_id = GetChildValue(child, 'Record')
        title   = GetChildValue(child, 'cTitle')
        authors = GetChildValue(child, 'cAuthors')
        title_date    = GetChildValue(child, 'cDate')
        page    = GetChildValue(child, 'cPage')
        title_type    = GetChildValue(child, 'cType')
        length  = GetChildValue(child, 'cLength')
        checkTitleExistence(title_id, submission_id)
	print "<tr>"
	print '<td class="keep">%s</td>' % (page)
	if int(title_id):
                print '<td class="keep">%s</td>' % ISFDBLink('title.cgi', title_id, title)
        else:
                print '<td class="keep">%s</td>' % title

	print '<td class="keep">'
	author_list = authors.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
        print '</td>'

	print '<td class="keep">%s</td>' % (title_date)
	print '<td class="keep">%s</td>' % (title_type)
	print '<td class="keep">%s</td>' % (length)
	if int(title_id):
		print '<td class="keep">Auto Merge</td>'
		# Do not display moderator warnings for auto-merged titles
                PrintWarning('Author', 0, 0, 0, title_date, pub_date)
	else:
		print '<td class="drop">Manual Merge</td>'
                PrintWarning('Author', unknown, pseudonym, disambig, title_date, pub_date)
	print "</tr>"

def displayOtherContentClone(pub_date, child, submission_id, record_type):
        from operator import add
	(unknown, pseudonym, disambig, unknown2, pseudonym2, disambig2) = 0, 0, 0, 0, 0, 0
        title_id  = GetChildValue(child, 'Record')
        title     = GetChildValue(child, 'cTitle')
        if record_type == 'review':
                primary_authors   = GetChildValue(child, 'cBookAuthors')
                secondary_authors = GetChildValue(child, 'cReviewers')
        else:
                primary_authors = GetChildValue(child, 'cInterviewees')
                secondary_authors = GetChildValue(child, 'cInterviewers')
        title_date = GetChildValue(child, 'cDate')
        page      = GetChildValue(child, 'cPage')
        checkTitleExistence(title_id, submission_id)
	print "<tr>"
	if not page:
		print '<td class="drop">-</td>'
	else:
		print '<td class="keep">%s</td>' % page
	if not title:
		print '<td class="drop">-</td>'
	else:
                if int(title_id):
                        print '<td class="keep">%s</td>' % ISFDBLink('title.cgi', title_id, title)
                else:
                        print '<td class="keep">%s</td>' % title
	if not primary_authors:
		print '<td class="drop">-</td>'
	else:
		print '<td class="keep">'
                author_list = primary_authors.split('+')
                (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
                print '</td>'
	if not secondary_authors:
		print '<td class="drop">-</td>'
	else:
		print '<td class="keep">'
                author_list = secondary_authors.split('+')
                (unknown2, pseudonym2, disambig2) = PrintAuthorNames(author_list, '+')
                print '</td>'
	if not title_date:
		print '<td class="drop">-</td>'
	else:
		print '<td class="keep">%s</td>' % title_date
	# Add the values of the unknown, pseudonym and disambig flags for
	# primary and secondary (reviewee/intervieew) authors 
	(unknown, pseudonym, disambig) = map(add, (unknown, pseudonym, disambig), (unknown2, pseudonym2, disambig2))
	if int(title_id):
		print '<td class="keep">Auto Merge</td>'
		# Do not display moderator warnings for autho-merged titles
                PrintWarning('Author', 0, 0, 0, title_date, pub_date)
	else:
		print '<td class="drop">Manual Merge</td>'
                PrintWarning('Author', unknown, pseudonym, disambig, title_date, pub_date)
	print "</tr>"

def DisplayNewPub(submission_id):
        xml = SQLloadXML(submission_id)
        doc = minidom.parseString(XMLunescape2(xml))

        if not doc.getElementsByTagName('NewPub'):
        	InvalidSubmission(submission_id, 'Expected data elements not found in the submission')

        merge = doc.getElementsByTagName('NewPub')
        submitter = GetElementValue(merge, 'Submitter')

        value = GetElementValue(merge, 'Parent')
        title_data = []
        if TagPresent(merge, 'Parent'):
                title_data = SQLloadTitle(int(value))
                if title_data == []:
                        InvalidSubmission(submission_id, 'Automerge specified, but target title record %s is missing' % value)
                else:
                        print 'Automerge with title %s' % ISFDBLink('title.cgi', value, title_data[TITLE_TITLE])

        ##########################################################
        # Title data
        ##########################################################
        print '<h2>Title Data</h2>'
        print '<table border="1" cellpadding=2>'
        print "<tr>"
        print '<td class="label"><b>Column</b></td>'
        print '<td class="label"><b>Proposed Values</b></td>'
        print '<td class="label" align="center"><b>Warnings</b></td>'
        print "</tr>"
        PrintField1XML('Title',     merge, title_data)
        PrintMultFieldRaw(merge, doc, 'TransTitles', 'TransTitle')
        PrintMultField2XML('Authors', 'Author', '+', doc, merge)
        PrintField1XML('Language',  merge, title_data)
        PrintField1XML('Synopsis',  merge, title_data)
        PrintField1XML('TitleNote',  merge, title_data)
        PrintField1XML('Series', merge, title_data)
        PrintField1XML('SeriesNum', merge, title_data)
        PrintField1XML('ContentIndicator', merge, title_data)
        PrintField1XML('NonGenre',  merge, title_data)
        PrintField1XML('Juvenile',  merge, title_data)
        PrintField1XML('Novelization',  merge, title_data)
        PrintField1XML('Graphic',   merge, title_data)
        PrintMultFieldRaw(merge, doc, 'Webpages', 'Webpage')
        print '</table>'

        print '<h2>Publication Data</h2>'
        print '<table border="1" cellpadding=2>'
        print '<tr>'
        print '<td class="label"><b>Column</b></td>'
        print '<td class="label"><b>Proposed Values</b></td>'
        print '<td class="label" align="center"><b>Warnings</b></td>'
        print '</tr>'

        ##########################################################
        # Publication MetaData
        ##########################################################
        PrintField1XML('Year',      merge, title_data)
        PrintField1XML('PubType',   merge, title_data)
        PrintField1XML('Publisher', merge, title_data)
        PrintField1XML('Pages',     merge, title_data)
        PrintField1XML('Binding',   merge, title_data)
        PrintField1XML('Isbn',      merge, title_data)
        PrintField1XML('Catalog',   merge, title_data)
        PrintField1XML('Price',     merge, title_data)
        PrintField1XML('PubSeries', merge, title_data)
        PrintField1XML('PubSeriesNum', merge, title_data)
        PrintField1XML('Image',     merge, title_data)
        PrintMultFieldRaw(merge, doc, 'PubWebpages', 'PubWebpage')
        PrintField1XML('Note',      merge, title_data)
        PrintNewExternalIDs(merge, doc, submission_id)
        print '</table>'

        if doc.getElementsByTagName('Content'):
                ##########################################################
                # Cover Art
                ##########################################################
                children = doc.getElementsByTagName('Cover')
                if len(children):
                        print '<h2>Cover Art</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Artists</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayCoverNew(child)
                        print '</table>'
                ##########################################################
                # Content
                ##########################################################
                children = doc.getElementsByTagName('ContentTitle')
                if len(children):
                        print '<h2>Regular Titles</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Authors</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Type</b></td>'
                        print '<td class="label"><b>Length</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayTitleContentNew(child, merge)
                        print '</table>'
                        
                ##########################################################
                # Reviews
                ##########################################################
                children = doc.getElementsByTagName('ContentReview')
                if len(children):
                        print '<h2>Reviews</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Authors</b></td>'
                        print '<td class="label"><b>Reviewers</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayOtherContentNew(child, 'review', merge)
                        print '</table>'

                ##########################################################
                # Interviews
                ##########################################################
                children = doc.getElementsByTagName('ContentInterview')
                if len(children):
                        print '<h2>Interviews</h2>'
                        print '<table border="2" class="generic_table">'
                        print '<tr>'
                        print '<td class="label"><b>Page</b></td>'
                        print '<td class="label"><b>Title</b></td>'
                        print '<td class="label"><b>Interviewees</b></td>'
                        print '<td class="label"><b>Interviewers</b></td>'
                        print '<td class="label"><b>Date</b></td>'
                        print '<td class="label"><b>Warnings</b></td>'
                        print '</tr>'
                        for child in children:
                                displayOtherContentNew(child, 'interview', merge)
                        print '</table>'

        mod_note = GetElementValue(merge, 'ModNote')
        if mod_note: 
                print '<h3>Note to Moderator: </h3>' + mod_note	+ '<p><p>'

        DisplaySource(merge)
        return submitter

def PrintNewExternalIDs(merge, doc, submission_id):
        print '<tr>'
        print '<td class="label"><b>External IDs</b></td>'
        PrintExternalIDsCell(merge, doc, submission_id)
        # Print an empty warnings cell
        print '<td class="blankwarning">&nbsp;</td>'
        print '</tr>'

def PrintExternalIDsCell(merge, doc, submission_id):
        if GetElementValue(merge, 'External_IDs'):
                id_types = SQLLoadIdentifierTypes()
                sites = SQLLoadIdentifierSites()
                display_values = {}
                print '<td class="keep">'
                id_elements = doc.getElementsByTagName('External_ID')
                for id_element in id_elements:
                        try:
                                type_id = int(GetChildValue(id_element, 'IDtype'))
                                type_name = id_types[type_id][0]
                                full_name = id_types[type_id][1]
                        except:
                                InvalidSubmission(submission_id, 'Submitted external ID type does not exist')
                        id_value = XMLunescape(GetChildValue(id_element, 'IDvalue'))
                        if type_name not in display_values:
                                display_values[type_name] = []
                        display_values[type_name].append((id_value, full_name, type_id))
                for type_name in sorted(display_values.keys()):
                        formatted_line = FormatExternalIDType(type_name, id_types)
                        for value in display_values[type_name]:
                                id_value = value[0]
                                type_full_name = value[1]
                                type_id = value[2]
                                formatted_id = FormatExternalIDSite(sites, type_id, id_value)
                                formatted_line += formatted_id
                        print formatted_line,'<br>'
                print '</td>'
        else:
                print '<td class="drop">-</td>'

def PrintEditExternalIDs(merge, doc, current, submission_id):
        print '<tr>'
        print '<td class="label"><b>External IDs</b></td>'
        if GetElementValue(merge, 'External_IDs'):
                print '<td class="drop">'
        else:
                print '<td class="keep">'
        current.printExternalIDs('table')
        print '</td>'
        PrintExternalIDsCell(merge, doc, submission_id)
        # Print an empty warnings cell
        print '<td class="blankwarning">&nbsp;</td>'
        print '</tr>'

def PrintDeleteExternalIDs(current):
        print '<tr>'
        print '<td class="label"><b>External IDs</b></td>'
        if current.identifiers:
                print '<td class="keep">'
                current.printExternalIDs('table')
        else:
                print '<td class="drop">-'
        print '</td>'
        print '</tr>'

def displayCoverNew(child):
        title   = GetChildValue(child, 'cTitle')
        date    = GetChildValue(child, 'cDate')
        artists = GetChildValue(child, 'cArtists')
	print '<tr>'
	print '<td class="keep">%s</td>' % title

	print '<td class="keep">'
	artist_list = artists.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(artist_list, '+')
        print '</td>'

	print '<td class="keep">%s</td>' % date
        PrintWarning('Artist', unknown, pseudonym, disambig)
	print '</tr>'

def displayTitleContentNew(child, merge):
        title   = GetChildValue(child, 'cTitle')
        authors = GetChildValue(child, 'cAuthors')
        title_date    = GetChildValue(child, 'cDate')
        page    = GetChildValue(child, 'cPage')
        type    = GetChildValue(child, 'cType')
        length  = GetChildValue(child, 'cLength')
	print '<tr>'
	print '<td class="keep">%s</td>' % page
	print '<td class="keep">%s</td>' % title
	print '<td class="keep">'
	author_list = authors.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
        print '</td>'
	print '<td class="keep">%s</td>' % title_date
	print '<td class="keep">%s</td>' % type
	print '<td class="keep">%s</td>' % length
	pub_date = GetElementValue(merge, 'Year')
        PrintWarning('Author', unknown, pseudonym, disambig, title_date, pub_date)
	print '</tr>'

def displayOtherContentNew(child, record_type, merge):
        from operator import add
        title = GetChildValue(child, 'cTitle')
        if record_type == 'review':
                primary_authors   = GetChildValue(child, 'cBookAuthors')
                secondary_authors = GetChildValue(child, 'cReviewers')
        else:
                primary_authors = GetChildValue(child, 'cInterviewees')
                secondary_authors = GetChildValue(child, 'cInterviewers')
        title_date = GetChildValue(child, 'cDate')
        page = GetChildValue(child, 'cPage')
	print '<tr>'
        print '<td class="keep">%s</td>' % page
	(unknown, pseudonym, disambig, unknown2, pseudonym2, disambig2) = 0, 0, 0, 0, 0, 0
        print '<td class="keep">%s</td>' % title
        print '<td class="keep">'
        author_list = primary_authors.split('+')
        (unknown, pseudonym, disambig) = PrintAuthorNames(author_list, '+')
        print '</td>'
        print '<td class="keep">'
        author_list = secondary_authors.split('+')
        (unknown2, pseudonym2, disambig2) = PrintAuthorNames(author_list, '+')
        print '</td>'
        print '<td class="keep">%s</td>' % title_date
	# Add the values of the unknown, pseudonym and disambig flags for primary and secondary authors 
	(unknown, pseudonym, disambig) = map(add, (unknown, pseudonym, disambig), (unknown2, pseudonym2, disambig2))
	pub_date = GetElementValue(merge, 'Year')
        PrintWarning('Author', unknown, pseudonym, disambig, title_date, pub_date)
	print "</tr>"

def DisplayVerifications(pub_id, include_secondary = 1):
        from pubClass import pubs
        pub = pubs(db)
        pub.pub_id = pub_id
        verificationstatus = SQLVerificationStatus(pub_id)
        if verificationstatus == 1:
		print '<p><div id="WarningBox">'
		print '<b>WARNING:</b> This publication has been verified against the primary source.'
                print '</div><p>'
        pub.PrintPrimaryVerifications()
        if include_secondary:
                pub.PrintActiveSecondaryVerifications()

def DisplayVerificationSourceEdit(submission_id):
	from verificationsourceClass import VerificationSource

	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('VerificationSource'):
                merge = doc.getElementsByTagName('VerificationSource')
                Record = GetElementValue(merge, 'Record')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Column</b></td>'
		print '<td class="label"><b>Current</b></td>'
                print '<td class="label"><b>Proposed</b></td>'
                print '<td class="label"><b>Warnings</b></td>'
                print '</tr>'

                current = VerificationSource()
                current.load(int(Record))
                if not current.id:
                        InvalidSubmission(submission_id, 'This verification source no longer exists')

                PrintField2XML('SourceLabel', merge, 1,  current.label)
                PrintField2XML('SourceName',  merge, 1,  current.name)
                PrintField2XML('SourceURL',   merge, 1,  current.url)

        print '</table>'
	return submitter

def DisplayVerificationSourceAdd(submission_id):
	xmlData = SQLloadXML(submission_id)

        print '<table border="2" class="generic_table">'
        submitter = ''
        doc = minidom.parseString(XMLunescape2(xmlData))
        if doc.getElementsByTagName('VerificationSource'):
                merge = doc.getElementsByTagName('VerificationSource')
                submitter = GetElementValue(merge, 'Submitter')

                print '<tr>'
                print '<td class="label"><b>Source Label</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'SourceLabel')
                print '</tr>'

                print '<tr>'
                print '<td class="label"><b>Source Name</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'SourceName')
                print '</tr>'

                print '<tr>'
                print '<td class="label"><b>Source URL</b></td>'
                print '<td class="keep">%s</td>' % GetElementValue(merge, 'SourceURL')
                print '</tr>'
	print '</table>'

	return submitter
