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
import string
import sys
import os
from localdefs import *
import urllib

def PrintHTMLHeaders(title):
    from datetime import date
    # Disallow the <base> directive
    policy = "base-uri 'none';"
    # Disallow <a> ping, Fetch, XMLHttpRequest, WebSocket, and EventSource
    #   May need to be re-worked if we implement AJAX
    policy += " connect-src 'none';"
    # Disallow @font-face
    policy += " font-src 'none';"
    # Restrict form submission URLs to the ISFDB server
    policy += " form-action 'self' %s://%s https://www.google.com;" % (PROTOCOL, HTMLHOST)
    # Disable nested browsing contexts
    policy += " frame-src 'none';"
    # Disable <frame>, <iframe>, <object>, <embed>, and <applet>
    policy += " frame-ancestors 'none';"
    # Restrict sources of images and favicons to http and https
    policy += " img-src http: https:;"
    # Disallow <manifest>
    policy += " manifest-src 'none';"
    # Disallow <audio>, <track> and <video>
    policy += " media-src 'none';"
    # Disallow <object>, <embed>, and <applet>
    policy += " object-src 'none';"
    # Limit JS scripts to .js files served by the ISFDB server
    policy += " script-src 'self' %s://%s;" % (PROTOCOL, HTMLHOST)
    # Limit stylesheets to .css files served by the ISFDB server
    policy += " style-src 'self' %s://%s;" % (PROTOCOL, HTMLHOST)
    # Disable Worker, SharedWorker, or ServiceWorker scripts
    #   May need to be re-worked if we implement workers
    policy += " worker-src 'none';"
    print """Content-Security-Policy: %s""" % policy
    
    # Declare content type and end the http headers section with a \n
    print 'Content-type: text/html; charset=%s\n' % UNICODE
    # The DTD Web page for the HTML standard redirects to https, but the standard
    # and HTML validators still uses http in the page name, so that's what we use
    print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
    print '<html lang="en-us">'
    print '<head>'
    print '<meta http-equiv="content-type" content="text/html; charset=%s" >' % UNICODE
    print '<link rel="shortcut icon" href="%s://%s/favicon.ico">' % (PROTOCOL, HTMLHOST)
    print '<title>%s</title>' % title
    print '<link href="%s://%s/biblio.css" rel="stylesheet" type="text/css" media="screen">' % (PROTOCOL, HTMLHOST)
    print '</head>'
    print '<body>'
    print '<div id="wrap">'
    print '<a class="topbanner" href="%s:/%s/index.cgi">' % (PROTOCOL, HTFAKE)
    print '<span>'
    # Get the number of days since January 1, 2000
    millenium = date(2000, 1, 1)
    today = date.today()
    elapsed = today - millenium
    # Calculate the banner number for today; the range is 1-12
    banner_number = (elapsed.days % 12) + 1
    print '<img src="%s://%s/IsfdbBanner%d.jpg" alt="ISFDB banner">' % (PROTOCOL, HTMLHOST, banner_number)
    print '</span>'
    print '</a>'
    print '<div id="statusbar">'
    print '<h2>%s</h2>' % (title)

class Session:
    def __init__(self):
        self.cgi_dir = ''
        self.cgi_script = ''
        self.parameters = []
        self.query_string = ''
        self.frame = 1 # Flag indicating whether the framing divs need to be displayed

    def ParseParameters(self):
        cgi_path = os.environ.get('SCRIPT_NAME')
        # CGI script name is in the last "/" chunk
        if cgi_path:
            self.cgi_script = cgi_path.split('/')[-1]
            if self.cgi_script.endswith('.cgi'):
                self.cgi_script = self.cgi_script[0:-4] # Strip the trailing ".cgi" string
            self.cgi_dir = cgi_path.split('/')[-2]

        self.query_string = os.environ.get('QUERY_STRING')
        if self.query_string:
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
            self.DisplayError('Invalid parameter. Only %d parameters are allowed.' % len(param_display_values))
        param_order = param_display_values[param_number]
        
        try:
            value = self.parameters[param_number]
            if not value:
                raise
        except:
            value = ''
        if not value and default_value is not None:
            value = default_value
        if value == '':
            self.DisplayError('%s parameter not specified' % param_order)
        
        if param_type == 'int':
            try:
                value = int(value)
                if value < 0:
                    raise
            except:
                self.DisplayError('%s parameter must be a valid integer number' % param_order)
        elif param_type == 'unescape':
            value = string.replace(value, '%20', ' ')
            value = string.replace(value, '&rsquo;', "'")
            value = string.replace(value, '%E2%80%99', "'")
            value = string.replace(value, '_', ' ')
            value = string.replace(value, '\\', '')
            value = string.replace(value, '=', '')
            value = urllib.unquote(value).decode('utf-8').encode('iso-8859-1', 'xmlcharrefreplace')
        
        if allowed_values and value not in allowed_values:
            output = '%s parameter must be one of the following values: ' % param_order
            for count, allowed_value in enumerate(allowed_values):
                if count:
                    output += ', '
                output += '%s' % allowed_value
            self.DisplayError(output)
        return value

    def DisplayError(self, message, frame = 1):
        self.frame = frame
        if self.cgi_dir == 'cgi-bin':
            self._DisplayBiblioError(message)
        elif self.cgi_dir == 'edit':
            self._DisplayEditError(message)
        elif self.cgi_dir == 'mod':
            self._DisplayModError(message)
        elif self.cgi_dir == 'rest':
            print '%s.cgi: Bad query. %s' % (self.cgi_script, message)
        sys.exit(0)

    def _DisplayBiblioError(self, message):
        from common import PrintHeader, PrintNavbar, PrintTrailer
        if self.frame:
            PrintHeader('Error')
            try:
                record_id = int(self.parameter[0])
            except:
                record_id = 0
            PrintNavbar(self.cgi_script, record_id, 0, '%s.cgi' % self.cgi_script, 0)
        print """<h3>%s</h3>""" % message
        PrintTrailer(self.cgi_script, record_id, 0)

    def _DisplayEditError(self, message):
        from isfdblib import PrintPreSearch, PrintNavBar, PrintPostSearch
        if self.frame:
            PrintPreSearch('Error')
            PrintNavBar('%s/%s' % (self.cgi_dir, self.cgi_script), 0)
        print """<h3>%s</h3>""" % message
        PrintPostSearch(0, 0, 0, 0, 0, 0)

    def _DisplayModError(self, message):
        from isfdblib import PrintPreMod, PrintNavBar, PrintPostMod
        if self.frame:
            PrintPreMod('Error')
            PrintNavBar()
        print """<h3>%s</h3>""" % message
        PrintPostMod(0)

