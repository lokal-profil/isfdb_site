#
#     (C) COPYRIGHT 2005-2013   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2013/12/16 03:09:06 $

install:
	cd common && $(MAKE) install;
	cd biblio && $(MAKE) LOCAL;
	cd biblio && $(MAKE) install;
	cd edit   && $(MAKE) LOCAL;
	cd edit   && $(MAKE) install;
	cd mod    && $(MAKE) LOCAL;
	cd mod    && $(MAKE) install;
	cd nightly && $(MAKE) LOCAL;
	cd nightly && $(MAKE) install;
	cd css    && $(MAKE) install;
	cd rest   && $(MAKE) LOCAL;
	cd rest   && $(MAKE) install;
clean:
	cd common && $(MAKE) clean;
	cd biblio && $(MAKE) clean;
	cd edit && $(MAKE) clean;
	cd mod && $(MAKE) clean;
	cd css && $(MAKE) clean;
	cd rest && $(MAKE) clean;
export:
		/bin/bash export.sh

