#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2019   Al von Ruff, Ahasuerus and Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import string

from isfdb import *
from SQLparsing import *
from common import *


def PrintDropDownValues():
        PrintOneDropDown('Formats', FORMATS)
        PrintOneDropDown('PubTypes', PUB_TYPES)
        PrintOneDropDown('TitleTypes', ALL_TITLE_TYPES)
        PrintOneDropDown('StoryLengths', STORYLEN_CODES)
        selectable_languages = sorted(list(LANGUAGES))
        if 'None' in selectable_languages:
                selectable_languages.remove('None')
        PrintOneDropDown('AllLanguages', selectable_languages)

def PrintOneDropDown(name, values):
	print '<select NAME="%s" id="%s" class="nodisplay">' % (name, name)
	for value in values:
                # Skip empty values, e.g. in STORYLEN_CODES
                if value:
                        print '<option VALUE="%s">%s' % (value, value)
       	print '</select>'

def PrintRadioSelectors():
	print '<input TYPE="RADIO" NAME="C" VALUE="AND" CHECKED>AND'
	print '<input TYPE="RADIO" NAME="C" VALUE="OR">OR'

def PrintSubmitButton(record_type):
	print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="query">Get Results</button>'
	print '<button TYPE="SUBMIT" NAME="ACTION" VALUE="count">Get Count</button>'
	print '<input NAME="START" VALUE="0" TYPE="HIDDEN">'
	print '<input NAME="TYPE" VALUE="%s" TYPE="HIDDEN">' % record_type
	print '</form>'

def PrintOperators(record_type, number):
	print '<select NAME="O_%d" id="%s_operator_%d">' % (number, record_type, number)
	print '<option SELECTED VALUE="exact">is exactly'
	print '<option VALUE="notexact">is not exactly'
	print '<option VALUE="contains">contains'
	print '<option VALUE="notcontains">does not contain'
	print '<option VALUE="starts_with">starts with'
	print '<option VALUE="ends_with">ends with'
       	print '</select>'

def PrintTitleSelectors(number):
	print '<p id="title_selectors_%d">' % number
	print '<select NAME="USE_%d" id="title_%d">' % (number, number)
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
        print '<option VALUE="title_language">Title Language (list)'
        print '<option VALUE="title_language_free">Title Language (free form)'
        print '<option VALUE="title_webpage">Title Webpage'
        print '<option VALUE="tag">Tag'
        print '<option VALUE="title_jvn">Juvenile'
        print '<option VALUE="title_nvz">Novelization'
        print '<option VALUE="title_non_genre">Non-Genre'
        print '<option VALUE="title_graphic">Graphic Format'
	print '</select>'

        PrintOperators('title', number)

        print '<input id="titleterm_%d" NAME="TERM_%d" SIZE="50">' % (number, number)
        if number == 1:
                PrintRadioSelectors()
	print '<p>'

def PrintTitleSearch(max_term):
	print '<h2>Title Search</h2>'
	print '<p>'
	print '<ul>'
	print '<li> When specifying multiple authors and/or multiple tags, OR is supported but AND is not'
	print '</ul>'
	print '<p>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'

        for number in range(1, max_term + 1):
                PrintTitleSelectors(number)
	PrintTitleSortBy()
        PrintSubmitButton('Title')

def PrintTitleSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="title_title">Title'
	print '<option VALUE="title_copyright">Date'
	print '<option VALUE="title_ttype">Title Type'
       	print '</select>'

def PrintAuthorSelectors(number):
	print '<p id="author_selectors_%d">' % number
	print '<select NAME="USE_%d" id="author_%d">' % (number, number)
	print '<option SELECTED VALUE="author_canonical">Canonical Name'
        print '<option VALUE="author_trans_name">Transliterated Name'
	print '<option VALUE="author_lastname">Directory Entry'
	print '<option VALUE="author_legalname">Legal Name'
	print '<option VALUE="author_birthplace">Birth Place'
	print '<option VALUE="author_birthdate">Birthdate'
	print '<option VALUE="author_deathdate">Deathdate'
        print '<option VALUE="author_language">Working Language (list)'
        print '<option VALUE="author_language_free">Working Language (free form)'
        print '<option VALUE="author_trans_legalname">Transliterated Legal Name'
        print '<option VALUE="author_webpage">Webpage'
        print '<option VALUE="author_email">E-mail'
        print '<option VALUE="author_pseudos">Alternate Name'
        print '<option VALUE="author_note">Note'
       	print '</select>'

        PrintOperators('author', number)

        print '<input id="authorterm_%d" NAME="TERM_%d" SIZE="50">' % (number, number)
        if number == 1:
                PrintRadioSelectors()
	print '<p>'

def PrintAuthorSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="author_canonical">Canonical Name'
	print '<option VALUE="author_lastname">Directory Entry'
	print '<option VALUE="author_legalname">Legal Name'
	print '<option VALUE="author_birthplace">Birth Place'
	print '<option VALUE="author_birthdate">Birthdate'
	print '<option VALUE="author_deathdate">Deathdate'
       	print '</select>'
        
def PrintAuthorSearch(max_term):
	print '<h2>Author Search</h2>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'

        for number in range(1, max_term + 1):
                PrintAuthorSelectors(number)
	PrintAuthorSortBy()
        PrintSubmitButton('Author')

