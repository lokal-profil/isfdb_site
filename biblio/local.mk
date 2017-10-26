#
#     (C) COPYRIGHT 2005-2016   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.12 $
#     Date: $Date: 2016/05/30 19:55:30 $


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)

MYLIBS	= awards.py \
	  biblio.py \
	  common.py \
	  utils.py \
	  isfdblib.py

LIBS	= authorClass.py \
	 awardClass.py \
	 awardcatClass.py \
	 awardtypeClass.py \
	 titleClass.py \
	 pubClass.py \
	 publisherClass.py \
	 pubseriesClass.py \
	 seriesClass.py \
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