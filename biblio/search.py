#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2017   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.56 $
#     Date: $Date: 2017/10/08 19:00:10 $


import sys
import string

from isfdb import *
from SQLparsing import *
from common import *

def PrintRadioSelectors(number):
	print '<input TYPE="RADIO" NAME="CONJUNCTION_%d" VALUE="AND" CHECKED>AND' % number
	print '<input TYPE="RADIO" NAME="CONJUNCTION_%d" VALUE="OR">OR' % number
	print '<p>'

def PrintOperators(number):
	print '<select NAME="OPERATOR_%d">' % number
	print '<option SELECTED VALUE="exact">is exactly'
	print '<option VALUE="notexact">is not exactly'
	print '<option VALUE="contains">contains'
	print '<option VALUE="notcontains">does not contain'
	print '<option VALUE="starts_with">starts with'
	print '<option VALUE="ends_with">ends with'
       	print '</select>'

def PrintTitleSelectors(number):
	print '<select NAME="USE_%d">' % number
	print '<option SELECTED VALUE="title_title">Title'
        print '<option VALUE="title_trans_title">Transliterated Title'
        print '<option VALUE="author_canonical">Author\'s Name'
        print '<option VALUE="author_birthplace">Author\'s Birth Place'
        print '<option VALUE="author_birthdate">Author\'s Birthdate'
        print '<option VALUE="author_deathdate">Author\'s Deathdate'
        print '<option VALUE="author_webpage">Author\'s Webpage'
        print '<option VALUE="reviewee">Reviewed Author'
        print '<option VALUE="interviewee">Interviewed Author'
	print '<option VALUE="title_copyright">Title Year'
        print '<option VALUE="month">Title Month'
        print '<option VALUE="title_storylen">Length'
        print '<option VALUE="title_content">Content'
	print '<option VALUE="title_ttype">Title Type'
        print '<option VALUE="title_note">Notes'
        print '<option VALUE="title_synopsis">Synopsis'
        print '<option VALUE="series">Series'
        print '<option VALUE="title_language">Title Language'
        print '<option VALUE="title_webpage">Title Webpage'
        print '<option VALUE="tag">Title Tag'
        print '<option VALUE="title_jvn">Juvenile (Yes or No)'
        print '<option VALUE="title_nvz">Novelization (Yes or No)'
        print '<option VALUE="title_non_genre">Non-Genre (Yes or No)'
        print '<option VALUE="title_graphic">Graphic Format (Yes or No)'
	print '</select>'

        PrintOperators(number)

        print '<input NAME="TERM_%d" SIZE="50">' % number
	print '<p>'

def PrintTitleSearch():
	print '<h2>Title Search</h2>'
	print '<p>'
	print '<ul>'
	print '<li> Valid title types: ANTHOLOGY, CHAPBOOK, COLLECTION, COVERART, EDITOR (for magazines/fanzines), ESSAY, INTERIORART, INTERVIEW, NONFICTION, NOVEL, OMNIBUS, POEM, REVIEW, SERIAL, SHORTFICTION'
	print '<li> Valid length types: "novella", "novelette", "short story"'
	print '<li> When specifying multiple authors and/or multiple tags, OR is supported but AND is not'
	print '</ul>'
	print '<p>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'

        for number in (1, 2, 3):
                PrintTitleSelectors(number)
                if number < 3:
                        PrintRadioSelectors(number)
	PrintTitleSortBy()

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
	print '<input NAME="TYPE" VALUE="Title" TYPE="HIDDEN">'
	print '</form>'

def PrintTitleSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="title_title">Title'
	print '<option VALUE="title_copyright">Date'
	print '<option VALUE="title_ttype">Title Type'
       	print '</select>'

def PrintAuthorSelectors(number):
	print '<select NAME="USE_%d">' % number
	print '<option SELECTED VALUE="author_canonical">Canonical Name'
        print '<option VALUE="author_trans_name">Transliterated Name'
	print '<option VALUE="author_lastname">Family Name'
	print '<option VALUE="author_legalname">Legal Name'
	print '<option VALUE="author_birthplace">Birth Place'
	print '<option VALUE="author_birthdate">Birthdate'
	print '<option VALUE="author_deathdate">Deathdate'
        print '<option VALUE="author_language">Working Language'
        print '<option VALUE="author_trans_legalname">Transliterated Legal Name'
        print '<option VALUE="author_webpage">Webpage'
        print '<option VALUE="author_email">E-mail'
        print '<option VALUE="author_pseudos">Pseudonym'
        print '<option VALUE="author_note">Note'
       	print '</select>'

        PrintOperators(number)

        print '<input NAME="TERM_%d" SIZE="50">' % number
	print '<p>'

def PrintAuthorSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="author_canonical">Canonical Name'
	print '<option VALUE="author_lastname">Family Name'
	print '<option VALUE="author_legalname">Legal Name'
	print '<option VALUE="author_birthplace">Birth Place'
	print '<option VALUE="author_birthdate">Birthdate'
	print '<option VALUE="author_deathdate">Deathdate'
       	print '</select>'
        
