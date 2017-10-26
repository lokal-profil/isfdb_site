#
#     (C) COPYRIGHT 2013-2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.7 $
#     Date: $Date: 2017/05/08 17:30:18 $


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_HTML)/nightly

MYLIBS	= nightly_dup_authors.py \
	  nightly_html.py \
	  nightly_lib.py \
	  nightly_os_files.py \
	  nightly_transliterations.py \
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
	  install.py \
	  isbn.py \
	  library.py \
	  navbar.py \
	  viewers.py \
	  login.py \
	  SQLparsing.py \
	  isfdb.py 

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.py:	%.py
		python install_nightly.py $* local /usr/bin/python
local/CurrentBanner:	CurrentBanner
		cp $< local
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
