#
#     (C) COPYRIGHT 2005-2021   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import cgitb; cgitb.enable()
import sys
import os
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
    print """Content-Security-Policy: form-action 'self' http://%s https://www.google.com;""" % HTMLHOST
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
    # Calculate the banner number for today; the range is 1-12
    banner_number = (elapsed.days % 12) + 1
    print '<img src="http://%s/IsfdbBanner%d.jpg" alt="ISFDB banner">' % (HTMLHOST, banner_number)
    print '</span>'
    print '</a>'
    print '<div id="statusbar">'
    print '<h2>%s</h2>' % (title)

class Session:
    def __init__(self):
        self.cgi_script = ''
        self.parameters = []

    def ParseParameters(self):
        script = sys.argv[0]
        # Some OSes put the full path name in sys.argv[0], so we extract the last "/" chunk
        file_name = script.split('/')[-1]
        if file_name.endswith('.cgi'):
            file_name = file_name[0:-4]
        self.cgi_script = file_name

        # We get the query string from os.environ.get('QUERY_STRING') as opposed to sys.argv
        # because some third party sites like Facebook add '&key=value' data to ISFDB URLs
        self.query_string = os.environ.get('QUERY_STRING')
        for parameter in self.query_string.split('+'):
                parameter = parameter.split('&fbclid=')[0] # Strip trailing Facebook IDs
                self.parameters.append(parameter)

    def Parameter(self, param_number, param_type = 'str', default_value = None, allowed_values = []):
        param_display_values = {0: 'First',
                                1: 'Second',
                                2: 'Third',
                                3: 'Fourth',
                                4: 'Fifth',
                                5: 'Sixth',
                                6: 'Seventh',
                                7: 'Eight',
                                8: 'Nineth',
                                9: 'Tenth'
                                }
        if param_number not in param_display_values:
            self.DisplayError('Too many parameters. Only %d parameters are allowed.' % len(param_display_values))
        param_order = param_display_values[param_number]
        
        try:
            value = self.parameters[param_number]
            if not value:
                raise
        except:
            value = ''
        if not value and default_value is not None:
            value = default_value
        if not value:
            self.DisplayError('%s parameter not specified' % param_order)
        
        if param_type == 'int':
            try:
                value = int(value)
            except:
                self.DisplayError('%s parameter must be numeric' % param_order)
        
        if allowed_values and value not in allowed_values:
            output = '%s parameter must be one of the following values: ' % param_order
            for count, allowed_value in enumerate(allowed_values):
                if count:
                    output += ', '
                output += allowed_value
            self.DisplayError(output)
        return value
    
    def DisplayError(self, message):
        from common import PrintHeader, PrintNavbar, PrintTrailer
        PrintHeader('Page Does Not Exist')
        try:
            record_id = int(self.parameter[0])
        except:
            record_id = 0
        PrintNavbar(self.cgi_script, record_id, 0, '%s.cgi' % self.cgi_script, 0)
        print """<h3>%s</h3>""" % message
        PrintTrailer(self.cgi_script, record_id, 0)
        sys.exit(0)

SCHEMA_VER = "0.02"
ENGINE     = "<b>ISFDB Engine</b> - Version 4.00 (2006-04-24)"
COPYRIGHT  = "Copyright &copy; 1995-2021 Al von Ruff and the ISFDB team"
# NONCE should be uncommented if and when we need it to create CSP nonces
# import uuid
# NONCE = uuid.uuid4().hex

SESSION = Session()
SESSION.ParseParameters()

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
SERIES_TYPE_COVERART    = 8
SERIES_TYPE_INTERIORART = 9
SERIES_TYPE_REVIEW      = 10
SERIES_TYPE_INTERVIEW   = 11
SERIES_TYPE_OTHER       = 12

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

# Field offsets for Web Pages records
WEBPAGE_ID           = 0
WEBPAGE_AUTHOR       = 1
WEBPAGE_PUBLISHER    = 2
WEBPAGE_URL          = 3
WEBPAGE_PUB_SERIES   = 4
WEBPAGE_TITLE        = 5
WEBPAGE_AWARD_TYPE   = 6
WEBPAGE_SERIES       = 7
WEBPAGE_AWARD_CAT    = 8
WEBPAGE_PUB          = 9

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

