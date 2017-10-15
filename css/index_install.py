#
#     (C) COPYRIGHT 2008-2010   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.5 $
#     Date: $Date: 2010/12/04 01:58:53 $

from localdefs import *
import sys
import os
import string

def fillIn(in_filename, out_filename, varname, var):
	fd = open(in_filename)
	image = fd.read()
	fd.close()

	image = string.replace(image, varname, var)
	fd = open(out_filename, 'w+')
	fd.write(image)
	fd.close()
        
if __name__ == '__main__':
        fillIn('index_stub', 'index.html', 'HTMLHOST', HTMLHOST)
        
        fillIn('biblio_css_stub', 'biblio.css', 'HTMLHOST', HTMLHOST)

