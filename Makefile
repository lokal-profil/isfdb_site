#
#     (C) COPYRIGHT 2005-2013   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

install:
	cd isfdb/common && $(MAKE) install;
	cd isfdb/biblio && $(MAKE) LOCAL;
	cd isfdb/biblio && $(MAKE) install;
	cd isfdb/edit   && $(MAKE) LOCAL;
	cd isfdb/edit   && $(MAKE) install;
	cd isfdb/mod    && $(MAKE) LOCAL;
	cd isfdb/mod    && $(MAKE) install;
	cd isfdb/nightly && $(MAKE) LOCAL;
	cd isfdb/nightly && $(MAKE) install;
	cd isfdb/css    && $(MAKE) install;
	cd isfdb/rest   && $(MAKE) LOCAL;
	cd isfdb/rest   && $(MAKE) install;
clean:
	cd isfdb/common && $(MAKE) clean;
	cd isfdb/biblio && $(MAKE) clean;
	cd isfdb/edit && $(MAKE) clean;
	cd isfdb/mod && $(MAKE) clean;
	cd isfdb/css && $(MAKE) clean;
	cd isfdb/rest && $(MAKE) clean;
export:
		/bin/bash export.sh