# Field offsets for Deleted Secondary Verification
DEL_VER_ID            = 0
DEL_VER_PUB_ID        = 1
DEL_VER_REFERENCE_ID  = 2
DEL_VER_VERIFIER_ID   = 3
DEL_VER_VERIFICATION_TIME = 4
DEL_VER_DELETER_ID    = 5
DEL_VER_DELETION_TIME = 6

# Recognized submission types
MOD_AUTHOR_MERGE     = 1
MOD_AUTHOR_UPDATE    = 2
MOD_AUTHOR_DELETE    = 3 # Never used
MOD_PUB_UPDATE       = 4
MOD_PUB_MERGE        = 5 # No longer used
MOD_PUB_DELETE       = 6
MOD_PUB_NEW          = 7 # Edit History supported for submissions created after 2016-10-24
MOD_TITLE_UPDATE     = 8
MOD_TITLE_MERGE      = 9
MOD_TITLE_DELETE     = 10
MOD_TITLE_NEW        = 11 # Never used
MOD_TITLE_UNMERGE    = 12
MOD_SERIES_UPDATE    = 13
MOD_CONTENT_UPDATE   = 14 # Never used
MOD_VARIANT_TITLE    = 15 # Edit History supported for submissions created after 2021-01-11
MOD_TITLE_MKVARIANT  = 16
MOD_RMTITLE          = 17
MOD_PUB_CLONE        = 18 # Edit History supported for submissions created after 2016-10-24
MOD_AUTHOR_PSEUDO    = 19
MOD_AWARD_NEW        = 20 # Edit History supported for submissions created after 2016-10-24
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
MOD_AWARD_TYPE_NEW   = 31 # Edit History supported for submissions created after 2016-10-24
MOD_AWARD_TYPE_DELETE= 32
MOD_AWARD_CAT_NEW    = 33 # Edit History supported for submissions created after 2016-10-24
MOD_AWARD_CAT_DELETE = 34
MOD_AWARD_CAT_UPDATE = 35

