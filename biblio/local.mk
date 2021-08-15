#
#     (C) COPYRIGHT 2005-2021   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)

MYLIBS	= advSearchClass.py \
	  biblio.py \
	  calendarClass.py \
	  common.py \
	  isfdblib.py \
	  utils.py

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
	 login.py \
	 SQLparsing.py \
	 isbn.py \
	 isfdb.py \
	 library.py \
	 navbar.py \
	 install.py \
	 viewers.py

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.cgi:	%.py
		python install.py $* local /usr/bin/python

install:	all
		rm -f $(INSTALL)/*.pyc
		cp local/* $(INSTALL)
		chmod 755 $(INSTALL)/*.cgi
		chmod 644 $(INSTALL)/*.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local
