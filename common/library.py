#
#     (C) COPYRIGHT 2007-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import string
import datetime
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node

################################################################
# The routines found here are used across all ISFDB directories.
################################################################

monthmap = {
        1  : 'Jan',
        2  : 'Feb',
        3  : 'Mar',
        4  : 'Apr',
        5  : 'May',
        6  : 'Jun',
        7  : 'Jul',
        8  : 'Aug',
        9  : 'Sep',
        10 : 'Oct',
        11 : 'Nov',
        12 : 'Dec',
}

def validateMonth(string):
        now = datetime.datetime.now()
        # Validate that the passed string is in the YYYY-MM format
        error = "Month must be specified using the YYYY-MM format"
        if len(string ) != 7:
                return (0, 0, error)

        if string[4:5] != '-':
                return (0, 0, error)
        try:
                year=int(string[0:4])
                month=int(string[5:7])
                if (year < 1) or (year > (now.year +1)):
                        return (0, 0 , "Year must be between 1 and one year in the future")
                if (month <1) or (month > 12):
                        return (0, 0 , "Month must be between 01 and 12")
                return (year, month, '')

        except:
                return (0, 0, error)


def normalizeDate(date):
        now = datetime.datetime.now()
        # This function takes a date and normalizes it to be in the standard 'YYYY-MM-DD' format
        # For invalid dates, '0000-00-00' is returned
        date = string.replace(date, "'", '')
        date = string.replace(date, "<", '')
        date = string.replace(date, ">", '')
        date = string.replace(date, " ", '')

        # Check for missing date elements
        if len(date) < 4:
                return '0000-00-00'
        elif len(date) == 4:
                date = '%s-00-00' % date
        elif len(date) == 7:
                date = '%s-00' % date
        elif len(date) != 10:
                return '0000-00-00'

        if (date[4] != '-') or (date[7] != '-'):
                return '0000-00-00'

        # Make sure the date elements are all integers and pass date validation
        try:
                year = int(date[0:4])
                month = int(date[5:7])
                day = int(date[8:10])
                if (year > (now.year +1)) and (year != 8888) and (year != 9999):
                        return '0000-00-00'
                elif month > 12:
                        return '0000-00-00'
                else:
                        # Determine the last day of the specified month. For '00' month, the max day is 31 in MySQL
                        maxday = 31
                        if (month == 4) or (month == 6) or (month == 9) or (month == 11):
                                maxday = 30
                        elif month == 2:
                                maxday = 28
                                leap = 0
                                # Years divisible by 400 are leap years
                                if year % 400 == 0:
                                        leap = 1
                                # Years divisble by 100 but not by 400 are not leap years
                                elif year % 100 == 0:
                                        leap = 0
                                # Years divisible by 4, but not by 100 are leap years
                                elif year % 4 == 0:
                                        leap = 1
                                if leap:
                                        maxday = 29
                        if day > maxday:
                                return '0000-00-00'
        except:
                return '0000-00-00'

        return date

def convertForthcoming(theDate):
	year  = theDate[0:4]
	month = int(theDate[5:7])
	day   = theDate[8:10]
	if month:
		if int(day):
			datestr = "%s %s %s" % (monthmap[month], day, year)
		else:
			datestr = "%s %s" % (monthmap[month], year)
	else:
		datestr = year
	return datestr

def convertYear(date):
        if not date:
                date = '0000'
        year = str(date)[:4]
	if year == '0000':
		yearstr = 'unknown'
	elif year == '8888':
		yearstr = unpublishedDate()
	elif year == '9999':
		yearstr = 'forthcoming'
	else:
		yearstr = year
	return yearstr

def unpublishedDate():
        value = '<span class="hint" title="Announced but never published">unpublished'
        value += '<img src="http://%s/question_mark_icon.gif" alt="Question mark" class="help"></span>' % (HTMLLOC)
        return value

def convertDate(theDate, precise = 0):
	try:
		if theDate == '0000-00-00':
			datestr = 'date unknown'
		elif theDate == '8888-00-00':
			datestr = unpublishedDate()
		elif theDate == '9999-00-00':
			datestr = 'forthcoming'
		elif precise:
                        datestr = theDate
		else:
			month = string.split(theDate, "-")[1]
			if month:
				try:
					strmonth = monthmap[int(month)]
					datestr = "%s %s" % (strmonth, theDate[:4])
				except:
					datestr = theDate[:4]
			else:
				datestr = theDate[:4]
	except:
		datestr = ''
	return datestr


##########################################################################
#  Compare two dates and return:
#    1 if Date 1 is before Date 2
#    2 if Date is more precise than Date 2
#    0 is neither is the case
##########################################################################
def Compare2Dates(date1, date2):
        # If date1 is blank or '0000-00-00', it can't be "before" or "more precise" than date2
        if not date1 or (date1 == '0000-00-00'):
                return 0
        # If date2 is blank or '0000-00-00' and date1 is not (already checked above), then date1 is more precise
        if not date2 or (date2 == '0000-00-00'):
                return 2
        date1_year = date1[0:4]
        date1_month = date1[5:7]
        date1_day = date1[8:10]
        date2_year = date2[0:4]
        date2_month = date2[5:7]
        date2_day = date2[8:10]
        # If the first year is after the second year, then return 0
        if int(date1_year) > int(date2_year):
                return 0
        # If the first year is before the second year, return 1
        if int(date1_year) < int(date2_year):
                return 1
        #
        # If the two years are the same, compare the two months
        #
        # If the month of date1 is unknown, then it's neither more precise nor before date2
        if date1_month == '00':
                return 0
        # If the month of date2 is unknown and the month of date1 is known, then date1 is more precise
        if date2_month == '00':
                return 2
        # If the first month is after the second month, then date1 is not before date2
        if int(date1_month) > int(date2_month):
                return 0
        # If the first month is before the second month, then date1 is before date2
        if int(date1_month) < int(date2_month):
                return 1
        #
        # If the years and months are the same, compare days
        #
        # If date1 is unknown, it's neither before nor more precise than date2
        if date1_day == '00':
                return 0
        # If the day of date2 is unknown and the day of date1 is known, then date1 is more precise
        if date2_day == '00':
                return 2
        if int(date1_day) < int(date2_day):
                return 1
        return 0

def toISBN10(isbn13):
	if len(isbn13) != 13:
		return isbn13
	isbn = isbn13[3:12]
	counter = 0
	sum = 0
	mult = 1
	try:
		while counter < 9:
			sum += (mult * int(isbn[counter]))
			mult += 1
			counter += 1
		remain = sum % 11
		if remain == 10:
			isbn = isbn + 'X'
		else:
			isbn = isbn + str(remain)
		return isbn
	except:
		return isbn13

def toISBN13(isbn):
	if len(isbn) != 10:
		return isbn
	newISBN = '978' + isbn[0:9]

	try:
		sum1 = int(newISBN[0]) + int(newISBN[2]) + int(newISBN[4]) + int(newISBN[6]) + int(newISBN[8]) + int(newISBN[10])
		sum2 = int(newISBN[1]) + int(newISBN[3]) + int(newISBN[5]) + int(newISBN[7]) + int(newISBN[9]) + int(newISBN[11])
		checksum = sum1 + (sum2 * 3)
		remainder = checksum - ((checksum/10)*10)
		if remainder:
			remainder = 10 - remainder
		newISBN = newISBN + str(remainder)
		return newISBN
	except:
		return isbn


def validISBN13(isbn):
	isbn = string.replace(isbn, '-', '')
	isbn = string.replace(isbn, ' ', '')
	if len(isbn) != 13:
		return 0

        try:
                testInt = int(isbn[0:12])
		newISBN = isbn[0:12]
        except:
                return 0

	sum1 = int(newISBN[0]) + int(newISBN[2]) + int(newISBN[4]) + int(newISBN[6]) + int(newISBN[8]) + int(newISBN[10])
	sum2 = int(newISBN[1]) + int(newISBN[3]) + int(newISBN[5]) + int(newISBN[7]) + int(newISBN[9]) + int(newISBN[11])
	checksum = sum1 + (sum2 * 3)
	remainder = checksum - ((checksum/10)*10)
	if remainder:
		remainder = 10 - remainder
	newISBN = newISBN + str(remainder)
	if isbn == newISBN:
		return 1
	else:
		return 0


def validISBN(isbn):
	isbn = string.replace(isbn, '-', '')
	isbn = string.replace(isbn, ' ', '')
	if len(isbn) != 10:
		return validISBN13(isbn)

        # Look for non-integer catalog numbers
        try:
                testInt = int(isbn[0:9])
        except:
                return 0

	counter = 0
	sum = 0
	mult = 1
	while counter < 9:
		sum += (mult * int(isbn[counter]))
		mult += 1
		counter += 1
	remain = sum % 11
        if remain == 10:
                if isbn[9] != 'X':
                        return 0
        else:
                try:
                        lastdigit = int(isbn[9])
                except:
                        return 0
                if lastdigit != remain:
                        return 0
        return 1