# SUBMAP is a dictionary used to store information about submission types
# [0] - Name of the moderator review script
# [1] - Short name of the submission type and the first XML tag in the submission; displayed on submission list pages
# [2] - Name of the script used to link to the record from the list of recent entries
# [3] - Full name of the submission type, used in stats-and-tops.py
# [4] - Name of the XML element containing the record number in the submission -- used to link from the list of recent entries
# [5] - Name of the "viewers" function used to display the body of this submission type
# [6] - Name of the filing script
SUBMAP = {
  MOD_AUTHOR_MERGE :	 ('av_merge',  'AuthorMerge', 'ea.cgi', 'Author Merge', 'Record', 'DisplayAuthorMerge', 'aa_merge'),
  MOD_AUTHOR_UPDATE :	 ('av_update', 'AuthorUpdate', 'ea.cgi', 'Author Update', 'Record', 'DisplayAuthorChanges', 'aa_update'),
  MOD_AUTHOR_DELETE :	 ('av_delete', 'AuthorDelete', None, None, 'Record'), # currently unused
  MOD_PUB_UPDATE :	 ('pv_update', 'PubUpdate', 'pl.cgi', 'Publication Update', 'Record', 'DisplayEditPub', 'pa_update'),
  MOD_PUB_DELETE :	 ('pv_delete', 'PubDelete', 'pl.cgi', 'Publication Delete', 'Record', 'DisplayDeletePub', 'pa_delete'),
  MOD_PUB_NEW :		 ('pv_new',    'NewPub', 'pl.cgi', 'New Publication', 'Record', 'DisplayNewPub', 'pa_new'),
  MOD_TITLE_UPDATE :	 ('tv_update', 'TitleUpdate', 'title.cgi', 'Title Update', 'Record', 'DisplayTitleEdit', 'ta_update'),
  MOD_TITLE_MERGE :	 ('tv_merge',  'TitleMerge', 'title.cgi', 'Title Merge', 'Record', 'DisplayMergeTitles', 'ta_merge'),
  MOD_TITLE_DELETE :	 ('tv_delete', 'TitleDelete', 'title.cgi', 'Title Delete', 'Record', 'DisplayTitleDelete', 'ta_delete'),
  MOD_TITLE_NEW :	 ('tv_new',    'TitleNew', None, None, 'Record'), #currently unused, but referenced in submittitle
  MOD_TITLE_UNMERGE :	 ('tv_unmerge','TitleUnmerge', 'title.cgi', 'Title Unmerge', 'Record', 'DisplayUnmergeTitle', 'ta_unmerge'),
  MOD_SERIES_UPDATE :	 ('sv_update', 'SeriesUpdate', 'pe.cgi', 'Series Update', 'Record', 'DisplaySeriesChanges', 'sa_update'),
  MOD_CONTENT_UPDATE :	 ('cv_update', 'ContentUpdate', None, None, 'Record'), #currently unused
  MOD_VARIANT_TITLE:	 ('vv_new',    'VariantTitle', 'title.cgi', 'Add Variant Title', 'Record', 'DisplayAddVariant', 'va_new'),
  MOD_TITLE_MKVARIANT:	 ('kv_new',    'MakeVariant', 'title.cgi', 'Make Variant Title', 'Record', 'DisplayMakeVariant', 'ka_new'),
  MOD_RMTITLE:		 ('tv_remove', 'TitleRemove', 'pl.cgi', 'Remove Title', 'Record', 'DisplayRemoveTitle', 'ta_remove'),
  MOD_PUB_CLONE :	 ('cv_new',    'NewPub', 'pl.cgi', 'Clone Publication', 'Record', 'DisplayClonePublication', 'ca_new'),
  MOD_AUTHOR_PSEUDO :	 ('yv_new',    'MakePseudonym', 'ea.cgi', 'Create Alternate Name', 'Record', 'DisplayMakePseudonym', 'ya_new'),
  MOD_AWARD_NEW :	 ('wv_new',    'NewAward', 'award_details.cgi', 'New Award', 'Record', 'DisplayNewAward', 'wa_new'),
  MOD_AWARD_UPDATE :	 ('wv_update', 'AwardUpdate', 'award_details.cgi', 'Award Update', 'Record', 'DisplayAwardEdit', 'wa_update'),
  MOD_AWARD_DELETE :	 ('wv_delete', 'AwardDelete', None, 'Award Delete', 'Record', 'DisplayAwardDelete', 'wa_delete'),
  MOD_PUBLISHER_UPDATE : ('xv_update', 'PublisherUpdate', 'publisher.cgi', 'Publisher Update', 'Record', 'DisplayPublisherChanges', 'xa_update'),
  MOD_PUBLISHER_MERGE :	 ('uv_merge',  'PublisherMerge', 'publisher.cgi', 'Publisher Merge', 'Record', 'DisplayPublisherMerge', 'ua_merge'),
  MOD_REVIEW_LINK :	 ('rv_link',   'LinkReview', 'title.cgi', 'Link Review', 'Record', 'DisplayLinkReview', 'ra_link'),
  MOD_DELETE_SERIES :	 ('sv_delete', 'SeriesDelete', None, 'Delete Series', 'Record', 'DisplaySeriesDelete', 'sa_delete'),
  MOD_REMOVE_PSEUDO :    ('yv_remove', 'RemovePseud', 'ea.cgi', 'Remove Alternate Name', 'Record', 'DisplayRemovePseudonym', 'ya_remove'),
  MOD_PUB_SERIES_UPDATE: ('zv_update', 'PubSeriesUpdate', 'pubseries.cgi', 'Publication Series Update', 'Record', 'DisplayPubSeriesChanges', 'za_update'),
  MOD_AWARD_TYPE_UPDATE: ('award_type_update_display', 'AwardTypeUpdate', 'awardtype.cgi', 'Award Type Update', 'Record', 'DisplayAwardTypeChanges', 'award_type_update_file'),
  MOD_AWARD_LINK:        ('award_link_display', 'LinkAward', 'award_details.cgi', 'Link Award', 'Award', 'DisplayAwardLink', 'award_link_file'),
  MOD_AWARD_TYPE_NEW:    ('award_type_new_display', 'NewAwardType', 'awardtype.cgi', 'Add New Award Type', 'Record', 'DisplayNewAwardType', 'award_type_new_file'),
  MOD_AWARD_TYPE_DELETE: ('award_type_delete_display', 'AwardTypeDelete', None, 'Delete Award Type', 'AwardTypeId', 'DisplayAwardTypeDelete', 'award_type_delete_file'),
  MOD_AWARD_CAT_NEW:     ('award_cat_new_display', 'NewAwardCat', 'award_category.cgi', 'Add New Award Category', 'Record', 'DisplayNewAwardCat', 'award_cat_new_file'),
  MOD_AWARD_CAT_DELETE:  ('award_cat_delete_display', 'AwardCategoryDelete', None, 'Delete Award Category', 'Record', 'DisplayAwardCatDelete', 'award_cat_delete_file'),
  MOD_AWARD_CAT_UPDATE:  ('award_cat_update_display', 'AwardCategoryUpdate', 'award_category.cgi', 'Award Category Update', 'AwardCategoryId', 'DisplayAwardCatChanges', 'award_cat_update_file')
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
             'Tswana', 'Zulu', 'Acoli', 'Fulah', 'Ganda', 'Kinyarwanda', 'Luo', 'Mandingo',
             'Oriya', 'Pedi/Sepedi/Northern Sotho', 'South Ndebele', 'Southern Sotho',
             'Standard Moroccan Tamazight', 'Wolof', 'North Ndebele', 'Montenegrin',
             'Mirandese', 'Lao', 'South American Indian language', 'Interlingua',
             'Guarani', 'Maithili', 'Romance language', 'Klingon')

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
    'PubWebpages': 'Publication Web Page',
    'PubType': 'Pub Type',
    'Seriesnum': 'Series Number',
    'SeriesNum': 'Series Number',
    'SeriesTransNames': 'Transliterated Name',
    'ShortName': 'Short Name',
    'Storylen': 'Length',
    'TitleNote': 'Title Note',
    'TranslitTitles': 'Transliterated Title',
    'TransTitles': 'Transliterated Title',
    'Webpages': 'Web Page',
    'Year': 'Date'
    }

