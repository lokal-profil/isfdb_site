#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Ahasuerus and Bill Longley
#	 ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import printtextarea
from titleClass import *
from isbn import convertISBN
	

if __name__ == '__main__':
        title_id = SESSION.Parameter(0, 'int')
	pubs = SQLGetPubsByTitleNoParent(title_id)
	if not pubs:
                SESSION.DisplayError('No Publications to Unmerge')
	
	PrintPreSearch('Title Unmerge Request')
	PrintNavBar('edit/tv_unmerge.cgi', title_id)

	print '<div id="HelpBox">'
	print '<b>Help on unmerging titles: </b>'
	print '<a href="http://%s/index.php/Help:Screen:UnmergeTitles">Help:Screen:UnmergeTitles</a><p>' % (WIKILOC)
	print '</div>'
	print '<b>Select titles to unmerge:</b>'
	print '<p>'
	print '<hr>'

        help = HelpGeneral()

	print "<form id='data' METHOD=\"POST\" ACTION=\"/cgi-bin/edit/ts_unmerge.cgi\">"
        index = 1
        print '<ul>'
        for pub in pubs:
                output = '<li>'
                output += '<input type="checkbox" value="%d" name="pub%d"> ' % (pub[PUB_PUBID], index)

                #####################################
                # TITLE
                #####################################
                output += pub[PUB_TITLE]

                #####################################
                # DATE
                #####################################
                if pub[PUB_YEAR] == '0000-00-00':
                        output += " (date unknown "
                else:
                        month = string.split(pub[PUB_YEAR], "-")[1]
                        if month:
                                try:
                                        strmonth = monthmap[int(month)]
                                        output += " (%s %s " % (strmonth, pub[PUB_YEAR][:4])
                                except:
                                        output += " (%s " % (pub[PUB_YEAR][:4])
                        else:
                                output += " (%s " % (pub[PUB_YEAR][:4])

                #####################################
                # AUTHORS
                #####################################
                output += ', '
                authors = SQLPubAuthors(pub[PUB_PUBID])
                counter = 0
                for author in authors:
                        if counter:
                                output += ", "
                        output += author
                        counter += 1

                if pub[PUB_PUBLISHER]:
                        publisher = SQLGetPublisher(pub[PUB_PUBLISHER])
                        output += ", " + publisher[PUBLISHER_NAME]
                if pub[PUB_SERIES]:
                        pub_series = SQLGetPubSeries(pub[PUB_SERIES])
                        output += ", " + pub_series[PUB_SERIES_NAME]
                if pub[PUB_SERIES_NUM]:
                        output += ", " + pub[PUB_SERIES_NUM]
                if pub[PUB_ISBN]:
                        output += ", " + convertISBN(pub[PUB_ISBN])
                if pub[PUB_PRICE]:
                        output += ", " + pub[PUB_PRICE]
                if pub[PUB_PAGES]:
                        output += ", " + pub[PUB_PAGES]+"pp"
                if pub[PUB_PTYPE]:
                        output += ", " + pub[PUB_PTYPE]
                if pub[PUB_CTYPE]:
                        if pub[PUB_CTYPE] == 'COLLECTION':
                                output += ", coll"
                        elif pub[PUB_CTYPE] == 'ANTHOLOGY':
                                output += ", anth"
                        elif pub[PUB_CTYPE] == 'OMNIBUS':
                                output += ", omni"
                        elif pub[PUB_CTYPE] == 'MAGAZINE':
                                output += ", magazine"
                        elif pub[PUB_CTYPE] == 'FANZINE':
                                output += ", fanzine"
                output += ")"

                print output
                index += 1
        print '</ul>'
        print '<hr>'
        print '<table border="0">'
        print '<tbody id="tagBody">'
        printtextarea('Note to Moderator', 'mod_note', help, '')
        print '</tbody>'
        print '</table>'
        print '<p>'

	print '<input NAME="record" VALUE="%d" TYPE="HIDDEN">' % (title_id)
	print '<input TYPE="SUBMIT" VALUE="Submit Unmerge" tabindex="1">'
	print '</form>'

	PrintPostSearch(0, 0, 0, 0, 0, False)
