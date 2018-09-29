#
#     (C) COPYRIGHT 2005-2018   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgitb; cgitb.enable()
from localdefs import *

def Date_or_None(s):
    return s

def IsfdbConvSetup():
    import MySQLdb.converters
    IsfdbConv = MySQLdb.converters.conversions
    IsfdbConv[10] = Date_or_None
    return(IsfdbConv)

def PrintHTMLHeaders(title):
    from datetime import date
    # Disallow the <base> directive
    print """Content-Security-Policy: base-uri 'none';"""
    # Disallow <a> ping, Fetch, XMLHttpRequest, WebSocket, and EventSource
    #   May need to be re-worked if we implement AJAX
    print """Content-Security-Policy: connect-src 'none';"""
    # Disallow @font-face
    print """Content-Security-Policy: font-src 'none';"""
    # Restrict form submission URLs to the ISFDB server
    print """Content-Security-Policy: form-action 'self' http://%s;""" % HTMLHOST
    # Disable nested browsing contexts
    print """Content-Security-Policy: frame-src 'none';"""
    # Disable <frame>, <iframe>, <object>, <embed>, and <applet>
    print """Content-Security-Policy: frame-ancestors 'none';"""
    # Restrict sources of images and favicons to HTTP and HTTPS
    print """Content-Security-Policy: img-src http: https:;"""
    # Disallow <manifest>
    print """Content-Security-Policy: manifest-src 'none';"""
    # Disallow <audio>, <track> and <video>
    print """Content-Security-Policy: media-src 'none';"""
    # Disallow <object>, <embed>, and <applet>
    print """Content-Security-Policy: object-src 'none';"""
    # Limit JS scripts to .js files served by the ISFDB server
    print """Content-Security-Policy: script-src 'self' http://%s;""" % HTMLHOST
    # Limit stylesheets to .css files served by the ISFDB server
    print """Content-Security-Policy: style-src 'self' http://%s;""" % HTMLHOST
    # Disable Worker, SharedWorker, or ServiceWorker scripts
    #   May need to be re-worked if we implement workers
    print """Content-Security-Policy: worker-src 'none';"""
    # Declare content type and end the HTTP headers section with a \n
    print 'Content-type: text/html; charset=%s\n' % UNICODE
    print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    print '<html lang="en-us">'
    print '<head>'
    print '<meta http-equiv="content-type" content="text/html; charset=%s" >' % UNICODE
    print '<link rel="shortcut icon" href="http://%s/favicon.ico">' % HTMLHOST
    print '<title>%s</title>' % title
    print '<link href="http://%s/biblio.css" rel="stylesheet" type="text/css" media="screen">' % HTMLHOST
    print '</head>'
    print '<body>'
    print '<div id="wrap">'
    print '<a class="topbanner" href="http:/%s/index.cgi">' % HTFAKE
    print '<span>'
    # Get the number of days since January 1, 2000
    millenium = date(2000, 1, 1)
    today = date.today()
    elapsed = today - millenium
    # Calculate the banner number for today; the range is 2-11
    banner_number = (elapsed.days % 10) + 2
    print '<img src="http://%s/IsfdbBanner%d.jpg" alt="ISFDB banner">' % (HTMLHOST, banner_number)
    print '</span>'
    print '</a>'
    print '<div id="statusbar">'
    print '<h2>%s</h2>' % (title)

SCHEMA_VER = "0.02"
ENGINE     = "<b>ISFDB Engine</b> - Version 4.00 (04/24/06)"
COPYRIGHT  = "Copyright (c) 1995-2018 Al von Ruff."
# NONCE should be uncommented if and when we need it to create CSP nonces
# import uuid
# NONCE = uuid.uuid4().hex

# History Actions (obsolete)
AUTHOR_UPDATE  = 1
AUTHOR_INSERT  = 2
AUTHOR_DELETE  = 3
AUTHOR_MERGE   = 4

# Field offsets for publication records
PUB_PUBID     = 0
PUB_TITLE     = 1
PUB_TAG       = 2
PUB_YEAR      = 3
PUB_PUBLISHER = 4
PUB_PAGES     = 5
PUB_PTYPE     = 6
PUB_CTYPE     = 7
PUB_ISBN      = 8
PUB_IMAGE     = 9
PUB_PRICE     = 10
PUB_NOTE      = 11
PUB_SERIES    = 12
PUB_SERIES_NUM= 13
PUB_CATALOG   = 14

