#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2021   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from isbn import *
from SQLparsing import *
from pub_output import pubOutput


if __name__ == '__main__':

	print 'Content-type: text/html\n'

        isbns = isbnVariations(SESSION.Parameter(0, 'str'))
        if not isbns:
		print "getpub.cgi: Bad ISBN"
		sys.exit(1)

        pub_bodies = SQLFindPubsByIsbn(isbns)
        pubOutput(pub_bodies)