def pseudoISBN(isbn):
        isbn = string.replace(isbn, '-', '')
        isbn = string.replace(isbn, ' ', '')
        if (len(isbn) != 10) and (len(isbn) != 13):
                return 0

        counter = 0
        while counter < len(isbn)-1:
                if isbn[counter] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        pass
                else:
                        return 0
		counter += 1

	if isbn[len(isbn)-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']:
		pass
	else:
		return 0
        return 1

def ISBNlength(isbn):
        stripped_isbn = string.replace(isbn, '-', '')
        stripped_isbn = string.replace(isbn, ' ', '')
        return len(stripped_isbn)

##############################################
# Obtains the value associated with a
# particular XML tag.
##############################################
def GetElementValue(element, tag):
	document = element[0].getElementsByTagName(tag)
	try:
		value = document[0].firstChild.data.encode('iso-8859-1')
	except:
		value = ''
	return value

def GetChildValue(doc, label):
	try:
		tag = doc.getElementsByTagName(label)[0]
		value = tag.firstChild.data.encode('iso-8859-1')
	except:
		value = ''
	return value

def XMLunescape(input):
	retval = string.replace(str(input), "&amp;", "&")
	retval = string.replace(retval, "&rsquo;", "'")
	retval = string.replace(retval, "&quot;", '"')
	retval = string.replace(retval, "&lt;", "<")
	retval = string.replace(retval, "&gt;", ">")
        retval = string.strip(retval)
        retval = string.rstrip(retval)
	return retval

def XMLunescape2(input):
	# un-encode quotes
	retval = string.replace(str(input), "&rsquo;", "'")
	retval = string.replace(retval, "&quot;", '"')
	# sometimes we get \r + \n, sometimes just \n.
	# remove any \r instances.
	retval = string.replace(retval, "\r", "")
	# remove leading + trailing spaces
	retval = string.strip(retval)
	retval = string.rstrip(retval)
	return retval

##############################################
# Determines whether or not a particular
# XML tag is present in the given element.
##############################################
def TagPresent(element, tag):
        try:
                document = element.getElementsByTagName(tag)[0]
        except:
                try:
                        document = element[0].getElementsByTagName(tag)
                except:
                        return 0
        if document:
                return 1
        else:
                return 0

def normalizeInput(retval):
        retval = str(retval)
        # First replace ". . . ." with "....", otherwise ". . . ." will be converted to "... ."
        while ". . . ." in retval:
                retval = retval.replace(". . . .", "....")

	###################################################################################
        # Replace and/or remove various characters
	###################################################################################
        replace_dict = {}
        for char in range(0,32):
                # Do not replace carriage return and line feed since they are legal
                if char in (10,13):
                        continue
                # Convert tabs to spaces
                elif char == 9:
                        replace_dict[chr(char)] = ' '
                # Remove all other control characters
                else:
                        replace_dict[chr(char)] = ''
	
        # Replace double spaces with single spaces
        replace_dict['  '] = ' '
        # Replace ". . ." with "..."
        replace_dict['. . .'] = '...'
        # Replace the single ellipsis character with three dots
        replace_dict[chr(133)] = '...'
        # Replace Latin-1 and Unicode punctuation with ASCII equivalents
        replace_dict[chr(130)] = ','
        replace_dict[chr(132)] = '"'
        replace_dict[chr(145)] = "'"
        replace_dict[chr(146)] = "'"
        replace_dict[chr(147)] = '"'
        replace_dict[chr(148)] = '"'
        replace_dict[chr(160)] = ' '

        retval = replaceDict(retval, replace_dict)

        # Next replace characters followed by invalid Unicode characters,
        # including "combining diacritics", with Latin-1 equivalents where
        # available, otherwise decimally HTML-encoded Unicode equivalents
        replace_dict = unicode_translation()
        retval = replaceDict(retval, replace_dict)
	return retval

def replaceDict(retval, replace_dict):
	# Perform the actual replacement
	for key in replace_dict:
                while key in retval:
                        retval = retval.replace(key, replace_dict[key])
	return retval
       

###################################################
# This function converts input, typically from
# an editing form, into a format that can be 
# utilized in an XML structure.
###################################################

def XMLescape(input, compliant = 0):

        retval = normalizeInput(input)

	###########################################
	# Replace the usual ASCII characters with
	# their escaped equivalents for XML
	###########################################
	retval = string.replace(retval, "&", "&amp;")
	# If standards-compliant XML was requested, use &apos;. Internally we use HTML-specific &rsquo; instead (for now)
	if compliant:
        	retval = string.replace(retval, "'", "&apos;")
        else:
                retval = string.replace(retval, "'", "&rsquo;")
	retval = string.replace(retval, '"', "&quot;")
	retval = string.replace(retval, "<", "&lt;")
	retval = string.replace(retval, ">", "&gt;")

	###########################################
	# Sometimes we get \r + \n, sometimes just
	# \n.  Remove all instances of \r.
	###########################################
	retval = string.replace(retval, "\r", "")

	###########################################
	# Strip off leading and trailing spaces
	###########################################
	retval = string.strip(retval)
	retval = string.rstrip(retval)
	return retval

def ISFDBLink(script, record_id, displayed_value, brackets=False, argument='', transliterations = None):
        # Special case: author "uncredited" is displayed without a link for performance reasons
        if script == 'ea.cgi' and displayed_value == 'uncredited':
                return 'uncredited'
        trans_functions = {'ea.cgi': SQLloadTransAuthorNames,
                           'pl.cgi': SQLloadTransPubTitles,
                           'title.cgi': SQLloadTransTitles,
                           'publisher.cgi': SQLloadTransPublisherNames,
                           'pubseries.cgi': SQLloadTransPubSeriesNames
                           }
        trans_function = trans_functions.get(script, None)
        separator = "?"
        if record_id == '':
                separator = ''
        if argument:
                argument += ' '
	link = '<a %shref="http:/%s/%s%s%s" dir="ltr">%s</a>' % (argument, HTFAKE, script, separator, record_id, displayed_value)

        # Transliterated values
	trans_values = None
	# If a list of transliterated values was passed in and contains
	# transliterated values for this record ID, display them
	if transliterations:
                trans_values = transliterations.get(record_id, None)
        # If no list was passed in, but the CGI script is associated with
        # a data retrieval function, use that function to retrieve a list
        # of transliterated values
	elif trans_function:
                trans_values = trans_function(record_id)
        # If transliterated values have been found, add them to the link
        if trans_values:
                link = ISFDBMouseover(trans_values, link, 'span')

	if brackets:
		link = '[%s]' % link
	return link

def ISFDBText(text, escape_quotes = False):
        from cgi import escape
        text = escape(text, escape_quotes)
        if UNICODE != "utf-8":
                text = text.replace("&amp;#","&#")
        return text

def ISFDBPubFormat(format_code):
        formats = {'pb': """Paperback. Typically 7" by 4.25" (18 cm by 11 cm) or smaller, 
                            though trimming errors can cause them to sometimes be slightly
                            (less than 1/4 extra inch) taller or wider/deeper.""",
                   'tp': """Trade paperback. Any softcover book which is at least 7.25"
                            (or 19 cm) tall, or at least 4.5" (11.5 cm) wide/deep.""",
                   'hc': """Hardcover. Used for all hardbacks of any size.""",
                   'ph': """Pamphlet. Used for short (in page count), unbound, staple-bound,
                            or otherwise lightly bound publications.""",
                   'digest': """Books which are similar in size and binding to digest-formatted
                            magazines, using the standard digest size of approximately 7" by 4.5""",
                   'dos': """Dos-a-dos or tete-beche formatted paperback books, such as Ace Doubles
                            and Capra Press back-to-back books.""",
                   'audio CD': "Compact disc with standard audio tracks",
                   'audio MP3 CD': "Compact disc with mp3-encoded audio tracks ",
                   'audio cassette': "Cassette tape",
                   'audio LP': "Long-playing record (vinyl)",
                   'digital audio player': "Player with a pre-loaded digital file of the audiobook",
                   'digital audio download': """Digital recording in any format that is downloaded
                            directly from the Internet. This category includes podcasts.""",
                   'digest': """Digest-size magazine, including both standard digest size, at about
                            7" by 4.5", and also large digest, such as recent issues of Asimov's,
                            which are about 8.25" by 5.125".""",
                   'pulp': """Magazine using the common pulp size: 6.5" by 9.5". For ISFDB purposes
                            this may also be used as a designation for the quality of the paper.
                            There are some untrimmed pulps that are as large as 8" by 11.75""",
                   'bedsheet': """8.5" by 11.25" magazines, e.g. early issues of Amazing; or the
                            1942-43 issues of Astounding.""",
                   'tabloid': """11" by 16" magazine, usually newsprint, e.g. British Science Fiction Monthly.""",
                   'A4': """21 cm by 29.7 cm or 8.3" by 11.7" magazine, used by some UK and European magazines""",
                   'A5': """14.8 cm by 21 cm or 5.8" by 8.3" magazine, used by some UK and European magazines""",
                   'quarto': """8.5" by 11" magazine, usually saddle-stapled, instead of side-stapled or glued""",
                   'octavo': """5.5" by 8.5" magazine, usually saddle-stapled, instead of side-stapled or glued""",
                   'ebook': """Used for all electronic formats, including but not limited to EPUB,
                            eReader, HTML, iBook, Mobipocket, and PDF.""",
                   'webzine': """Used for Internet-based periodical publications which are otherwise
                            not downloadable as an "ebook".""",
                   'other': """The publication format is non-standard. The details are usually provided
                            publication notes.""",
                   'unknown': """The publication record was created from a secondary source and
                            the publication format is unknown."""
                   }
        mouseover_text = formats.get(format_code, '')
        while "\n" in mouseover_text:
                mouseover_text = mouseover_text.replace("\n", " ")
        mouseover_text = normalizeInput(mouseover_text)
       
        if mouseover_text:
                display_value = ISFDBMouseover((mouseover_text,), format_code, 'span')
        else:
                display_value = format_code
        return display_value

class AutoVivification(dict):
        """Emulate Perl's autovivification feature"""
        def __getitem__(self, item):
                try:
                    return dict.__getitem__(self, item)
                except KeyError:
                    value = self[item] = type(self)()
                    return value

def roman2int(roman):
        # Convert a roman numeral to regular integer format
	conversion = { 'm':1000, 'd':500, 'c':100, 'l':50, 'x':10, 'v':5, 'i':1 }
	sum = 0
	roman = roman.lower()
	for i in range(len(roman)):
		if conversion.has_key(roman[i]):
			value = conversion[roman[i]]
		else:
			return 0
		if i < (len(roman)-1):
			if conversion.has_key(roman[i+1]):
				nextvalue = conversion[roman[i+1]]
			else:
				return 0
			if nextvalue > value:
				value *= -1
		sum += value
	return sum

def ConvertPageNumber(page):
        # Returns the page group and the normalized page number for each page. Page groups are:
        #    1 for "no page", 2 for "cover", 3 for "roman", 4 for "arabic", 5 for "back"
	if not page:
		return (1, 0, '')

        # If the page value contains a "pipe" character (|), then everything before the pipe is
        # the display value and the everything after the pipe is the "sort" value
        pipe_list = page.split('|')
        # If there is a pipe, then change the page value to what's to the right of the pipe
        if len(pipe_list) > 1:
                page = pipe_list[1]
        # Re-check the page number now that it may have been repaced with the "sort" value
	if not page:
		return (1, 0, '')
        
	# If the first and last characters are square brackets, remove them
	if page[0] == '[' and page[-1] == ']':
                page = page[1:-1]

	# "fc" means "front cover"
	if page == 'fc':
                return (2, 1, '')

	# "fep" means "front end paper" or inside front cover of a magazine
	if page == 'fep':
                return (2, 2, '')

	# "bp" means "unpaginated pages that precede pagination"
	if page == 'bp':
                return (2, 3, '')

	# "ep" means "unpaginated pages that follow pagination"
	if page == 'ep':
                return (5, 1, '')

        # "bep" means "back end paper" or inside back cover of a magazine
        if page == 'bep':
                return (5, 2, '')

        # "bc" means "back cover"
        if page == 'bc':
                return (5, 3, '')

        # Extract the integer and decimal parts of the page value
        numeric_list = page.split('.')
        if len(numeric_list) > 1:
                integer_part = numeric_list[0]
                decimal_part = numeric_list[1]
        else:
                integer_part = page
                decimal_part = ''

        # Check if the supposed integer part of the page number is really an integer
	try:
		integer_part = int(integer_part)
		return (4, integer_part, decimal_part)
        except:
                # If the supposed integer part is not an integer, check if it's a roman numeral
		integer_part = roman2int(integer_part)
		if integer_part:
			return (3, integer_part, decimal_part)
		# If it's neither an arabic numeral nor a roman numeral, then it is unrecognized, so we will display this page value first
		else:
			return (1, 0, decimal_part)


def getPubContentList(pubid):
	pub_content_list = SQLGetPubContentList(pubid)
	sorted_list = []
	# Build a list of content items with "sort group" and "normalized page number" information
	for pub_content_record in pub_content_list:
                page = pub_content_record[PUB_CONTENTS_PAGE]
                (group, normalized_page, decimal_part) = ConvertPageNumber(page)
                sorted_list.append((group, normalized_page, decimal_part, pub_content_record))
        # Re-sort the list of content items based on group and page number
        sorted_list.sort()
        # Strip intermediate sorting data and build a list of content record in display order
        result = []
        for content_item in sorted_list:
                result.append(content_item[3])
	return result

def getSortedTitlesInPub(pub_id):
        titles = SQLloadTitlesXBT(pub_id)
	title_dict = {}
        for title in titles:
                title_dict[title[TITLE_PUBID]] = title
        sorted_contents = getPubContentList(pub_id)
        new_titles = []
	for content in sorted_contents:
                title_id = content[PUB_CONTENTS_TITLE]
                # Check that the title ID retrieved from the table of contents titles
                # is in the main list of titles for this pub in case of data corruption
                if title_id in title_dict:
                        title = title_dict[title_id]
                        new_titles.append(title)
        return new_titles

def outputGraph(height, startyear, xscale, yscale, years, maximum, results):

	xoffset = 15
	yoffset = 10

	print '<svgcode width="%d" height="%d" version="1.1">' % (xoffset+40+(years*xscale), height+30+yoffset)
	print '<svg width="100%%" height="%dpx" version="1.1" xmlns="http://www.w3.org/2000/svg">' % (height+30+yoffset)

	###################################################
	# Output the grid and labels - Horizontal Lines
	###################################################
	y = 0
	increment = maximum/4
	value = increment * 4
	while y <= height:
		print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:gray;stroke-width:1"/>' % (xoffset, y+yoffset, xoffset+5+(years*xscale), y+yoffset)
		print '<text x="%d" y="%d" font-size="10">%d</text>' % (xoffset+10+(years*xscale), y+5+yoffset, value)
		value -= increment
		y = y + 50

	###################################################
	# Output the grid and labels - Vertical Lines
	###################################################
	x = 0
	while x < years:
		print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:gray;stroke-width:1"/>' % (xoffset+(xscale*x), yoffset, xoffset+(xscale*x), height+10+yoffset)
		print '<text x="%d" y="%d" font-size="10">%d</text>' % ((xscale*x)-12+xoffset, height+20+yoffset, x+startyear)
		x += 10

	###################################################
	# Output the data
	###################################################
        for line_color in results:
                printOneSVGLine(xscale, yscale, years, maximum, results[line_color], xoffset, yoffset, line_color)

	print '</svg>'
	print '</svgcode>'

def printOneSVGLine(xscale, yscale, years, maximum, results, xoffset, yoffset, color):
        index = 0
        last = (0, 0)
        while index < years:
                if index:
                        print '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:2"/>' % (xoffset+(xscale * last[0]), yoffset+(int(yscale * float(last[1]))), xoffset+(xscale * results[index][0]), yoffset+(int(yscale * float(maximum-results[index][1]))), color)
                last = (results[index][0], maximum-results[index][1])
                index += 1

def FormatNote(note, note_type = '', display_mode = 'short', record_id = 0, record_type = ''):
        import urllib
        import re
        if display_mode == 'short' and '{{BREAK}}' in note:
                note = note[:note.index('{{BREAK}}')]
                note += """ ... <big><a class="inverted" href="http:/%s/note.cgi?%s+%d">view
                        full %s</a></big>""" % (HTFAKE, record_type, int(record_id), note_type)
        # Strip {{BREAK}} for full note display mode, but not for edit mode
        if display_mode == 'full' and '{{BREAK}}' in note:
                # Replace {{BREAK}} and any spaces next to it with a single space
                note1 = note[:note.index('{{BREAK}}')].rstrip(' ')
                note2 = note[note.index('{{BREAK}}')+9:].lstrip(' ')
                note = note1 + ' ' + note2

        # Dictionary of supported templates. The structure is:
        #   key = template name
        #   1st tuple value = HTML link
        #   2nd tuple value = displayed name, e.g. the "OCLC" in "OCLC 123456"
        #   3rd tuple value = hover-over display value
        templates = {
                'A': ('http:/%s/se.cgi?arg=%%s&amp;type=Name&amp;mode=exact' % HTFAKE, ),
                'ASIN': ('https://www.amazon.com/dp/%s', 'ASIN',
                         'Amazon Standard Identification Number'),
                'BL': ('http://explore.bl.uk/primo_library/libweb/action/dlDisplay.do?vid=BLVU1&docId=BLL01%s',
                       'BL', 'British Library'),
                'Bleiler1': ('http:/%s/title.cgi?102825' % HTFAKE, 'Bleiler1',
                                   'Science-Fiction: The Gernsback Years by Everett F. Bleiler and Richard J. Bleiler, 1998'),
                'Bleiler78': ('http:/%s/title.cgi?187785' % HTFAKE, 'Bleiler78',
                                   'The Checklist of Science-Fiction and Supernatural Fiction by E. F. Bleiler, 1978'),
                'BNB': ('http://search.bl.uk/primo_library/libweb/action/dlSearch.do?vid=BLBNB&institution=BL&query=any,exact,%s',
                        'BNB', 'British National Bibliography'),
                'BNF': ('http://catalogue.bnf.fr/ark:/12148/%s', 'BNF',
                        'Biblioth&egrave;que nationale de France'),
                'Clute/Grant': ('http:/%s/title.cgi?189435' % HTFAKE, 'Clute/Grant',
                                   'The Encyclopedia of Fantasy, eds. John Clute and John Grant, 1997'),
                'Clute/Nicholls': ('http:/%s/title.cgi?102324' % HTFAKE, 'Clute/Nicholls',
                                   'The Encyclopedia of Science Fiction, 2nd edition, eds. John Clute and Peter Nicholls, 1993'),
                'Contento': ('http://www.philsp.com/homeville/ISFAC/0start.htm', 'Contento',
                                   'Index to Science Fiction Anthologies and Collections, Combined Edition, William G. Contento'),
                'Currey': ('http:/%s/title.cgi?102939' % HTFAKE, 'Currey',
                                   'Science Fiction and Fantasy Authors: A Bibliography of First Printings of Their Fiction and Selected Nonfiction by L. W. Currey, 1979'),
                'DNB': ('http://d-nb.info/%s', 'DNB',
                        'Deutsche Nationalbibliothek'),
                'FantLab': ('https://fantlab.ru/', 'FantLab'),
                'FantLab-author': ('https://fantlab.ru/autor%s', 'FantLab author'),
                'FantLab-pub': ('https://fantlab.ru/edition%s', 'FantLab publication'),
                'FantLab-title': ('https://fantlab.ru/work%s', 'FantLab title'),
                'ISBN': ('%s', 'Additional ISBN'),
                'JNB': ('https://iss.ndl.go.jp/api/openurl?ndl_jpno=%s&locale=en', 'JNB',
                        'Japanese National Bibliography'),
                'LCCN': ('https://lccn.loc.gov/%s', 'LCCN',
                         'Library of Congress Control Number'),
                'Locus1': ('http://www.locusmag.com/index', 'Locus1',
                           'The Locus Index to Science Fiction'),
                'Miller/Contento': ('http:/%s/title.cgi?1088499' % HTFAKE, 'Miller/Contento',
                                   'Science Fiction, Fantasy, & Weird Fiction Magazine Index (1890-2007) by Stephen T. Miller and William G. Contento'),
                'NDL': ('https://id.ndl.go.jp/bib/%s/eng', 'NDL',
                        'National Diet Library'),
                'OCLC': ('http://www.worldcat.org/oclc/%s', 'OCLC',
                         'WorldCat/Online Computer Library Center'),
                'PPN': ('http://picarta.pica.nl/xslt/DB=3.9/XMLPRS=Y/PPN?PPN=%s', 'PPN',
                        'De Nederlandse Bibliografie Pica Productie Nummer'),
                'Publisher': ('http:/%s/se.cgi?arg=%%s&amp;type=Publisher&amp;mode=exact' % HTFAKE, ),
                'Reginald1': ('http:/%s/title.cgi?102834' % HTFAKE, 'Reginald1',
                                   'Science Fiction and Fantasy Literature: A Checklist, 1700-1974 by Robert Reginald, 1979'),
                'Reginald3': ('http:/%s/title.cgi?102835' % HTFAKE, 'Reginald3',
                                   'Science Fiction and Fantasy Literature 1975 - 1991 by Robert Reginald, 1992'),
                'SFBG': ('http://www.sfbg.us', 'SFBG',
                         'Bulgarian SF'),
                'SFBG-pub': ('http://www.sfbg.us/book/%s', 'SFBG publication',
                             'Bulgarian SF - publication'),
                'SFBG-publisher': ('http://www.sfbg.us/publisher/%s', 'SFBG publisher',
                                   'Bulgarian SF - publisher'),
                'SFBG-title': ('http://www.sfbg.us/pubsequence/%s', 'SFBG title',
                               'Bulgarian SF - title'),
                'SFE3': ('http://www.sf-encyclopedia.com/', 'SFE3',
                         'Third Edition of the Encyclopedia of Science Fiction'),
                'Tr': ('%s', 'Translated by'),
                'Tuck': ('http:/%s/pe.cgi?10230' % HTFAKE, 'Tuck',
                                   'The Encyclopedia of Science Fiction and Fantasy through 1968 by Donald H. Tuck, 1974-1982')
                }

        # Substitute templates
        for template in templates:
                dict_node = templates[template]
                template_link = dict_node[0]
                if len(dict_node) > 1:
                        template_name = dict_node[1]
                else:
                        template_name = ''
                if len(dict_node) > 2:
                        template_description = dict_node[2]
                else:
                        template_description = ''
                # Non-record based templates
                if '%s' not in template_link:
                        pattern = "{{"+template+"}}"
                # Record-based templates
                else:
                        pattern = "{{"+template+"\|"
                # Make the regex pattern case-insensitive
                regex = re.compile(pattern, flags=re.I)
                fragments = regex.split(note)
                if '%s' not in template_link:
                        substituted_text = '<a href="%s">%s</a>' % (template_link, template_name)
                        if template_description:
                                substituted_text = '<abbr class="template" title="%s">%s</abbr>' % (template_description, substituted_text)
                        note = substituted_text.join(fragments)
                        continue
                note = ''
                count = 0
                for fragment in fragments:
                        # The first fragment is everything to the left of the first occurrence of this template
                        if not count:
                                note = fragment
                                count += 1
                                continue
                        fragment_pieces = fragment.split('}}')
                        linking_value = fragment_pieces[0]
                        # Create a link only if a linking value was entered
                        if linking_value:
                                # Replace the '%s' in the template link with a URL-escaped version of the linking value
                                actual_link = template_link % urllib.quote(linking_value)
                                # If there is no template name, use the linking value as the display value
                                if not template_name:
                                        display_value = linking_value
                                # If there is a template name, display it first, then display the linking value
                                else:
                                        display_value = '%s %s' % (template_name, linking_value)
                                # For URLs, add the actual link and the display value to the note
                                if template_link[:4] == 'http':
                                        full_value = '<a href="%s">%s</a>' % (actual_link, display_value)
                                else:
                                        full_value = display_value
                                if template_description:
                                        full_value = '<abbr class="template" title="%s">%s</abbr>' % (template_description, full_value)
                                note += full_value
                                        
                        # Add the rest of the original text to the body of the note
                        note += '}}'.join(fragment_pieces[1:])
        
        retval = note

        # Remove all '<!--isfdb specific-->' strings which were used for magazine links in the past
	retval = string.replace(retval, '<!--isfdb specific-->','')
	list_of_brs = ('br', 'br/', 'br /', 'Br', 'Br/', 'Br /', 'BR', 'BR/', 'BR /')
	# Replace double <br>s with <p> (which will be replaced with two newlines later)
	for element in list_of_brs:
                double_element = '<' + element + '>' + '<' + element + '>'
                while double_element in retval:
                        retval = string.replace(retval, double_element, '<p>')
	# Replace HTML <br>s with regular carriage returns
	for element in list_of_brs:
                enclosed_element = '<' + element + '>'
        	retval = string.replace(retval, enclosed_element, '\n')

	# Convert all double carriage returns, which may have resulted from the <br> conversion above, into single carriage returns
	while '\n\n' in retval:
                retval = string.replace(retval, '\n\n', '\n')

        # Remove all carriage returns before and after <p> and <ul> to avoid creating additional displayed new lines
        for element in ('p', '/p', 'ul', 'li', '/li'):
                enclosed = '<' + element + '>'
                enclosed_upper = enclosed.upper()
                prefixed_element = ' ' + enclosed
                while prefixed_element in retval:
                        retval = string.replace(retval, prefixed_element, enclosed)
                suffixed_element = enclosed + ' '
                while suffixed_element in retval:
                        retval = string.replace(retval, suffixed_element, enclosed)
                retval = string.replace(retval, '\n' + enclosed, enclosed)
                retval = string.replace(retval, enclosed + '\n', enclosed)
                retval = string.replace(retval, '\n' + enclosed_upper, enclosed_upper)
                retval = string.replace(retval, enclosed_upper + '\n', enclosed_upper)

	# Replace HTML <p>s with two regular carriage returns
	retval = string.replace(retval, '<p>', '\n\n')
	retval = string.replace(retval, '<P>', '\n\n')

	# Remove leading and trailing spaces (but not newlines)
	retval = string.strip(retval, ' ')

        if note_type:
                retval = '<div class="notes"><b>%s:</b> %s</div>' % (note_type, retval)
        else:
                retval = '<div class="notes">%s</div>' % (retval)
	return retval

def ServerSideRedirect(location):
        print 'Status: 303 See Other'
        print 'Location: %s' % location
        print 'Content-type: text/html; charset=%s\n' % (UNICODE)
	print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
	print '<html lang="en-us">'
	print '<body>'
	print '</body>'
	sys.exit(0)

def SpecialAwards():
        return {
                '71' : 'No Winner -- Insufficient Votes',
                '72' : 'Not on ballot -- Insufficient Nominations',
                '73' : 'No Award Given This Year',
                '81' : 'Withdrawn',
                '82' : 'Withdrawn -- Nomination Declined',
                '83' : 'Withdrawn -- Conflict of Interest',
                '84' : 'Withdrawn -- Official Publication in a Previous Year',
                '85' : 'Withdrawn -- Ineligible',
                '90' : 'Finalists',
                '91' : 'Made First Ballot',
                '92' : "Preliminary Nominees",
                '93' : 'Honorable Mentions',
                '98' : 'Early Submissions',
                '99' : 'Nominations Below Cutoff',
        }

def RecognizedDomains():
        # A dictionary of all "recognized" Web sites and their names
        # The key is the domain name
        # The value is a tuple consiting of the following three values:
        #   1 - the name of the site that will be credited
        #   2 - the URL of the site that will be linked in the credit
        #   3 - 1 if the site has given us permission to link to their images or 0 if it hasn't
        domains = {}
        domains['1632.org'] = ('1632, Inc.', 'www.1632.org', 1)
        domains['amazon.com'] = ('Amazon.com', 'www.amazon.com', 1)
        domains['aozora.gr.jp'] = ('Aozora Bunko', 'www.aozora.gr.jp', 0)
        domains['ansible.co.uk'] = ('Ansible', 'ansible.uk', 0)
        domains['ansible.uk'] = ('Ansible', 'ansible.uk', 0)
        domains['argee.net'] = ('Dr. Robert G. Williscroft', 'argee.net/', 1)
        domains['bookscans.fatcow.com'] = ('Bookscans', 'www.bookscans.com', 1)
        domains['ssl-images-amazon.com'] = ('Amazon.com', 'www.amazon.com', 1)
        domains['images-eu.amazon.com'] = ('Amazon UK', 'www.amazon.co.uk', 1)
        domains['amazon.ca'] = ('Amazon.ca', 'www.amazon.ca', 1)
        domains['armchairfiction.com'] = ('Armchair Fiction', 'www.armchairfiction.com', 1)
        domains['asahi-net.or.jp'] = ('A. E. van Vogt Cover Art Gallery', 'www.asahi-net.or.jp/~we8y-mrt/vanvogt/', 1)
        domains['bestsf.net'] = ('Best SF', 'www.bestsf.net', 0)
        domains['blogspot.com'] = ('Blogspot', 'www.blogger.com', 0)
        domains['bnf.fr'] = ('National Library of France', 'www.bnf.fr', 0)
        domains['bookscans.com'] = ('Bookscans', 'www.bookscans.com', 1)
        domains['chickenlittleagenda.com'] = ('Dr. Robert G. Williscroft', 'chickenlittleagenda.com', 1)
        domains['collectorshowcase.fr'] = ('Collectors Showcase', 'www.collectorshowcase.fr/intro.htm', 1)
        domains['daganbooks.com'] = ('Dagan Books', 'daganbooks.com', 1)
        domains['dbr.nu'] = ('Diamond Bay Research', 'dbr.nu', 1)
        domains['deboekenplank.nl'] = ('De Boekenplank', 'www.deboekenplank.nl', 1)
        domains['downwarden.com'] = ('Black Bed Sheet Books', 'www.downwarden.com', 1)
        domains['dwtr67e3ikfml.cloudfront.net'] = ('Smashwords', 'www.smashwords.com', 1)
        domains['encyklopediafantastyki.pl'] = ('Encyklopedia Fantastyki', 'www.encyklopediafantastyki.pl', 0)
        domains['ericflint.net'] = ('1632, Inc.', 'www.1632.org', 1)
        domains['facebook.com'] = ('Facebook', 'www.facebook.com', 1)
        domains['fancyclopedia.org'] = ('Fancyclopedia 3', 'www.fancyclopedia.org', 0)
        domains['fantascienza.com'] = ('Fantascienza', 'fantascienza.com', 1)
        domains['fantlab.ru'] = ('FantLab', 'fantlab.ru', 1)
        domains['fantasticfiction.com'] = ('Fantastic Fiction', 'fantasticfiction.com', 1)
        domains['fantasticfiction.co.uk'] = ('Fantastic Fiction', 'fantasticfiction.com', 1)
        domains['goodreads.com'] = ('Goodreads', 'goodreads.com', 0)
        domains['grantvillegazette.com'] = ('1632, Inc.', 'www.1632.org', 1)
        domains['gutenberg.org'] = ('Gutenberg', 'gutenberg.org', 0)
        domains['icshi.net'] = ('The Weird Worlds of A. E. van Vogt', 'www.icshi.net/worlds/', 1)
        domains['images-amazon.com'] = ('Amazon.com', 'www.amazon.com', 1)
        domains['imdb.com'] = ('IMDB', 'imdb.com', 0)
        domains['instagram.com'] = ('Instagram', 'instagram.com', 0)
        domains['ivy-bells.com'] = ('Dr. Robert G. Williscroft', 'ivy-bells.com', 1)
        domains['wp.com'] = ('Nitchevo Factory', 'nitchevo.net/', 1)
        domains['isfdb.org'] = ('ISFDB', 'www.isfdb.org', 1)
        domains['kirjasto.sci.fi'] = ('Books and Writers', 'kirjasto.sci.fi', 0)
        domains['librarything.com'] = ('LibraryThing', 'librarything.com', 0)
        domains['linkedin.com'] = ('LinkedIn', 'linkedin.com', 0)
        domains['livejournal.com'] = ('LiveJournal', 'livejournal.com', 0)
        domains['loc.gov'] = ('Library of Congress', 'www.loc.gov', 0)
        domains['locusmag.com'] = ('Locus', 'locusmag.com', 0)
        domains['luminist.org'] = ('The Luminist League', 'www.luminist.org', 1)
        domains['metaphorosis.com'] = ('Metaphorosis', 'www.metaphorosis.com', 1)
        domains['mondourania.com'] = ('Mondourania', 'www.mondourania.com', 1)
        domains['myspace.com'] = ('Myspace', 'myspace.com', 0)
        domains['nasa.gov'] = ('NASA', 'www.nasa.gov', 0)
        domains['nla.gov.au'] = ('National Library of Australia', 'www.nla.gov.au', 0)
        domains['ofearna.us'] = ('Susan O\'Fearna', 'ofearna.us', 1)
        domains['openlibrary.org'] = ('Open Library', 'openlibrary.org', 1)
        domains['people.uncw.edu'] = ('Ace Image library', 'people.uncw.edu/smithms/ACE.html', 1)
        domains['philsp.com'] = ('Galactic Central', 'philsp.com', 1)
        domains['pinterest.com'] = ('Pinterest', 'pinterest.com', 0)
        domains['plus.google.com'] = ('Google+', 'plus.google.com', 0)
        domains['pulpcovers.com'] = ('PulpCovers.com', 'pulpcovers.com', 1)
        domains['relativitybirthdaypresent.com'] = ('Dr. Robert G. Williscroft', 'relativitybirthdaypresent.com', 1)
        domains['riversofwar.com'] = ('1632, Inc.', 'www.1632.org', 1)
        domains['jimrudnick.ca'] = ('Rudnick Press', 'jimrudnick.ca', 1)
        domains['rusf.ru'] = ('Russian SF&F', 'rusf.ru', 0)
        domains['scifiinc.net'] = ('Fan Gallery', 'scifiinc.net', 0)
        domains['sfadb.com'] = ('Science Fiction Awards Database', 'sfadb.com', 0)
        domains['sfcovers.net'] = ('Visco', 'sfcovers.net', 1)
        domains['sff.net'] = ('SFF Net', 'sff.net', 0)
        domains['sf-encyclopedia.com'] = ('SFE3', 'www.sf-encyclopedia.com', 1)
        domains['sf-encyclopedia.uk'] = ('Encyclopedia of Fantasy', 'sf-encyclopedia.uk/fe/', 1)
        domains['sf-encyclopedia.co.uk'] = ('Encyclopedia of Fantasy', 'sf-encyclopedia.uk/fe/', 1)
        domains['sfsite.com'] = ('SF Site', 'www.sfsite.com', 0)
        domains['sfwa.org'] = ('SFWA', 'www.sfwa.org', 0)
        domains['shelfari.com'] = ('Shelfari','', 0)
        domains['slingshotnovel.com'] = ('Dr. Robert G. Williscroft', 'slingshotnovel.com', 1)
        domains['starchildcompact.com'] = ('Dr. Robert G. Williscroft', 'starchildcompact.com', 1)
        domains['thetrashcollector.com'] = ('The Trash Collector', 'www.thetrashcollector.com', 1)
        domains['thrawnrickle.com'] = ('Dr. Robert G. Williscroft', 'thrawnrickle.com', 1)
        domains['tumblr.com'] = ('Tumblr', 'www.tumblr.com', 0)
        domains['twitter.com'] = ('Twitter', 'www.twitter.com', 0)
        domains['uraniamania.com'] = ('Urania Mania', 'www.uraniamania.com', 1)
        domains['vonniewinslowcrist.files.wordpress.com'] = ('Vonnie Winslow Crist', 'vonniewinslowcrist.wordpress.com', 1)
        domains['wattpad.com'] = ('Wattpad', 'www.wattpad.com', 0)
        domains['wikipedia.org'] = ('Wikipedia', 'www.wikipedia.org', 0)
        domains['worldcat.org'] = ('WorldCat', 'www.worldcat.org', 0)
        domains['wordpress.com'] = ('WordPress', 'www.wordpress.com', 0)
        domains['youtube.com'] = ('YouTube', 'www.youtube.com', 0)
        domains['yunchtime.net'] = ('Diamond Bay Research', 'yunchtime.net', 1)
        return domains

def FormatAuthors(authors):
        counter = 0
	output = ''
        for author in authors:
                if counter:
                        output += " <b>and</b> "
		output += ISFDBLink('ea.cgi', author[0], author[1])
                counter += 1
	return output

def AwardLevelDescription(award_level, award_id):
        # Load the award type record for this award
        from awardtypeClass import award_type
        awardType = award_type()
        awardType.award_type_id = award_id
        awardType.load()
        # Retrieve the list of special award levels
        special_awards = SpecialAwards()
        
        if award_level in special_awards:
                award_level_desc = special_awards[award_level]
        elif awardType.award_type_poll == 'Yes':
                award_level_desc = award_level
        else:
                if award_level == '1':
                        award_level_desc = "Win"
                else:
                        award_level_desc = "Nomination"
        return award_level_desc

def DetermineRecordType(recordType, subtype, doc2):
        from xml.dom import minidom
        from xml.dom import Node
        # Since XML tag "NewPub" is used for "New Pub", "Add Pub to Title", "Import Contents", "Export Contents"
        # and "Clone Pub", we need to check the sub-tags inside the XML body to determine the actual type
        if recordType == 'NewPub':
                if GetElementValue(doc2, 'ClonedTo'):
                        recordType = 'ImportExport'
                elif GetElementValue(doc2, 'Parent'):
                        if subtype == MOD_PUB_NEW:
                                recordType = 'AddPub'
                        elif subtype == MOD_PUB_CLONE:
                                recordType = 'ClonePub'
        return recordType

def FormatImage(value, height = 250):
        # If there is a delimiter, only display the part before the delimiter
        image = value.split("|")[0]
        value = '<img src="%s" height="%s" alt="Coverart"><br>[%s]' % (image, height, value)
        return value

def unicode_translation():
##      Possible candidates:
##        '&#699;' : "'",      # Modifier letter turned comma
##        '&#700;' : "'",      # Modified letter apostrophe
        replace = {
                   '&#165;':  chr(165), # Unicode yen changed to Latin-1 yen
                   '&#8192;': ' ',      # En quad space
                   '&#8193;': ' ',      # Em quad space
                   '&#8194;': ' ',      # En space
                   '&#8195;': ' ',      # Em space
                   '&#8196;': ' ',      # Three-per-em space
                   '&#8197;': ' ',      # Four-per-em space
                   '&#8198;': ' ',      # Six-per-em space
                   '&#8199;': ' ',      # Figure space
                   '&#8200;': ' ',      # Punctuation space
                   '&#8201;': ' ',      # Thin space
                   '&#8202;': ' ',      # Hair space
                   '&#8203;': '',       # Zero width space, which we replace with "no character"
                   '&#8206;': '',       # Left-To-Right character
                   '&#8216;': "'",      # Left single quotation mark
                   '&#8217;': "'",      # Right single quotation mark
                   '&#8218;': "'",      # Single low-reverse-9 quotation mark
                   '&#8219;': "'",      # Single high-reverse-9 quotation mark
                   '&#8220;': '"',      # Left double quotation mark
                   '&#8221;': '"',      # Right double quotation mark
                   '&#8222;': '"',      # Double low-reverse-9 quotation mark
                   '&#8223;': '"',      # Double high-reverse-9 quotation mark
                   '&#8230;': '...',    # Horizontal ellipsis
                   '&#8232;': '',       # Line separator
                   '&#8239;': ' ',      # Narrow no-break space
                   '&#8287;': ' ',      # Medium mathematical space
                   '&#12288;':' ',      # Ideographic space
                   '&#65509;':chr(165), # Fullwidth Unicode yen changed to Latin-1 yen
                   'A&#768;': chr(192), # A grave accent
                   'A&#769;': chr(193), # A acute accent
                   'A&#770;': chr(194), # A cirmuflex accent
                   'A&#771;': chr(195), # A tilde
                   'A&#772;': '&#256;', # A macron
                   'A&#774;': '&#258;', # A breve
                   'A&#775;': '&#550;', # A dot above
                   'A&#776;': chr(196), # A diaresis/umlaut
                   'A&#778;': chr(197), # A ring above
                   'A&#780;': '&#461;', # A caron
                   'A&#783;': '&#512;', # A double grave
                   'A&#785;': '&#514;', # A inverted breve
                   'A&#808;': '&#260;', # A ogonek
                   'C&#769;': '&#262;', # C acute accent
                   'C&#770;': '&#264;', # C cirmuflex accent
                   'C&#775;': '&#266;', # C dot above
                   'C&#780;': '&#268;', # C caron
                   'C&#807;': chr(199), # C cedilla
                   'D&#780;': '&#270;', # D caron
                   'E&#768;': chr(200), # E grave accent
                   'E&#769;': chr(201), # E acute accent
                   'E&#770;': chr(202), # E cirmuflex accent
                   'E&#772;': '&#274;', # E macron
                   'E&#774;': '&#276;', # E breve
                   'E&#775;': '&#278;', # E dot above
                   'E&#776;': chr(203), # E diaresis/umlaut
                   'E&#780;': '&#282;', # E caron
                   'E&#783;': '&#516;', # E double grave
                   'E&#785;': '&#518;', # E inverted breve
                   'E&#807;': '&#552;', # E cedilla
                   'E&#808;': '&#280;', # E ogonek
                   'G&#769;': '&#500;', # G acute accent
                   'G&#770;': '&#284;', # G cirmuflex accent
                   'G&#774;': '&#286;', # G breve
                   'G&#775;': '&#288;', # G dot above
                   'G&#780;': '&#486;', # G caron
                   'G&#807;': '&#290;', # G cedilla
                   'H&#770;': '&#292;', # H cirmuflex accent
                   'H&#780;': '&#542;', # H caron
                   'I&#768;': chr(204), # I grave accent
                   'I&#769;': chr(205), # I acute accent
                   'I&#770;': chr(206), # I cirmuflex accent
                   'I&#771;': '&#296;', # I tilde
                   'I&#772;': '&#298;', # I macron
                   'I&#774;': '&#300;', # I breve
                   'I&#775;': '&#304;', # I dot above
                   'I&#776;': chr(207), # I diaresis/umlaut
                   'I&#780;': '&#463;', # I caron
                   'I&#783;': '&#520;', # I double grave
                   'I&#785;': '&#522;', # I inverted breve
                   'I&#808;': '&#302;', # I ogonek
                   'J&#770;': '&#308;', # J cirmuflex accent
                   'K&#780;': '&#488;', # K caron
                   'K&#807;': '&#310;', # K cedilla
                   'L&#769;': '&#313;', # L acute accent
                   'L&#780;': '&#317;', # L caron
                   'L&#807;': '&#315;', # L cedilla
                   'N&#768;': '&#504;', # N grave accent
                   'N&#769;': '&#323;', # N acute accent
                   'N&#771;': chr(209), # N tilde
                   'N&#775;': '&#7748;', # N dot above
                   'N&#780;': '&#327;', # N caron
                   'N&#807;': '&#325;', # N cedilla
                   'O&#768;': chr(210), # O grave accent
                   'O&#769;': chr(211), # O acute accent
                   'O&#770;': chr(212), # O cirmuflex accent
                   'O&#771;': chr(213), # O tilde
                   'O&#772;': '&#332;', # O macron
                   'O&#774;': '&#334;', # O breve
                   'O&#775;': '&#558;', # O dot above
                   'O&#776;': chr(214), # O diaresis/umlaut
                   'O&#779;': '&#336;', # O double acute
                   'O&#780;': '&#465;', # O caron
                   'O&#783;': '&#524;', # O double grave
                   'O&#785;': '&#526;', # O inverted breve
                   'O&#808;': '&#490;', # O ogonek
                   'R&#769;': '&#340;', # R acute accent
                   'R&#780;': '&#344;', # R caron
                   'R&#783;': '&#528;', # R double grave
                   'R&#785;': '&#530;', # R inverted breve
                   'R&#807;': '&#342;', # R cedilla
                   'S&#769;': '&#346;', # S acute accent
                   'S&#770;': '&#348;', # S cirmuflex accent
                   'S&#780;': '&#352;', # S caron
                   'S&#806;': '&#536;', # S comma below
                   'S&#807;': '&#350;', # S cedilla
                   'T&#780;': '&#356;', # T caron
                   'T&#806;': '&#538;', # T comma below
                   'T&#807;': '&#354;', # T cedilla
                   'U&#768;': chr(217), # U grave accent
                   'U&#769;': chr(218), # U acute accent
                   'U&#770;': chr(219), # U cirmuflex accent
                   'U&#771;': '&#360;', # U tilde
                   'U&#772;': '&#362;', # U macron
                   'U&#774;': '&#364;', # U breve
                   'U&#776;': chr(220), # U diaresis/umlaut
                   'U&#778;': '&#366;', # U ring above
                   'U&#779;': '&#368;', # U double acute
                   'U&#780;': '&#467;', # U caron
                   'U&#783;': '&#532;', # U double grave
                   'U&#785;': '&#534;', # U inverted breve
                   'U&#808;': '&#370;', # U ogonek
                   'W&#770;': '&#372;', # W cirmuflex accent
                   'Y&#769;': chr(221), # Y acute accent
                   'Y&#770;': '&#374;', # Y cirmuflex accent
                   'Y&#776;': '&#376;', # Y diaresis/umlaut
                   'Y&#772;': '&#562;', # Y macron
                   'Z&#769;': '&#377;', # Z acute accent
                   'Z&#775;': '&#379;', # Z dot above
                   'Z&#780;': '&#381;', # Z caron
                   'a&#768;': chr(224), # a grave accent
                   'a&#769;': chr(225), # a acute accent
                   'a&#770;': chr(226), # a cirmuflex accent
                   'a&#771;': chr(227), # a tilde
                   'a&#772;': '&#257;', # a macron
                   'a&#774;': '&#259;', # a breve
                   'a&#775;': '&#551;', # a dot above
                   'a&#776;': chr(228), # a diaresis/umlaut
                   'a&#778;': chr(229), # a ring above
                   'a&#780;': '&#462;', # a caron
                   'a&#783;': '&#513;', # a double grave
                   'a&#785;': '&#515;', # a inverted breve
                   'a&#808;': '&#261;', # a ogonek
                   'c&#769;': '&#263;', # c acute accent
                   'c&#770;': '&#265;', # c cirmuflex accent
                   'c&#775;': '&#267;', # c dot above
                   'c&#780;': '&#269;', # c caron
                   'c&#807;': chr(231), # c cedilla
                   'd&#780;': '&#271;', # d caron (displayed as an apostrophe)
                   'e&#768;': chr(232), # e grave accent
                   'e&#769;': chr(233), # e acute accent
                   'e&#770;': chr(234), # e cirmuflex accent
                   'e&#772;': '&#275;', # e macron
                   'e&#774;': '&#277;', # e breve
                   'e&#775;': '&#279;', # e dot above
                   'e&#776;': chr(235), # e diaresis/umlaut
                   'e&#780;': '&#283;', # e caron
                   'e&#783;': '&#517;', # e double grave
                   'e&#785;': '&#519;', # e inverted breve
                   'e&#807;': '&#553;', # e cedilla
                   'e&#808;': '&#281;', # e ogonek
                   'g&#769;': '&#501;', # g acute accent
                   'g&#770;': '&#285;', # g cirmuflex accent
                   'g&#774;': '&#287;', # g breve
                   'g&#775;': '&#289;', # g dot above
                   'g&#780;': '&#487;', # g caron
                   'g&#807;': '&#291;', # g cedilla
                   'h&#770;': '&#293;', # h cirmuflex accent
                   'h&#780;': '&#543;', # h caron
                   'i&#768;': chr(236), # i grave accent
                   'i&#769;': chr(237), # i acute accent
                   'i&#770;': chr(238), # i cirmuflex accent
                   'i&#771;': '&#297;', # i tilde
                   'i&#772;': '&#299;', # i macron
                   'i&#774;': '&#301;', # i breve
                   'i&#776;': chr(239), # i diaresis/umlaut
                   'i&#780;': '&#464;', # i caron
                   'i&#783;': '&#521;', # i double grave
                   'i&#785;': '&#523;', # i inverted breve
                   'i&#808;': '&#303;', # i ogonek
                   'j&#770;': '&#309;', # j cirmuflex accent
                   'j&#780;': '&#496;', # j caron
                   'k&#780;': '&#489;', # k caron
                   'k&#807;': '&#311;', # k cedilla
                   'l&#769;': '&#314;', # l acute accent
                   'l&#780;': '&#318;', # L caron
                   'l&#807;': '&#316;', # l cedilla
                   'n&#768;': '&#505;', # n grave accent
                   'n&#769;': '&#324;', # n acute accent
                   'n&#771;': chr(241), # n tilde
                   'n&#775;': '&#7749;', # n dot above
                   'n&#780;': '&#328;', # n caron
                   'n&#807;': '&#326;', # n cedilla
                   'o&#768;': chr(242), # o grave accent
                   'o&#769;': chr(243), # o acute accent
                   'o&#770;': chr(244), # o cirmuflex accent
                   'o&#771;': chr(245), # o tilde
                   'o&#772;': '&#333;', # o macron
                   'o&#774;': '&#335;', # o breve
                   'o&#775;': '&#559;', # o dot above
                   'o&#776;': chr(246), # o diaresis/umlaut
                   'o&#779;': '&#337;', # o double acute
                   'o&#780;': '&#466;', # o caron
                   'o&#783;': '&#525;', # o double grave
                   'o&#785;': '&#527;', # o inverted breve
                   'o&#808;': '&#491;', # o ogonek
                   'r&#769;': '&#341;', # r acute accent
                   'r&#780;': '&#345;', # r caron
                   'r&#783;': '&#529;', # r double grave
                   'r&#785;': '&#531;', # r inverted breve
                   'r&#807;': '&#343;', # r cedilla
                   's&#769;': '&#347;', # s acute accent
                   's&#770;': '&#349;', # s cirmuflex accent
                   's&#780;': '&#353;', # s caron
                   's&#806;': '&#537;', # s comma below
                   's&#807;': '&#351;', # s cedilla
                   't&#780;': '&#357;', # t caron
                   't&#806;': '&#539;', # t comma below
                   't&#807;': '&#355;', # t cedilla
                   'u&#768;': chr(249), # u grave accent
                   'u&#769;': chr(250), # u acute accent
                   'u&#770;': chr(251), # u cirmuflex accent
                   'u&#771;': '&#361;', # u tilde
                   'u&#772;': '&#363;', # u macron
                   'u&#774;': '&#365;', # u breve
                   'u&#776;': chr(252), # u diaresis/umlaut
                   'u&#778;': '&#367;', # u ring above
                   'u&#779;': '&#369;', # u double acute
                   'u&#780;': '&#468;', # u caron
                   'u&#783;': '&#533;', # u double grave
                   'u&#785;': '&#535;', # u inverted breve
                   'u&#808;': '&#371;', # u ogonek
                   'w&#770;': '&#373;', # w cirmuflex accent
                   'y&#769;': chr(253), # y acute accent
                   'y&#770;': '&#375;', # y cirmuflex accent
                   'y&#772;': '&#563;', # y macron
                   'y&#776;': chr(255), # y diaresis/umlaut
                   'z&#769;': '&#378;', # z acute accent
                   'z&#775;': '&#380;', # z dot above
                   'z&#780;': '&#382;'  # z caron
                   }
        return replace

def badUnicodePatternMatch(field_name):
        unicode_map = unicode_translation()
        pattern_match = ''
        for key in unicode_map:
                if pattern_match:
                        pattern_match += ' or '
                pattern_match += "%s like binary '%%%s%%'" % (field_name, key)
        return pattern_match

def suspectUnicodePatternMatch(field_name):
        unicode_map = ('&#699;', '&#700;')
        pattern_match = ''
        for key in unicode_map:
                if pattern_match:
                        pattern_match += ' or '
                pattern_match += "%s like '%%%s%%'" % (field_name, key)
        return pattern_match

def dict_to_in_clause(id_dict_1, id_dict_2 = None):
        # Convert the keys of up to 2 dictionaries to a SQL 'IN' clause
        id_list = []
        for record_id in id_dict_1:
                id_list.append(record_id)
        if id_dict_2:
                for record_id in id_dict_2:
                        id_list.append(record_id)
        in_clause = list_to_in_clause(id_list)
        return in_clause

def list_to_in_clause(id_list):
        in_clause = ''
        for id_value in id_list:
                id_string = str(id_value)
                if not in_clause:
                        in_clause = "'%s'" % id_string
                else:
                        in_clause += ",'%s'" % id_string
        return in_clause

def ISFDBMouseover(mouseover_values, display_value, tag = 'td'):
        # Adds a mouseover bubble with the specified list of values to
        # the displayed text/link and returns the composite string.
        # Supports different HTML tags, typically <td> and <span>.

        if not mouseover_values:
                if tag == 'td':
                        return '<td>%s</td>' % display_value
                else:
                        return display_value
        display = '<%s class="hint" title="' % tag
        count = 0
        for mouseover_value in mouseover_values:
                if count:
                        display += '&#13;'
                # Append the HTML-escaped version of the mouseover value
                display += ISFDBText(mouseover_value, 1)
                count += 1
        display += '">%s<sup class="mouseover">%s</sup></%s>' % (display_value, QUESTION_MARK, tag)
        return display

def validateURL(url):
        from urlparse import urlparse
        parsed_url = urlparse(url)
        if parsed_url[0] not in ('http', 'https'):
                return 0
        else:
                return 1

def WikiExists():
        query = """select count(*) from information_schema.tables
                where table_schema = 'isfdb' and table_name = 'mw_page'"""
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	if record[0][0]:
                return 1
        else:
                return 0

def WikiLink(user_name):
        output = '<a href="http://%s/index.php/User:%s">%s</a>' % (WIKILOC, user_name, user_name)
        output += ' <a href="http://%s/index.php/User_Talk:%s">(Talk)</a>' % (WIKILOC, user_name)
        return output

def popularNonLatinLanguages(types):
        # Each language is associated with a tuple of report IDs.
        # The first number in the tuple is the report ID of the
        # title-specific cleanup report. The second number is the
        # report ID of the publication-specific cleanup report.
        languages = {
                   'Bulgarian': (138, 162, 183),
                   'Chinese': (139, 163, 184),
                   'Greek': (140, 164, 185),
                   'Japanese': (141, 165, 186),
                   'Russian': (142, 166, 187)
                   }
        if types == 'titles':
                position = 0
        elif types == 'pubs':
                position = 1
        elif types == 'authors':
                position = 2
        else:
                raise
        results = []
        for language in languages:
                report_ids = languages[language]
                report_id = report_ids[position]
                results.append((language, report_id))
        return results

def transliteratedReports(types):
        # Each language is associated with a tuple of report IDs.
        # The first number in the tuple is the report ID of the
        # title-specific cleanup report. The second number is the
        # report ID of the publication-specific cleanup report.
        # The third number is the report ID of the author-specific
        # cleanup report.
        languages = {
                   'Bulgarian': (124, 148, 169),
                   'Chinese': (125, 149, 170),
                   'Czech': (126, 150, 171),
                   'English': (127, 151, 172),
                   'Greek': (128, 152, 173),
                   'Hungarian': (129, 153, 174),
                   'Japanese': (130, 154, 175),
                   'Lithuanian': (131, 155, 176),
                   'Polish': (132, 156, 177),
                   'Romanian': (133, 157, 178),
                   'Russian': (134, 158, 179),
                   'Serbian': (135, 159, 180),
                   'Turkish': (136, 160, 181)
                   }
        if types == 'titles':
                position = 0
        elif types == 'pubs':
                position = 1
        elif types == 'authors':
                position = 2
        else:
                raise
        results = []
        for language in languages:
                report_ids = languages[language]
                report_id = report_ids[position]
                results.append((language, report_id))
        return results

def LIBprintISFDBtime():
        print '<p><b>Current ISFDB time:</b> %s' % str(datetime.datetime.now()).split('.')[0]

def printSubmissionTable(status):
        LIBprintISFDBtime()
        print '<table class="generic_table">'
        print '<tr align="left" class="generic_table_header">'
        print '<th>Submission</th>'
        print '<th>Type</th>'
        print '<th>Time Submitted</th>'
        print '<th>Submitter</th>'
        if status in ('I', 'R'):
                print '<th>Time Reviewed</th>'
        if status == 'N':
                print '<th>Holder</th>'
        else:
                print '<th>Moderator</th>'
        print '<th>Affected Record</th>'
        if status == 'R':
                print '<th>Reason</th>'
        elif status == 'N':
                print '<th>Cancel</th>'
        print '</tr>'

def printSubmissionRecord(record, eccolor, status):
	if eccolor:
		print '<tr align=left class="table1">'
	else:
		print '<tr align=left class="table2">'

        subType=record[0][SUB_TYPE]
        subTypeName=SUBMAP[subType][1]
        subId=record[0][SUB_ID]

        print '<td><a href="http:/%s/view_submission.cgi?%s">%s</a></td>' % (HTFAKE, subId, subId)

        try:
                doc = minidom.parseString(XMLunescape2(record[0][SUB_DATA]))
                doc2 = doc.getElementsByTagName(subTypeName)
                displayName = DetermineRecordType(subTypeName, subType, doc2)
                (subjectLink, new_record) = getSubjectLink(record[0], doc2, subType)
                submitter = GetElementValue(doc2, 'Submitter')
                submitter = string.replace(submitter, ' ', '_')
        except:
                subjectLink = '<b>XML PARSE ERROR</b>'
                submitter = SQLgetUserName(record[0][SUB_SUBMITTER])
        try:
                if displayName:
                        pass
        except:
                displayName = 'Unable to determine'

        print '<td>%s</td>' % displayName

        print '<td>%s</td>' % record[0][SUB_TIME]

	print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, submitter, submitter)

	if record[0][SUB_REVIEWED]:
		print '<td>%s</td>' % record[0][SUB_REVIEWED]

	if record[0][SUB_REVIEWER]:
                approver = SQLgetUserName(record[0][SUB_REVIEWER])
                print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, approver, approver)
        elif record[0][SUB_HOLDID]:
                holder = SQLgetUserName(record[0][SUB_HOLDID])
                print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, holder, holder)
        else:
                print '<td>&nbsp;</td>'

        print '<td><i>%s</i></td>' % subjectLink

        if status == 'R':
                if record[0][SUB_REASON]:
                        print '<td>%s</td>' % record[0][SUB_REASON]
                else:
                        print '<td>-</td>'
        elif status == 'N':
                print '<td><a href="http:/%s/cancelsubmission.cgi?%d">Cancel submission</a></td>' % (HTFAKE, subId)
        
        print '</tr>'