# Field offsets for author records
AUTHOR_ID         = 0
AUTHOR_CANONICAL  = 1
AUTHOR_LEGALNAME  = 2
AUTHOR_BIRTHPLACE = 3
AUTHOR_BIRTHDATE  = 4
AUTHOR_DEATHDATE  = 5
AUTHOR_NOTE_ID    = 6
AUTHOR_WIKI       = 7
AUTHOR_COUNTER    = 8
AUTHOR_IMDB       = 9
AUTHOR_MARQUE     = 10
AUTHOR_IMAGE      = 11
AUTHOR_ANNUALVIEWS= 12
AUTHOR_LASTNAME   = 13
AUTHOR_LANGUAGE   = 14
AUTHOR_NOTE       = 15
# Pseudo offsets used by author history
AUTHOR_EMAILS	  = 16
AUTHOR_WEBPAGES	  = 17
AUTHOR_TRANS_LEGALNAME	  = 18
AUTHOR_TRANS_NAME = 19
AUTHOR_MAX        = 20 # Highest author offset+1; used to display author history


# Field offsets for title records
TITLE_PUBID       = 0
TITLE_TITLE       = 1
TITLE_XLATE       = 2
TITLE_SYNOP       = 3
TITLE_NOTE        = 4
TITLE_SERIES      = 5
TITLE_SERIESNUM   = 6
TITLE_YEAR        = 7
TITLE_STORYLEN    = 8
TITLE_TTYPE       = 9
TITLE_WIKI        = 10
TITLE_VIEWS       = 11
TITLE_PARENT      = 12
TITLE_RATING      = 13
TITLE_ANNUALVIEWS = 14
TITLE_CTL         = 15
TITLE_LANGUAGE    = 16
TITLE_SERIESNUM_2 = 17
TITLE_NON_GENRE   = 18
TITLE_GRAPHIC     = 19
TITLE_NVZ         = 20
TITLE_JVN         = 21
TITLE_CONTENT     = 22

# Field offsets for award records
AWARD_ID             = 0
AWARD_TITLE          = 1
AWARD_AUTHOR         = 2
AWARD_YEAR           = 3
AWARD_TTYPE          = 4
#AWARD_ATYPE         = 5
AWARD_LEVEL          = 6
AWARD_MOVIE          = 7
AWARD_TYPEID         = 8
AWARD_CATID          = 9
AWARD_NOTEID         = 10

# Field offsets for award type records
AWARD_TYPE_ID         = 0
AWARD_TYPE_CODE       = 1
AWARD_TYPE_NAME       = 2
AWARD_TYPE_WIKI       = 3
AWARD_TYPE_NOTE       = 4
AWARD_TYPE_BY         = 5
AWARD_TYPE_FOR        = 6
AWARD_TYPE_SHORT_NAME = 7
AWARD_TYPE_POLL       = 8
AWARD_TYPE_NONGENRE   = 9

# Field offsets for award category records
AWARD_CAT_ID          = 0
AWARD_CAT_NAME        = 1
AWARD_CAT_TYPE_ID     = 2
AWARD_CAT_ORDER       = 3
AWARD_CAT_NOTE        = 4

# Field offsets for note records
NOTE_PUBID           = 0
NOTE_NOTE            = 1

# Field offsets for series records
SERIES_PUBID           = 0
SERIES_NAME            = 1
SERIES_PARENT          = 2
SERIES_TYPE            = 3
SERIES_PARENT_POSITION = 4
SERIES_NOTE            = 5

# Order of series types on author and series biblio page
SERIES_TYPE_UNKNOWN     = -1
SERIES_TYPE_NC          = 1
SERIES_TYPE_EDIT        = 2
SERIES_TYPE_ANTH        = 3
SERIES_TYPE_NONFIC      = 4
SERIES_TYPE_SF          = 5
SERIES_TYPE_POEM        = 6
SERIES_TYPE_ESSAY       = 7
SERIES_TYPE_OTHER       = 9

