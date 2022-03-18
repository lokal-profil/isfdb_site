#
#     (C) COPYRIGHT 2008-2021   Al von Ruff, Ahasuerus and Klaus Elsbernd
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from localdefs import *
import sys
import os
import string

def fillIn(in_filename, out_filename, replacement_dictionary):
	fd = open(in_filename)
	image = fd.read()
	fd.close()

        for key in replacement_dictionary:
                image = string.replace(image, key, replacement_dictionary[key])
	fd = open(out_filename, 'w+')
	fd.write(image)
	fd.close()
        
if __name__ == '__main__':
        replacement_dictionary = {'HTMLHOST': HTMLHOST,
                                  'PROTOCOL': PROTOCOL}

        fillIn('index_stub', 'index.html', replacement_dictionary)
        fillIn('biblio_css_stub', 'biblio.css', replacement_dictionary)