def getSubjectLink(record, doc2, subType):
        subject = GetElementValue(doc2, 'Subject')
        if record[SUB_NEW_RECORD_ID]:
                recordNum = record[SUB_NEW_RECORD_ID]
                new_record = 1
        else:
                recordNum = GetElementValue(doc2, SUBMAP[subType][4])
                new_record = 0
                # Since 'NewPub' is used for "New Pub", "Add Pub to Title", "Import Contents", "Export Contents"
                # and "Clone Pub", we need to check the sub-tags inside the XML to determine the record number
                if subType in (MOD_TITLE_MERGE, MOD_PUBLISHER_MERGE, MOD_AUTHOR_MERGE):
                        recordNum = GetElementValue(doc2, 'KeepId')
                elif subType == MOD_VARIANT_TITLE:
                        recordNum = GetElementValue(doc2, 'Parent')
                elif subType == MOD_PUB_CLONE:
                        recordNum = GetElementValue(doc2, 'ClonedTo')
        subjectLink=subject[:40]
        # This value is None for data deletion submissions since there is no record left to link to
        displayPage = SUBMAP[subType][2]
        if recordNum and displayPage: 
                subjectLink='<a href="http:/%s/%s?%s">%s</a>' % (HTFAKE, displayPage, recordNum, subjectLink)
        return (subjectLink, new_record)