# Field offsets for pub_contents records
PUB_CONTENTS_ID      = 0
PUB_CONTENTS_TITLE   = 1
PUB_CONTENTS_PUB     = 2
PUB_CONTENTS_PAGE    = 3

# Field offsets for publisher records
PUBLISHER_ID         = 0
PUBLISHER_NAME       = 1
PUBLISHER_WIKI       = 2
PUBLISHER_NOTE       = 3

# Field offsets for Publication Series records
PUB_SERIES_ID        = 0
PUB_SERIES_NAME      = 1
PUB_SERIES_WIKI      = 2
PUB_SERIES_NOTE      = 3

# Field offsets for submission records
SUB_ID               = 0
SUB_STATE            = 1
SUB_TYPE             = 2
SUB_DATA             = 3
SUB_TIME             = 4
SUB_REVIEWED         = 5
SUB_SUBMITTER        = 6
SUB_REVIEWER         = 7
SUB_REASON           = 8
SUB_HOLDID           = 9
SUB_NEW_RECORD_ID    = 10

# Field offsets for Website records
WEBSITE_URL          = 0
WEBSITE_NAME         = 1

# Field offsets for primary verifications
PRIM_VERIF_ID        = 0
PRIM_VERIF_PUB_ID    = 1
PRIM_VERIF_USER_ID   = 2
PRIM_VERIF_TIME      = 3
PRIM_VERIF_TRANSIENT = 4

# Field offsets for secondary verifications
VERIF_ID             = 0
VERIF_PUB_ID         = 1
VERIF_REF_ID         = 2
VERIF_USER_ID        = 3
VERIF_TIME           = 4
VERIF_STATUS         = 5

# Field offsets for verification sources; 3 is not used
REFERENCE_ID         = 0
REFERENCE_LABEL      = 1
REFERENCE_NAME       = 2
REFERENCE_URL        = 4

# Field offsets for tags
TAG_ID               = 0
TAG_NAME             = 1
TAG_STATUS           = 2

# Field offsets for User Preferences
USER_CONCISE_DISP     = 0
USER_DEFAULT_LANGUAGE = 1
USER_DISPLAY_ALL_LANG = 2

# Field offsets for External Identifier Types
IDTYPE_ID            = 0
IDTYPE_NAME          = 1
IDTYPE_FULL_NAME     = 2

# Field offsets for External Identifiers
IDENTIFIER_ID        = 0
IDENTIFIER_TYPE_ID   = 1
IDENTIFIER_VALUE     = 2
IDENTIFIER_PUB_ID    = 3

# Field offsets for External Identifier Sites
IDSITE_ID            = 0
IDSITE_TYPE_ID       = 1
IDSITE_POSITION      = 2
IDSITE_URL           = 3
IDSITE_NAME          = 4

# Recognized submission types
MOD_AUTHOR_MERGE     = 1
MOD_AUTHOR_UPDATE    = 2
MOD_AUTHOR_DELETE    = 3
MOD_PUB_UPDATE       = 4
MOD_PUB_MERGE        = 5
MOD_PUB_DELETE       = 6
MOD_PUB_NEW          = 7
MOD_TITLE_UPDATE     = 8
MOD_TITLE_MERGE      = 9
MOD_TITLE_DELETE     = 10
MOD_TITLE_NEW        = 11 #currently unused
MOD_TITLE_UNMERGE    = 12
MOD_SERIES_UPDATE    = 13
MOD_CONTENT_UPDATE   = 14 #currently unused
MOD_VARIANT_TITLE    = 15
MOD_TITLE_MKVARIANT  = 16
MOD_RMTITLE          = 17
MOD_PUB_CLONE        = 18
MOD_AUTHOR_PSEUDO    = 19
MOD_AWARD_NEW        = 20
MOD_AWARD_UPDATE     = 21
MOD_AWARD_DELETE     = 22
MOD_PUBLISHER_UPDATE = 23
MOD_PUBLISHER_MERGE  = 24
MOD_REVIEW_LINK      = 25
MOD_DELETE_SERIES    = 26
MOD_REMOVE_PSEUDO    = 27
MOD_PUB_SERIES_UPDATE= 28
MOD_AWARD_TYPE_UPDATE= 29
MOD_AWARD_LINK       = 30
MOD_AWARD_TYPE_NEW   = 31
MOD_AWARD_TYPE_DELETE= 32
MOD_AWARD_CAT_NEW    = 33
MOD_AWARD_CAT_DELETE = 34
MOD_AWARD_CAT_UPDATE = 35

