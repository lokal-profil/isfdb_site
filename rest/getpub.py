#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2018   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

import sys
import string
from isfdb import *
from isbn import *
from SQLparsing import *
from pub_output import pubOutput


if __name__ == '__main__':

	print 'Content-type: text/html\n'

	try:
                isbns = isbnVariations(sys.argv[1])
                if not isbns:
                        raise
	except:
		print "getpub.cgi: Bad ISBN"
		sys.exit(1)

        pub_bodies = SQLFindPubsByIsbn(isbns)
        pubOutput(pub_bodies)
