#
#     (C) COPYRIGHT 2005-2017   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.7 $
#     Date: $Date: 2017/07/23 00:11:35 $

include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)/rest

LIBS = login.py \
	SQLparsing.py \
	isbn.py \
	isfdb.py \
	library.py \
	navbar.py \
	install.py \
	pubClass.py \
	isfdblib.py

all:	$(TARGETS)
	cp $(LIBS) local

local/%.cgi:	%.py
		python install.py $* local /usr/bin/python

check_dirs:
		if test -d $(INSTALL); \
		then echo $(INSTALL) exists; \
		else mkdir $(INSTALL); \
		fi

install:	all check_dirs
		cp local/* $(INSTALL)
		chmod 755 $(INSTALL)/*.cgi
		chmod 644 $(INSTALL)/*.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local
