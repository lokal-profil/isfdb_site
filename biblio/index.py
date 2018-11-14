#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2018   Al von Ruff, Ahasuerus, Uzume and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import os
import string
from SQLparsing import *
from biblio import *
from time import *
from common import *


def printAuthorList(authors):
        print '<td>'
	if authors:
                print '<ul>'
                for author in authors:
                        print '<li>%s %s' % (ISFDBLink('ea.cgi', author[AUTHOR_ID], author[AUTHOR_CANONICAL]), lifeSpan(author))
                print '</ul>'
        print '</td>'

def lifeSpan(author):
        birthyear = author[AUTHOR_BIRTHDATE]
        if birthyear:
                birthyear = birthyear[:4]
        if birthyear == '0000':
                birthyear = 'unknown'

        deathyear = author[AUTHOR_DEATHDATE]
        if deathyear:
                deathyear = deathyear[:4]
        if deathyear == '0000':
                deathyear = 'unknown'

        if deathyear:
                lifespan = " (%s-%s)" % (birthyear, deathyear)
        else:
                lifespan = " (%s)" % birthyear
        return lifespan

def displayLinks():
        print '<p class="bottomlinks">\n%s\n%s' % (
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

        print '<table class="mainauthors">'
        print '<tr>'
        print '<td class="dividerrow"><b>Authors Born On This Day:</b></td>'
        print '<td class="dividerrow"><b>Authors Who Died On This Day:</b></td>'
        print '</tr>'
	########################################################
	# Authors born today
	########################################################
	print '<tr>'
	authors = SQLbornToday()
	printAuthorList(authors)

        ########################################################
        # Authors who died today
        ########################################################
        authors = SQLdiedToday()
	printAuthorList(authors)
        print '</tr>'
        print '</table>'

	########################################################
	# Forthcoming Books section
	########################################################
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
		if maxmonths > 11:
			break

		for result in results:

			if result[PUB_CTYPE] == 'MAGAZINE':
				continue
			if result[PUB_CTYPE] == 'FANZINE':
				continue
			if result[PUB_IMAGE] == '':
				continue

			if SQLMarqueAuthors(result[PUB_PUBID]):
                                from isbn import convertISBN
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

				if result[PUB_IMAGE]:
                                        image_source = result[PUB_IMAGE].split("|")[0]
                                        alt_name = 'Book Image'
                                else:
                                        image_source = 'http://%s/NoImage.gif' % HTMLLOC
                                        alt_name = 'No Image'
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
					if result[PUB_PTYPE] == 'hc':
						outstr += ", hardcover"
					elif result[PUB_PTYPE] == 'tp':
						outstr += ", trade paperback"
					elif result[PUB_PTYPE] == 'pb':
						outstr += ", mass market paperback"
					elif result[PUB_PTYPE] == 'audio':
						outstr += ", audio"
					else:
						outstr += ", " + result[PUB_PTYPE]

				if result[PUB_CTYPE]:
						outstr += ', %s' % result[PUB_CTYPE].lower()
				outstr += ') by '

				print '<td>%s' % outstr
				displayPubAuthors(result[PUB_PUBID])
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
