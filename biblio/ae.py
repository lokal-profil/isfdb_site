#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2016   Al von Ruff, Ahasuerus & Bill Longley
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import sys
import os
import string
from SQLparsing import *
from biblio import *


if __name__ == '__main__':

	bib = Bibliography()
        bib.page_type = 'Alphabetical'
	bib.displayBiblio()