def PrintAuthorSearch():
	print '<h2>Author Search</h2>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'

        for number in (1, 2, 3):
                PrintAuthorSelectors(number)
                if number < 3:
                        PrintRadioSelectors(number)
	PrintAuthorSortBy()

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
	print '<input NAME="TYPE" VALUE="Author" TYPE="HIDDEN">'
	print '</form>'

def PrintPubSelectors(number):
	print '<select NAME="USE_%d">' % number
	print '<option SELECTED VALUE="pub_title">Title'
        print '<option VALUE="pub_trans_title">Transliterated Title'
	print '<option VALUE="pub_ctype">Publication Type'
        print '<option VALUE="author_canonical">Author\'s Name'
        print '<option VALUE="author_birthplace">Author\'s Birth Place'
        print '<option VALUE="author_birthdate">Author\'s Birthdate'
        print '<option VALUE="author_deathdate">Author\'s Deathdate'
        print '<option VALUE="author_webpage">Author\'s Webpage'
	print '<option VALUE="pub_year">Publication Year'
        print '<option VALUE="pub_month">Publication Month'
        print '<option VALUE="pub_publisher">Publisher'
        print '<option VALUE="trans_publisher">Transliterated Publisher'
        print '<option VALUE="pub_series">Publication Series'
        print '<option VALUE="trans_pub_series">Transliterated Publication Series'
	print '<option VALUE="pub_isbn">ISBN/Catalog #'
	print '<option VALUE="pub_price">Price'
	print '<option VALUE="pub_pages">Page Count'
        print '<option VALUE="pub_coverart">Cover Artist'
	print '<option VALUE="pub_ptype">Format'
	print '<option VALUE="pub_verifier">Primary Verifier'
        print '<option VALUE="pub_note">Notes'
	print '<option VALUE="pub_frontimage">Image URL'
	print '<option VALUE="pub_tag">Tag'
	print '</select>'

        PrintOperators(number)

        print '<input NAME="TERM_%d" SIZE="50">' % number
	print '<p>'

def PrintPubSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="pub_title">Title'
	print '<option VALUE="pub_ctype">Publication Type'
	print '<option VALUE="pub_tag">Tag'
	print '<option VALUE="pub_year">Date'
	print '<option VALUE="pub_isbn">ISBN/Catalog #'
	print '<option VALUE="pub_price">Price'
	print '<option VALUE="pub_pages">Page Count'
	print '<option VALUE="pub_ptype">Format'
	print '<option VALUE="pub_frontimage">Image URL'
       	print '</select>'

def PrintPubSearch():
	print '<h2>Publication Search</h2>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'
	print '<ul>'
	print '<li> Valid publication types: ANTHOLOGY, CHAPBOOK, COLLECTION, FANZINE, MAGAZINE, NONFICTION, NOVEL, OMNIBUS'
	print '<li> ISBN searches ignore dashes and search for both ISBN-10 and ISBN-13'
	print '</ul>'
	print '<p>'

        for number in (1, 2, 3):
                PrintPubSelectors(number)
                if number <3:
                        PrintRadioSelectors(number)
	PrintPubSortBy()

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
	print '<input NAME="TYPE" VALUE="Publication" TYPE="HIDDEN">'
	print '</form>'

def PrintIdentifierSearch():
	print '<h2>Publication Search by External Identifier</h2>'
	print '<form METHOD="GET" action="http:/%s/external_id_search_results.cgi">' % (HTFAKE)
	print '<p>'
        id_types = SQLLoadIdentifierTypes()
	print '<select NAME="ID_TYPE">'
	for type_number in sorted(id_types, key = id_types.get):
                type_name = id_types[type_number][0]
                print '<option VALUE="%d">%s</option>' % (type_number, type_name)
	print '</select>'

        print '<input NAME="ID_VALUE" SIZE="50">'
	print '<p>'

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
	print '<input NAME="TYPE" VALUE="Publication" TYPE="HIDDEN">'
	print '</form>'

def PrintUserSearch():
	print '<h2>User Search</h2>'
	print '<form METHOD="GET" action="http:/%s/user_search_results.cgi">' % (HTFAKE)
	print '<p>'
        print '<input NAME="USER_NAME" SIZE="50">'
	print '<p>'
	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

if __name__ == '__main__':

        PrintHeader("ISFDB Advanced Search")
	PrintNavbar('search', 0, 0, 0, 0)

        print '<ul>'
        print '<li>Supported wildcards: * and % match any number of characters, _ matches one character'
        print '</ul>'
        print '<hr>'
	PrintTitleSearch()
	print '<p><hr><p>'
	PrintAuthorSearch()
	print '<p><hr><p>'
	PrintPubSearch()
	print '<p><hr><p>'
	PrintIdentifierSearch()
	print '<p><hr><p>'
	PrintUserSearch()

	PrintTrailer('search', 0, 0)