def AdvSearchLink(params):
        link = '<a href="http:/%s/adv_search_results.cgi?START=0%s">' % (HTFAKE, EscapeParams(params))
        return link

def EscapeParams(params):
        import urllib
        param_string = ''
        for param in params:
                param_string += '&amp;%s=%s' % (urllib.quote(param[0]), urllib.quote(param[1]))
        return param_string

def printRecordID(record_type, record_id, user_id, user = None):
	output = '<span style="float:right"><b>%s Record # </b>%d' % (record_type, int(record_id))
	if user_id:
                cgi_scripts = {'Publication': 'editpub',
                               'Title': 'edittitle',
                               'Author': 'editauth',
                               'Series': 'editseries',
                               'Publisher': 'editpublisher',
                               'Pub. Series': 'editpubseries',
                               'Award': 'editaward',
                               'Award Category': 'editawardcat',
                               'Award Type': 'editawardtype'
                               }
                if record_type in cgi_scripts:
                        cgi_script = cgi_scripts[record_type]
                        edit_mode = 1
                        if record_type in ('Award Category', 'Award Type'):
                                user.load_moderator_flag()
                                if not user.moderator:
                                        edit_mode = 0
                        if edit_mode:
                                output += ' [<a href="http:/%s/edit/%s.cgi?%d">Edit</a>]' % (HTFAKE, cgi_script, int(record_id))
        output += '</span>'
        print output

