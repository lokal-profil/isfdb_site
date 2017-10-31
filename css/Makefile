#
#     (C) COPYRIGHT 2008-2015   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


# Need to create index.html

include ../INSTALLDIRS

INSTALL = $(INSTALL_HTML)

TARGETS	= apple-touch-icon.png \
	  apple-touch-icon-precomposed.png \
	  biblio.css \
	  checkmark.png \
	  isfdb.gif \
	  isfdb_logo.jpg \
	  index.html \
	  IsfdbBanner.jpg \
	  question_mark_icon.gif \
	  edit_js.js \
	  edit_pub.js \
	  edit_author.js \
	  edit_award.js \
	  edit_other.js \
	  edit_title.js

install:
	python index_install.py
	cp $(TARGETS) $(INSTALL)

clean: clobber

clobber:
	rm -f localdefs.*
	rm -f index.html