# SUBMAP is a dictionary used to store information about submission types
# [0] - Name of the moderator review script
# [1] - Short name of the submission type and the first XML tag in the submission; displayed on submission list pages
# [2] - Name of the script used to link to the record from the list of recent entries
# [3] - Full name of the submission type, used in stats-and-tops.py
# [4] - Name of the XML element containing the record number in the submission -- used to link from the list of recent entries
# [5] - Name of the "viewers" function used to display the body of this submission type
SUBMAP = {
  MOD_AUTHOR_MERGE :	 ('av_merge',  'AuthorMerge', 'ea.cgi', 'Author Merge', 'Record', 'DisplayAuthorMerge'),
  MOD_AUTHOR_UPDATE :	 ('av_update', 'AuthorUpdate', 'ea.cgi', 'Author Update', 'Record', 'DisplayAuthorChanges'),
  MOD_AUTHOR_DELETE :	 ('av_delete', 'AuthorDelete', None, None, 'Record'), # currently unused
  MOD_PUB_UPDATE :	 ('pv_update', 'PubUpdate', 'pl.cgi', 'Publication Update', 'Record', 'DisplayEditPub'),
  MOD_PUB_DELETE :	 ('pv_delete', 'PubDelete', None, 'Publication Delete', 'Record', 'DisplayDeletePub'),
  MOD_PUB_NEW :		 ('pv_new',    'NewPub', 'pl.cgi', 'New Publication', 'Record', 'DisplayNewPub'),
  MOD_TITLE_UPDATE :	 ('tv_update', 'TitleUpdate', 'title.cgi', 'Title Update', 'Record', 'DisplayTitleEdit'),
  MOD_TITLE_MERGE :	 ('tv_merge',  'TitleMerge', 'title.cgi', 'Title Merge', 'Record', 'DisplayMergeTitles'),
  MOD_TITLE_DELETE :	 ('tv_delete', 'TitleDelete', None, 'Title Delete', 'Record', 'DisplayTitleDelete'),
  MOD_TITLE_NEW :	 ('tv_new',    'TitleNew', None, None, 'Record'), #currently unused, but referenced in submittitle
  MOD_TITLE_UNMERGE :	 ('tv_unmerge','TitleUnmerge', 'title.cgi', 'Title Unmerge', 'Record', 'DisplayUnmergeTitle'),
  MOD_SERIES_UPDATE :	 ('sv_update', 'SeriesUpdate', 'pe.cgi', 'Series Update', 'Record', 'DisplaySeriesChanges'),
  MOD_CONTENT_UPDATE :	 ('cv_update', 'ContentUpdate', None, None, 'Record'), #currently unused
  MOD_VARIANT_TITLE:	 ('vv_new',    'VariantTitle', 'title.cgi', 'Add Variant Title', 'Record', 'DisplayAddVariant'),
  MOD_TITLE_MKVARIANT:	 ('kv_new',    'MakeVariant', 'title.cgi', 'Make Variant Title', 'Record', 'DisplayMakeVariant'),
  MOD_RMTITLE:		 ('tv_remove', 'TitleRemove', 'pl.cgi', 'Remove Title', 'Record', 'DisplayRemoveTitle'),
  MOD_PUB_CLONE :	 ('cv_new',    'NewPub', 'pl.cgi', 'Clone Publication', 'Record', 'DisplayClonePublication'),
  MOD_AUTHOR_PSEUDO :	 ('yv_new',    'MakePseudonym', 'ea.cgi', 'Create Pseudonym', 'Record', 'DisplayMakePseudonym'),
  MOD_AWARD_NEW :	 ('wv_new',    'NewAward', 'award_details.cgi', 'New Award', 'Record', 'DisplayNewAward'),
  MOD_AWARD_UPDATE :	 ('wv_update', 'AwardUpdate', 'award_details.cgi', 'Award Update', 'Record', 'DisplayAwardEdit'),
  MOD_AWARD_DELETE :	 ('wv_delete', 'AwardDelete', None, 'Award Delete', 'Record', 'DisplayAwardDelete'),
  MOD_PUBLISHER_UPDATE : ('xv_update', 'PublisherUpdate', 'publisher.cgi', 'Publisher Update', 'Record', 'DisplayPublisherChanges'),
  MOD_PUBLISHER_MERGE :	 ('uv_merge',  'PublisherMerge', 'publisher.cgi', 'Publisher Merge', 'Record', 'DisplayPublisherMerge'),
  MOD_REVIEW_LINK :	 ('rv_link',   'LinkReview', 'title.cgi', 'Link Review', 'Record', 'DisplayLinkReview'),
  MOD_DELETE_SERIES :	 ('sv_delete', 'SeriesDelete', None, 'Delete Series', 'Record', 'DisplaySeriesDelete'),
  MOD_REMOVE_PSEUDO :    ('yv_remove', 'RemovePseud', 'ea.cgi', 'Remove Pseudonym', 'Record', 'DisplayRemovePseudonym'),
  MOD_PUB_SERIES_UPDATE: ('zv_update', 'PubSeriesUpdate', 'pubseries.cgi', 'Publication Series Update', 'Record', 'DisplayPubSeriesChanges'),
  MOD_AWARD_TYPE_UPDATE: ('award_type_update_display', 'AwardTypeUpdate', 'awardtype.cgi', 'Award Type Update', 'Record', 'DisplayAwardTypeChanges'),
  MOD_AWARD_LINK:        ('award_link_display', 'LinkAward', 'award_details.cgi', 'Link Award', 'Award', 'DisplayAwardLink'),
  MOD_AWARD_TYPE_NEW:    ('award_type_new_display', 'NewAwardType', 'awardtype.cgi', 'Add New Award Type', 'Record', 'DisplayNewAwardType'),
  MOD_AWARD_TYPE_DELETE: ('award_type_delete_display', 'AwardTypeDelete', None, 'Delete Award Type', 'AwardTypeId', 'DisplayAwardTypeDelete'),
  MOD_AWARD_CAT_NEW:     ('award_cat_new_display', 'NewAwardCat', 'award_category.cgi', 'Add New Award Category', 'Record', 'DisplayNewAwardCat'),
  MOD_AWARD_CAT_DELETE:  ('award_cat_delete_display', 'AwardCategoryDelete', None, 'Delete Award Category', 'Record', 'DisplayAwardCatDelete'),
  MOD_AWARD_CAT_UPDATE:  ('award_cat_update_display', 'AwardCategoryUpdate', 'award_category.cgi', 'Award Category Update', 'AwardCategoryId', 'DisplayAwardCatChanges')
}

