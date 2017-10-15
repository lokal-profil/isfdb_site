#
#     (C) COPYRIGHT 2005-2006   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.2 $
#     Date: $Date: 2008/04/24 10:30:43 $


import sys
import os
import string

if __name__ == '__main__':

	try:
		basename  = sys.argv[1]
		directory = sys.argv[2]
		python    = sys.argv[3]
	except:
		print "Usage: install.py <basename> <directory> <pythonloc>"
		sys.exit(0)

	fd = open(basename+ '.py')
	image = fd.read()
	fd.close()

	image = string.replace(image, '_PYTHONLOC', python)
	fd = open(directory +'/' +basename+ '.cgi', 'w+')
	fd.write(image)
	fd.close

	os.system('chmod 755 '+directory+ '/' +basename+'.cgi')
	


