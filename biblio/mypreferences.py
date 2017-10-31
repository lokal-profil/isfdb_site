#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2016   Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import string
import sys
import MySQLdb
from isfdb import *
from common import *
from login import *


if __name__ == '__main__':

	PrintHeader("User Preferences")
	PrintNavbar('mypreferences', 0, 0, 'mypreferences.cgi', 0)

        user = User()
        user.load()
	if not user.id:
                print 'You must be logged in to modify your user preferences'
        	PrintTrailer('mypreferences', 0, 0)
                sys.exit(0)

       
        print '<form id="data" METHOD="POST" ACTION="/cgi-bin/submitpreferences.cgi">'
        print '<ul>'
        print '<li><a href="http:/%s/edit/keygen.cgi">Key Maintenance</a></li><br>' % (HTFAKE)
        print '<li><a href="http:/%s/mywebsites.cgi">My Web Sites</a></li><br>' % (HTFAKE)

        print '<b>Publication Pages</b><br>'
        
	concise_checked = ''
	if user.concise_display:
                concise_checked = 'checked'
        print '<li><input type="checkbox" name="concise_display" value="on"'
        print ' %s>%s</li>' % (concise_checked, "Use concise Publication listing by default")
        print '<br>'

        print '<b>Title Pages</b><br>'
        
	covers_checked = ''
	if user.covers_display:
                covers_checked = 'checked'
        print '<li><input type="checkbox" name="covers_display" value="on"'
        print ' %s>%s</li>' % (covers_checked, "Display cover images on Title pages")

	suppress_bibliographic_warnings = ''
	if user.suppress_bibliographic_warnings:
                suppress_bibliographic_warnings = 'checked'
        print '<li><input type="checkbox" name="suppress_bibliographic_warnings" value="on"'
        print ' %s>%s</li>' % (suppress_bibliographic_warnings, "Do not display bibliographic warnings on Title pages")

	suppress_awards = ''
	if user.suppress_awards:
                suppress_awards = 'checked'
        print '<li><input type="checkbox" name="suppress_awards" value="on"'
        print ' %s>%s</li>' % (suppress_awards, "Do not display awards on Title pages")

	suppress_reviews = ''
	if user.suppress_reviews:
                suppress_reviews = 'checked'
        print '<li><input type="checkbox" name="suppress_reviews" value="on"'
        print ' %s>%s</li>' % (suppress_reviews, "Do not display reviews on Title pages")

	cover_links_display = ''
	if user.cover_links_display:
                cover_links_display = 'checked'
        print '<li><input type="checkbox" name="cover_links_display" value="on"'
        print ' %s>%s</li>' % (cover_links_display, "Display cover scan indicators on Title and search pages")
        print '<br>'

        print '<b>Searching</b><br>'
        
	keep_spaces_in_searches = ''
	if user.keep_spaces_in_searches:
                keep_spaces_in_searches = 'checked'
        print '<li><input type="checkbox" name="keep_spaces_in_searches" value="on"'
        print ' %s>%s</li>' % (keep_spaces_in_searches, "Keep leading and trailing spaces when searching")
        print '<br>'

        print '<b>Editing</b><br>'
        
        suppress_help_bubbles = ''
	if user.suppress_help_bubbles:
                suppress_help_bubbles = 'checked'
        print '<li><input type="checkbox" name="suppress_help_bubbles" value="on"'
        print ' %s>%s</li>' % (suppress_help_bubbles, "Do not display mouseover help on Edit pages")

        if SQLisUserModerator(user.id):
                display_post_submission = ''
                if user.display_post_submission:
                        display_post_submission = 'checked'
                print '<li><input type="checkbox" name="display_post_submission" value="on"'
                print ' %s>%s</li>' % (display_post_submission, "Display post-submission review pages")

        print "<li>Default author/title language when editing records: "
        print '<select name="default_language">'

        # Iterate over an alphabetized list of language names (excluding 'None' in the 0th position)
        # and display them in a drop-down list
        for language_name in sorted(LANGUAGES[1:]):
                language_id = list(LANGUAGES).index(language_name)
                # If this language is the user's current default language, then select it
                if language_name == LANGUAGES[user.default_language]:
                        print '<option selected="selected" value="%s">%s</option>' % (language_id, language_name)
                # Otherwise this language is displayed, but is not "selected"
                else:
                        print '<option value="%s">%s</option>' % (language_id, language_name)
        print "</select>"

        print '<br>'
        print '<br>'
        print '<b>Translations</b><br>'

        print '<li>Display translations: '
        print '<select name="display_all_languages">'
        for value in ('All', 'None', 'Selected'):
                if value == user.display_all_languages:
                        print '<option selected="selected">%s</option>' % value
                else:
                        print '<option>%s</option>' % value
        print '</select>'
        print ' (if you chose "Selected", you should also set up <a href="http:/%s/mylanguages.cgi">Translation Preferences</a>)' % (HTFAKE)
	suppress_translation_warnings = ''
	if user.suppress_translation_warnings:
                suppress_translation_warnings = 'checked'
        print '<li><input type="checkbox" name="suppress_translation_warnings" value="on"'
        print ' %s>%s</li>' % (suppress_translation_warnings, "Do not display translation warnings on Author and Series pages")
        print '<br>'

        print '</ul>'
	print '<input type="SUBMIT" value="Update Preferences">'
        print '</form>'

	PrintTrailer('mypreferences', 0, 0)