SUBMISSION_TYPE_DISPLAY = {
    'MakePseudonym': 'Make Alternate Name',
    'RemovePseud': 'Remove Alternate Name'    
    }

# Alternative Unicode question marks: '&#10068;' (white) '&#10067;' (black)
QUESTION_MARK = '?'
# "More info" sign for mouseover bubbles
INFO_SIGN = '&#x24d8;'

ENGLISH_LOWER_CASE = ['and', 'or', 'the', 'a', 'an', 'for', 'of', 'in', 'on', 'by', 'at', 'from', 'with', 'to']

MAX_FUTURE_DAYS = 90

# Irregular author names that should be ignored for cases like:
# * Setting author_marque to 1 to appear on the forthcoming books section
# * Cleanup report 11: Prolific Authors Without a Defined Language
# * Cleanup report 19: Interviews of Pseudonyms
# * Cleanup reports 58-61: Suspected X Authors without a Language Code
# * others...?
# If some of them need different sets of values, define them as separate
# lists here, then concatenate them all into SPECIAL_AUTHORS_TO_IGNORE
SPECIAL_AUTHORS_TO_IGNORE = [
    'unknown', # 2862
    'uncredited', # 20754
    'various', # 7311
    'The Readers', # 25179
    'Anonymous', # 6677
    'Traditional', # 17640
    'The Editors' # 38941
]

EURO_SIGN = chr(128)
POUND_SIGN = chr(163)
YEN_SIGN = chr(165)
BULLET = '&#8226;'