# This list of supported languages MUST be kept in sync with the "languages" table in MySQL
LANGUAGES = ('None','Afrikaans','Albanian','Ancient Greek','Arabic','Armenian',
             'Azerbaijani','Basque','Belarusian','Bengali','Bulgarian','Burmese',
             'Catalan','Chinese','Czech','Danish','Dutch','English','Esperanto',
             'Estonian','Filipino','Finnish','French','Frisian','Galician','Georgian',
             'German','Greek','Gujarati','Hebrew','Hindi','Croatian','Hungarian',
             'Icelandic','Indonesian','Irish','Italian','Japanese','Kazakh','Khmer',
             'Kyrgyz','Korean','Latvian','Latin','Lithuanian','Macedonian','Malay',
             'Malayalam','Marathi','Mongolian','Norwegian','Persian','Polish','Portuguese',
             'Romanian','Russian','Scottish Gaelic','Slovak','Slovenian','Spanish',
             'Serbian','Sinhalese','Swedish','Tajik','Tamil','Thai','Tibetan','Turkish',
             'Ukrainian','Urdu','Uzbek','Vietnamese','Welsh','Yiddish','Amharic',
             'Bosnian','Hausa','Hawaiian','Javanese','Judeo-Arabic','Karen','Ladino',
             'Maltese','Minangkabau','Nyanja','Panjabi','Samoan','Sindhi','Somali',
             'Sundanese','Swahili','Tagalog','Tatar','Telugu','Uighur','Sanskrit',
             'Serbo-Croatian Cyrillic','Serbo-Croatian Roman', 'Scots', 'Old English',
             'Old French', 'Middle English', 'Middle High German', 'Yoruba',
             'Mayan language', 'Akkadian', 'Sumerian', 'Norwegian (Bokmal)',
             'Norwegian (Nynorsk)', 'Asturian/Bable', 'Middle French', 'Low German',
             'Nepali', 'Pashto/Pushto', 'Shona', 'Old Norse', 'Nilo-Saharan language',
             'Bambara', 'Bantu language', 'Niger-Kordofanian language', 'Ewe', 'Igbo',
             'Kamba', 'Kannada', 'Kikuyu/Gikuyu', 'Kurdish', 'Lingala',
             'Creole or pidgin, French-based', 'Central American Indian language',
             'Nandi', 'Creole or pidgin, English-based', 'Tigre', 'Tigrinya', 'Tsonga',
             'Tswana', 'Zulu')