def valid_html_tags():
        paired_tags = ['b', 'i', 'u', 'ol', 'ul', 'em', 'li', 'p', 'table', 'th',
                       'tr', 'td', 'cite', 'sub', 'sup', 'span', 'blockquote', 'pre',
                       'h1', 'h2', 'h3', 'strong', 'abbr', 'center', 'del', 'tbody',
                       'caption', 'q', 's', 'small']
        self_closing_tags = ['p', 'br', '!--isfdb specific--', 'hr']
        tags_with_attributes = ['a', 'table', 'tr', 'td', 'th']

        valid_tags = []
        for tag in paired_tags:
                valid_tags.append('<%s>' % tag)
                valid_tags.append('</%s>' % tag)
        for tag in self_closing_tags:
                valid_tags.append('<%s>' % tag)
                valid_tags.append('<%s/>' % tag)
                valid_tags.append('<%s />' % tag)
        for tag in tags_with_attributes:
                valid_tags.append('<%s ' % tag)
                valid_tags.append('</%s>' % tag)
        return valid_tags

def BadHtmlClause(field_name):
        valid_tags = valid_html_tags()
        query = '(('
        for tag in valid_tags:
                query += "replace("
        query += "lower(%s)," % field_name
        for tag in valid_tags:
                query += "'%s','')," % tag
        query = query[:-1] + " like '%<%') "
        query += "or (%s like '%%<a href%%' and %s not like '%%<a href=%%'))" % (field_name, field_name)
        return query

