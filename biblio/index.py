#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Ahasuerus, Uzume and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from SQLparsing import *
from library import ISFDBLink, ISFDBText, ISFDBPubFormat
from time import gmtime
from common import displayAuthorList, PrintHeader, PrintNavbar, PrintTrailer
from calendarClass import CalendarDay
from isbn import convertISBN


def displayLinks():
        print '<p class="bottomlinks">\n%s\n%s Note: Forthcoming books may be delayed due to the Coronavirus pandemic' % (
                ISFDBLink("fc.cgi", "", "View All Forthcoming Books", argument='class="inverted"'),
                ISFDBLink("stats.cgi?24", "", "View Top Forthcoming", argument='class="inverted"')
                )
	return

if __name__ == '__main__':

	PrintHeader('The Internet Speculative Fiction Database')
	PrintNavbar('frontpage', 0, 0, 'index.cgi', 0)

	print 'The <i><b>ISFDB</b></i> is a community effort to catalog works of science '
	print 'fiction, fantasy, and horror. '
	print 'It links together various types of bibliographic data: author bibliographies, '
	print 'publication bibliographies, award listings, magazine content listings, anthology '
	print 'and collection content listings, and forthcoming books.'

        # Authors who were born and died on this day
        calendar_day = CalendarDay()
        calendar_day.padded_day = todaysDate()
        calendar_day.print_authors_section()
	# Forthcoming Books
	displayLinks()
	print '<div class="divider">'
	print '<b>Selected Forthcoming Books:</b>'
	print '</div>'

	print '<div id="Intro">'
	print '<table>'

        date = gmtime()
        month = date[1]
        day = date[2]
        year  = str(date[0])
	booksPrinted = 0
	maxmonths = 0
	leftcolumn = 1
	maxBooks = 21
	titles = []

	while booksPrinted <= maxBooks:

		results = SQLGetForthcoming(month, year, day, 0)

		maxmonths += 1
		if maxmonths > 2:
			break

		for result in results:

			if result[PUB_CTYPE] == 'MAGAZINE':
				continue
			if result[PUB_CTYPE] == 'FANZINE':
				continue
			if not result[PUB_IMAGE]:
				continue

			if SQLMarqueAuthors(result[PUB_PUBID]):
                                # Retrieve the book's referral title
                                title_id = SQLgetTitleReferral(result[PUB_PUBID], result[PUB_CTYPE])
                                # If we have already printed a publication for this title, don't print another one
                                if title_id in titles:
                                        continue
                                # Add this referral title to the list of displayed titles
                                titles.append(title_id)
				booksPrinted += 1

				if leftcolumn:
					print '<tr>'

                                image_source = result[PUB_IMAGE].split("|")[0]
                                alt_name = 'Book Image'
                                print '<td><img src="%s" class="covermainpage" alt="%s"></td>' % (image_source, alt_name)
				outstr = result[PUB_YEAR][5:7] +'/'+ result[PUB_YEAR][8:10] + ' - '
				outstr += ISFDBLink("pl.cgi", result[PUB_PUBID],
                                                    '<span class="forthcoming">%s</span>' % ISFDBText(result[PUB_TITLE])) + " ("
				if result[PUB_PUBLISHER]:
					publisher = SQLGetPublisher(result[PUB_PUBLISHER])
					outstr += ISFDBLink('publisher.cgi', publisher[PUBLISHER_ID], publisher[PUBLISHER_NAME])

				if result[PUB_ISBN]:
					outstr += ", " +convertISBN(result[PUB_ISBN])

				if result[PUB_PRICE]:
					outstr += ", "+result[PUB_PRICE]

				if result[PUB_PAGES]:
                                        outstr += ", %spp" % result[PUB_PAGES]

				if result[PUB_PTYPE]:
                                        outstr += ", " + ISFDBPubFormat(result[PUB_PTYPE], 'left')

				if result[PUB_CTYPE]:
						outstr += ', %s' % result[PUB_CTYPE].lower()
				outstr += ') by '

				print '<td>%s' % outstr
                                authors = SQLPubBriefAuthorRecords(result[PUB_PUBID])
                                displayAuthorList(authors)
				print '</td>'
				if leftcolumn:
					leftcolumn = 0
				else:
					print '</tr>'
					leftcolumn = 1
				if booksPrinted > maxBooks:
					# Break out of the results FOR loop
					break
		month += 1
		day = '1'
		if month > 12:
			month = 1
			Iyear = int(year)+1
			year = str(Iyear)

	if leftcolumn == 0:
		print '</tr>'
		print '<tr>'
		print '<td></td>'
		print '<td></td>'
		print '</tr>'
	print '</table>'
	print '</div>'
	displayLinks()

	PrintTrailer('frontpage', 0, 0)