# List of all supported format codes
FORMATS = ('unknown','hc','tp','pb','ph','digest','dos','ebook','webzine','pulp',
            'bedsheet','tabloid','A4','A5','quarto','octavo','audio CD','audio MP3 CD',
            'audio cassette','audio LP','digital audio player','digital audio download','other')

STORYLEN_CODES = ('', 'novella', 'short story', 'novelette')

REGULAR_TITLE_TYPES = ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'EDITOR', 'ESSAY',
                       'INTERIORART', 'NONFICTION', 'NOVEL', 'OMNIBUS', 'POEM',
                       'SERIAL', 'SHORTFICTION')

ALL_TITLE_TYPES = sorted(REGULAR_TITLE_TYPES + ('COVERART', 'REVIEW', 'INTERVIEW'))

PUB_TYPES = ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'FANZINE', 'MAGAZINE', 'NONFICTION', 'NOVEL', 'OMNIBUS')

SUBMISSION_DISPLAY = {
    'AuthorTransLegalNames': 'Trans. Legal Name',
    'AuthorTransNames': 'Transliterated Name',
    'AwardedBy': 'Awarded By',
    'AwardedFor': 'Awarded For',
    'AwardAuthors': 'Award Authors',
    'AwardCategory': 'Category',
    'AwardLevel': 'Award Level',
    'AwardMovie': 'Award Movie',
    'AwardNote': 'Note',
    'AwardTitle': 'Award Title',
    'AwardType': 'Award Type',
    'AwardYear': 'Award Year',
    'Binding': 'Format',
    'Birthdate': 'Birth Date',
    'Birthplace': 'Birth Place',
    'Canonical': 'Canonical Name',
    'CategoryName': 'Award Category',
    'ContentIndicator': 'Content',
    'Deathdate': 'Death Date',
    'DisplayOrder': 'Display Order',
    'Emails': 'Email Address',
    'External_ID': 'External ID',
    'Familyname': 'Directory Entry',
    'FullName': 'Full Name',
    'Graphic': 'Graphic Format',
    'Isbn': 'ISBN',
    'Catalog': 'Catalog ID',
    'Legalname': 'Legal Name',
    'NonGenre': 'Non-Genre',
    'Parentposition': 'Series Parent Position',
    'PublisherTransNames': 'Transliterated Name',
    'PubSeries': 'Pub Series',
    'PubSeriesNum': 'Pub Series #',
    'PubSeriesTransNames': 'Transliterated Name',
    'PubType': 'Pub Type',
    'Seriesnum': 'Series Number',
    'SeriesNum': 'Series Number',
    'ShortName': 'Short Name',
    'Storylen': 'Length',
    'TitleNote': 'Title Note',
    'TranslitTitles': 'Transliterated Title',
    'TransTitles': 'Transliterated Title',
    'Webpages': 'Web Page',
    'Year': 'Date'
    }

# Alternative Unicode question marks: '&#10068;' (white) '&#10067;' (black)
QUESTION_MARK = '?'
# "More info" sign for mouseover bubbles
INFO_SIGN = '&#x24d8;'