def FormatExternalIDType(type_name, types):
        formatted_type = ''
        for type_number in types:
                if types[type_number][0] == type_name:
                        type_full_name = types[type_number][1]
                        formatted_type = '<abbr class="template" title="%s">%s</abbr>:' % (type_full_name, type_name)
                        break
        return formatted_type

def FormatExternalIDSite(sites, type_id, id_value):
        site_count = 0
        for site in sites:
                if site[IDSITE_TYPE_ID] == type_id:
                        site_count += 1
                        url = site[IDSITE_URL]
        if site_count == 1:
                formatted_id = ' %s' % FormatExternalIDLink(url, id_value, id_value)
        else:
                formatted_id = ' %s (' % id_value
                for site in sites:
                        if site[IDSITE_TYPE_ID] == type_id:
                                if formatted_id[-1] != '(':
                                        formatted_id += ' '
                                formatted_id += FormatExternalIDLink(site[IDSITE_URL], id_value, site[IDSITE_NAME])
                formatted_id += ')'
        return formatted_id

def FormatExternalIDLink(url, value, display_value):
        return '<a href="%s" target="_blank">%s</a>' % (url % string.replace(value,' ',''), display_value)

def LIBsameParentAuthors(title):
        pseudonym = 0
        if title[TITLE_PARENT]:
                parentauthors = SQLTitleAuthors(title[TITLE_PARENT])
                pseudonymauthors = SQLTitleAuthors(title[TITLE_PUBID])
                if set(parentauthors) != set(pseudonymauthors):
                        pseudonym = 1
        return pseudonym
