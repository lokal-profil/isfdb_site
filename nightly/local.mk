#
#     (C) COPYRIGHT 2013-2022   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_HTML)/nightly

MYLIBS	= dup_authors.py \
	  nightly_3rd_parties.py \
          nightly_awards.py \
	  nightly_cleanup.py \
	  nightly_html.py \
	  nightly_lib.py \
	  database_stats.py \
	  transliterations.py \
	  nightly_wiki.py

LIBS	= authorClass.py \
	  awardClass.py \
	  awardcatClass.py \
	  awardtypeClass.py \
	  titleClass.py \
	  pubClass.py \
	  publisherClass.py \
	  pubseriesClass.py \
	  seriesClass.py \
	  verificationsourceClass.py \
	  install.py \
	  isbn.py \
	  library.py \
	  navbar.py \
	  viewers.py \
	  login.py \
	  SQLparsing.py \
	  isfdb.py \
	  sfe3.py

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.py:	%.py
		python install_nightly.py $* local /usr/bin/python

local/%.jpg:	%.jpg
		cp $*.jpg local

check_dirs:
		if test -d $(INSTALL); \
		then echo $(INSTALL) exists; \
		else mkdir $(INSTALL); \
		fi

install:	all check_dirs
		rm -f $(INSTALL)/*.pyc
		cp local/* $(INSTALL)
		chmod 744 $(INSTALL)/*.py

clean:
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local