SCHEMA_VER = '0.02'
ENGINE     = '<b>ISFDB Engine</b> - Version 4.00 (2006-04-24)'
COPYRIGHT  = 'Copyright &copy; 1995-2021 Al von Ruff and the ISFDB team'
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

# Field offsets for Languages
LANGUAGE_ID           = 0
LANGUAGE_NAME         = 1
LANGUAGE_CODE         = 2
LANGUAGE_LATIN_SCRIPT = 3

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
MOD_LANGUAGE_NEW     = 36
MOD_VER_SOURCE_EDIT  = 37
MOD_VER_SOURCE_ADD   = 38

# SUBMAP is a dictionary used to store information about submission types
# [0] - Name of the moderator review script
# [1] - Short name of the submission type and the first XML tag in the submission; displayed on submission list pages
# [2] - Name of the script used to link to the record from the list of recent entries
# [3] - Full name of the submission type
# [4] - Name of the XML element containing the record number in the submission -- used to link from the list of recent entries
# [5] - Name of the "viewers" function used to display the body of this submission type
# [6] - Name of the filing script
SUBMAP = {
  MOD_AUTHOR_MERGE :	 ('submission_review', 'AuthorMerge', 'ea.cgi', 'Author Merge', 'Record', 'DisplayAuthorMerge', 'aa_merge'),
  MOD_AUTHOR_UPDATE :	 ('submission_review', 'AuthorUpdate', 'ea.cgi', 'Author Update', 'Record', 'DisplayAuthorChanges', 'aa_update'),
  MOD_AUTHOR_DELETE :	 ('submission_review', 'AuthorDelete', None, None, 'Record'), # currently unused
  MOD_PUB_UPDATE :	 ('submission_review', 'PubUpdate', 'pl.cgi', 'Publication Update', 'Record', 'DisplayEditPub', 'pa_update'),
  MOD_PUB_DELETE :	 ('submission_review', 'PubDelete', 'pl.cgi', 'Publication Delete', 'Record', 'DisplayDeletePub', 'pa_delete'),
  MOD_PUB_NEW :		 ('submission_review', 'NewPub', 'pl.cgi', 'New Publication', 'Record', 'DisplayNewPub', 'pa_new'),
  MOD_TITLE_UPDATE :	 ('submission_review', 'TitleUpdate', 'title.cgi', 'Title Update', 'Record', 'DisplayTitleEdit', 'ta_update'),
  MOD_TITLE_MERGE :	 ('submission_review', 'TitleMerge', 'title.cgi', 'Title Merge', 'Record', 'DisplayMergeTitles', 'ta_merge'),
  MOD_TITLE_DELETE :	 ('submission_review', 'TitleDelete', 'title.cgi', 'Title Delete', 'Record', 'DisplayTitleDelete', 'ta_delete'),
  MOD_TITLE_NEW :	 ('submission_review', 'TitleNew', None, None, 'Record'), #currently unused, but referenced in submittitle
  MOD_TITLE_UNMERGE :	 ('submission_review', 'TitleUnmerge', 'title.cgi', 'Title Unmerge', 'Record', 'DisplayUnmergeTitle', 'ta_unmerge'),
  MOD_SERIES_UPDATE :	 ('submission_review', 'SeriesUpdate', 'pe.cgi', 'Series Update', 'Record', 'DisplaySeriesChanges', 'sa_update'),
  MOD_CONTENT_UPDATE :	 ('submission_review', 'ContentUpdate', None, None, 'Record'), #currently unused
  MOD_VARIANT_TITLE:	 ('submission_review', 'VariantTitle', 'title.cgi', 'Add Variant Title', 'Record', 'DisplayAddVariant', 'va_new'),
  MOD_TITLE_MKVARIANT:	 ('submission_review', 'MakeVariant', 'title.cgi', 'Make Variant Title', 'Record', 'DisplayMakeVariant', 'ka_new'),
  MOD_RMTITLE:		 ('submission_review', 'TitleRemove', 'pl.cgi', 'Remove Title', 'Record', 'DisplayRemoveTitle', 'ta_remove'),
  MOD_PUB_CLONE :	 ('submission_review', 'NewPub', 'pl.cgi', 'Clone Publication', 'Record', 'DisplayClonePublication', 'ca_new'),
  MOD_AUTHOR_PSEUDO :	 ('submission_review', 'MakePseudonym', 'ea.cgi', 'Create Alternate Name', 'Record', 'DisplayMakePseudonym', 'ya_new'),
  MOD_AWARD_NEW :	 ('submission_review', 'NewAward', 'award_details.cgi', 'New Award', 'Record', 'DisplayNewAward', 'wa_new'),
  MOD_AWARD_UPDATE :	 ('submission_review', 'AwardUpdate', 'award_details.cgi', 'Award Update', 'Record', 'DisplayAwardEdit', 'wa_update'),
  MOD_AWARD_DELETE :	 ('submission_review', 'AwardDelete', None, 'Award Delete', 'Record', 'DisplayAwardDelete', 'wa_delete'),
  MOD_PUBLISHER_UPDATE : ('submission_review', 'PublisherUpdate', 'publisher.cgi', 'Publisher Update', 'Record', 'DisplayPublisherChanges', 'xa_update'),
  MOD_PUBLISHER_MERGE :	 ('submission_review', 'PublisherMerge', 'publisher.cgi', 'Publisher Merge', 'Record', 'DisplayPublisherMerge', 'ua_merge'),
  MOD_REVIEW_LINK :	 ('submission_review', 'LinkReview', 'title.cgi', 'Link Review', 'Record', 'DisplayLinkReview', 'ra_link'),
  MOD_DELETE_SERIES :	 ('submission_review', 'SeriesDelete', None, 'Delete Series', 'Record', 'DisplaySeriesDelete', 'sa_delete'),
  MOD_REMOVE_PSEUDO :    ('submission_review', 'RemovePseud', 'ea.cgi', 'Remove Alternate Name', 'Record', 'DisplayRemovePseudonym', 'ya_remove'),
  MOD_PUB_SERIES_UPDATE: ('submission_review', 'PubSeriesUpdate', 'pubseries.cgi', 'Publication Series Update', 'Record', 'DisplayPubSeriesChanges', 'za_update'),
  MOD_AWARD_TYPE_UPDATE: ('submission_review', 'AwardTypeUpdate', 'awardtype.cgi', 'Award Type Update', 'Record', 'DisplayAwardTypeChanges', 'award_type_update_file'),
  MOD_AWARD_LINK:        ('submission_review', 'LinkAward', 'award_details.cgi', 'Link Award', 'Award', 'DisplayAwardLink', 'award_link_file'),
  MOD_AWARD_TYPE_NEW:    ('submission_review', 'NewAwardType', 'awardtype.cgi', 'Add New Award Type', 'Record', 'DisplayNewAwardType', 'award_type_new_file'),
  MOD_AWARD_TYPE_DELETE: ('submission_review', 'AwardTypeDelete', None, 'Delete Award Type', 'AwardTypeId', 'DisplayAwardTypeDelete', 'award_type_delete_file'),
  MOD_AWARD_CAT_NEW:     ('submission_review', 'NewAwardCat', 'award_category.cgi', 'Add New Award Category', 'Record', 'DisplayNewAwardCat', 'award_cat_new_file'),
  MOD_AWARD_CAT_DELETE:  ('submission_review', 'AwardCategoryDelete', None, 'Delete Award Category', 'Record', 'DisplayAwardCatDelete', 'award_cat_delete_file'),
  MOD_AWARD_CAT_UPDATE:  ('submission_review', 'AwardCategoryUpdate', 'award_category.cgi', 'Award Category Update', 'AwardCategoryId', 'DisplayAwardCatChanges', 'award_cat_update_file'),
  MOD_LANGUAGE_NEW:      ('submission_review', 'NewLanguage', None, 'New Language', 'Record', 'DisplayNewLanguage', 'new_language_file'),
  MOD_VER_SOURCE_EDIT:   ('submission_review', 'VerificationSource', None, 'Edit Verification Source', 'Record', 'DisplayVerificationSourceEdit', 'verification_source_file'),
  MOD_VER_SOURCE_ADD:    ('submission_review', 'VerificationSource', None, 'Add Verification Source', 'Record', 'DisplayVerificationSourceAdd', 'verification_source_add_file')
}

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

BAHT_SIGN = '&#3647;'
EURO_SIGN = chr(128)
PESO_SIGN = '&#8369;'
POUND_SIGN = chr(163)
YEN_SIGN = chr(165)

BULLET = '&#8226;'