def PrintPubSelectors(number):
	print '<p id="pub_selectors_%d">' % number
	print '<select NAME="USE_%d" id="pub_%d">' % (number, number)
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
	print '<option VALUE="pub_isbn">ISBN'
	print '<option VALUE="pub_catalog">Catalog ID'
	print '<option VALUE="pub_price">Price'
	print '<option VALUE="pub_pages">Page Count'
        print '<option VALUE="pub_coverart">Cover Artist'
	print '<option VALUE="pub_ptype">Format'
	print '<option VALUE="pub_verifier">Primary Verifier'
        print '<option VALUE="pub_note">Notes'
	print '<option VALUE="pub_frontimage">Image URL'
	print '</select>'

        PrintOperators('pub', number)

        print '<input id="pubterm_%d" NAME="TERM_%d" TYPE="text" SIZE="50">' % (number, number)
        if number == 1:
                PrintRadioSelectors()
        print '<p>'

def PrintPubSortBy():
	print '<b>Sort Results By:</b>'
	print '<select NAME="ORDERBY">'
	print '<option SELECTED VALUE="pub_title">Title'
	print '<option VALUE="pub_ctype">Publication Type'
	print '<option VALUE="pub_year">Date'
	print '<option VALUE="pub_isbn">ISBN'
	print '<option VALUE="pub_catalog">Catalog ID'
	print '<option VALUE="pub_price">Price'
	print '<option VALUE="pub_pages">Page Count'
	print '<option VALUE="pub_ptype">Format'
	print '<option VALUE="pub_frontimage">Image URL'
       	print '</select>'

def PrintPubSearch(max_term):
	print '<h2>Publication Search</h2>'
	print '<form METHOD="GET" action="http:/%s/adv_search_results.cgi">' % (HTFAKE)
	print '<p>'
	print '<ul>'
	print '<li> ISBN searches ignore dashes and search for both ISBN-10 and ISBN-13'
	print '</ul>'

        for number in range(1, max_term + 1):
                PrintPubSelectors(number)
	PrintPubSortBy()
        PrintSubmitButton('Publication')

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

	print '<select NAME="OPERATOR">'
	print '<option SELECTED VALUE="exact">is exactly'
	print '<option VALUE="contains">contains'
	print '<option VALUE="notcontains">does not contain'
	print '<option VALUE="starts_with">starts with'
	print '<option VALUE="not_starts_with">does not start with'
	print '<option VALUE="ends_with">ends with'
	print '<option VALUE="not_ends_with">does not end with'
	print '</select>'

        print '<input NAME="ID_VALUE" SIZE="50">'
	print '<p>'

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

def PrintUserSearch():
	print '<h2>User Search</h2>'
	print '<form METHOD="GET" action="http:/%s/user_search_results.cgi">' % (HTFAKE)
	print '<p>'
        print '<input NAME="USER_NAME" SIZE="50">'
	print '<p>'
	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

def PrintNotesSearch():
	print '<h2>Notes Search</h2>'
	print '<form METHOD="GET" action="http:/%s/note_search_results.cgi">' % (HTFAKE)
	print '<p>'
	print 'Note/Synopsis '
	print '<select NAME="OPERATOR">'
	print '<option SELECTED VALUE="contains">contains'
	print '<option VALUE="exact">is exactly'
	print '<option VALUE="starts_with">starts with'
	print '<option VALUE="ends_with">ends with'
       	print '</select>'
        print '<input NAME="NOTE_VALUE" SIZE="50">'
	print '<p>'
	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

def PrintWebPageSearch():
	print '<h2>Web Page Search</h2>'
	print '<form METHOD="GET" action="http:/%s/webpages_search_results.cgi">' % (HTFAKE)
	print '<p>'
	print 'Web Page '
	print '<select NAME="OPERATOR">'
	print '<option SELECTED VALUE="contains">contains'
	print '<option VALUE="exact">is exactly'
	print '<option VALUE="starts_with">starts with'
	print '<option VALUE="ends_with">ends with'
       	print '</select>'
        print '<input NAME="WEBPAGE_VALUE" SIZE="100">'
	print '<p>'
	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

def PrintGoogleSearch():
	print '<h2>Search ISFDB Using Google</h2>'
	print '<form METHOD="GET" action="http:/%s/google_search_redirect.cgi" accept-charset="utf-8">' % (HTFAKE)
	print '<p>'
	print '<select NAME="PAGE_TYPE">'
        print '<option VALUE="name">Name'
	print '<option VALUE="title">Title'
	print '<option VALUE="series">Series'
	print '<option VALUE="publication">Publication'
	print '<option VALUE="pubseries">Publication Series'
	print '<option VALUE="publisher">Publisher'
	print '<option VALUE="award_category">Award Category'
	print '</select>'

	print '<select NAME="OPERATOR">'
        print '<option VALUE="exact">contains exact word'
        print '<option SELECTED VALUE="approximate">contains approximate word'
	print '</select>'

        print '<input NAME="SEARCH_VALUE" SIZE="50">'
	print '<p>'

	print '<input TYPE="SUBMIT" VALUE="Submit Query">'
	print '</form>'

if __name__ == '__main__':

        PrintHeader("ISFDB Advanced Search")
	PrintNavbar('search', 0, 0, 0, 0)

        PrintDropDownValues()
        print '<ul>'
        print '<li>A downloadable version of the ISFDB database is available <a href="http://%s/index.php/ISFDB_Downloads">here</a>' % WIKILOC
        print '<li>Supported wildcards: * and % match any number of characters, _ matches one character'
        print '</ul>'
        print '<hr>'
        max_term = 5
	PrintTitleSearch(max_term)
	print '<p><hr><p>'
	PrintAuthorSearch(max_term)
	print '<p><hr><p>'
	PrintPubSearch(max_term)
	print '<p><hr><p>'
	PrintIdentifierSearch()
	print '<p><hr><p>'
	PrintUserSearch()
	print '<p><hr><p>'
	PrintNotesSearch()
	print '<p><hr><p>'
	PrintWebPageSearch()
	print '<p><hr><p>'
	PrintGoogleSearch()

	PrintTrailer('search', 0, 0)

