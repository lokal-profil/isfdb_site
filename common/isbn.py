#
#     (C) COPYRIGHT 2007-2016   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2016/12/28 17:19:33 $

import string
from library import validISBN, toISBN10, toISBN13


################################################################
# Format an ISBN with hyphen separators.  For information about
# the ranges, see:
#
#     http://www.isbn-international.org/agency?rmxml=1
#     http://www.isbn-international.org/agency?rmpdf=1
#
################################################################
def convertISBN(isbn):

	if validISBN(isbn) == 0:
		return isbn

	isbn13 = 0
	newISBN = string.replace(isbn, '-', '')
	newISBN = string.replace(newISBN, ' ', '')
	prefix = '978'
	if len(newISBN) == 13:
		isbn13 = 1
		prefix = newISBN[0:3]
		newISBN = newISBN[3:13]
	elif len(newISBN) != 10:
		return(isbn)

	# The ISBN is broken into group, publisher, and title numbers, plus a trailing
	# check-digit (always length 1).  Group number lengths vary but are published and
	# known in advance.  Publisher and title number lengths vary and are not known in
	# advance (they depend on what is purchased).  Rules, however, tells us how long
	# the two will be relative to each other, expressed in terms of the length of the
	# publisher group number (NOTE: the title number must always have at least one
	# digit, so maximum publisher length is 7 if a one-digit group code).

	group_len = 0
	publisher_len = 0
	remainder = 0

	if (prefix == '978'):
		group1 = newISBN[0:1]
		remainder = int(newISBN[1:8])
		if (group1 == '0'):
			# English language
			group_len = 1
			if (remainder <= 1999999):
				publisher_len = 2
			elif (remainder <= 6999999):
				publisher_len = 3
			elif (remainder <= 8499999):

				# Two special cases, "groups" 765 and 812.  The length rules say
				# these should be 4-digit publisher numbers, but they are always
				# presented as 3-digit, even though different publishes share the
				# same three digits. For example,
				#
				#    765-3 is Tor
				#    765-6 is M.E. Sharpe
				#    812-3 is Great Source Education Group
				#    812-5 is Tor
				# 2016-06-12 change: Apparently, these special cases reverted to
				# regular rules, i.e. 4-digit publisher numbers, around 2007. This
				# applies to at least Tor and apparrently M.E. Sharpe. We account
				# for it by only using a 3-digit publisher number for ISBN-10s (but
				# not for ISBN-13s.) It's not perfect since some books published by
				# Tor in 2006 had an ISBN-13 but used a 3-digit publisher number.
				#
				if not isbn13 and (((remainder >= 7650000) and (remainder < 7660000))
                                                   or ((remainder >= 8120000) and (remainder < 8130000))):
					publisher_len = 3
				else:
					publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9499999):
				publisher_len = 6
			elif (remainder <= 9999999):
				publisher_len = 7
		elif (group1 == '1'):
			# English language
			group_len = 1
			if (remainder <= 999999):
				publisher_len = 2
			elif (remainder <= 3999999):
				publisher_len = 3
			elif (remainder <= 5499999):
				publisher_len = 4
			elif (remainder <= 8697999):
				publisher_len = 5
			elif (remainder <= 9989999):
				publisher_len = 6
			elif (remainder <= 9999999):
				publisher_len = 7
		elif (group1 == '2'):
			# French language
			group_len = 1
			if (remainder <= 1999999):
				publisher_len = 2
			elif (remainder <= 3499999):
				publisher_len = 3
			elif (remainder <= 3999999):
				publisher_len = 5
			elif (remainder <= 6999999):
				publisher_len = 3
			elif (remainder <= 8399999):
				publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9499999):
				publisher_len = 6
			elif (remainder <= 9999999):
				publisher_len = 7
		elif (group1 == '3'):
			# German language
			group_len = 1
			if (remainder <= 299999):
				publisher_len = 2
			elif (remainder <= 339999):
				publisher_len = 3
			elif (remainder <= 369999):
				publisher_len = 4
			elif (remainder <= 399999):
				publisher_len = 5
			elif (remainder <= 1999999):
				publisher_len = 2
			elif (remainder <= 6999999):
				publisher_len = 3
			elif (remainder <= 8499999):
				publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9499999):
				publisher_len = 6
			elif (remainder <= 9539999):
				publisher_len = 7
			elif (remainder <= 9699999):
				publisher_len = 5
			elif (remainder <= 9899999):
				publisher_len = 7
			elif (remainder <= 9949999):
				publisher_len = 5
			elif (remainder <= 9999999):
				publisher_len = 5
		elif (group1 == '4'):
			# Japan
			group_len = 1
			if (remainder <= 1999999):
				publisher_len = 2
			elif (remainder <= 6999999):
				publisher_len = 3
			elif (remainder <= 8499999):
				publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9499999):
				publisher_len = 6
			elif (remainder <= 9999999):
				publisher_len = 7
		elif (group1 == '5'):
			# Russian Federation and former USSR
			group_len = 1
			if (remainder <= 1999999):
				publisher_len = 2
			elif (remainder <= 4209999):
				publisher_len = 3
			elif (remainder <= 4299999):
				publisher_len = 4
			elif (remainder <= 4309999):
				publisher_len = 3
			elif (remainder <= 4399999):
				publisher_len = 4
			elif (remainder <= 4409999):
				publisher_len = 3
			elif (remainder <= 4499999):
				publisher_len = 4
			elif (remainder <= 6999999):
				publisher_len = 3
			elif (remainder <= 8499999):
				publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9099999):
				publisher_len = 6
			elif (remainder <= 9199999):
				publisher_len = 5
			elif (remainder <= 9299999):
				publisher_len = 4
			elif (remainder <= 9499999):
				publisher_len = 5
			elif (remainder <= 9500999):
				publisher_len = 7
			elif (remainder <= 9799999):
				publisher_len = 4
			elif (remainder <= 9899999):
				publisher_len = 5
			elif (remainder <= 9909999):
				publisher_len = 7
			elif (remainder <= 9999999):
				publisher_len = 4
		elif (group1 == '6'):
			# All group codes starting with 6 are three digits.
			group_len = 3
			group3 = newISBN[0:3]
			remainder = int(newISBN[group_len:8])
			if (group3 == '600'):
				# Iran
				if (remainder <= 9999):
					publisher_len = 2
				elif (remainder <= 49999):
					publisher_len = 3
				elif (remainder <= 89999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '601'):
				# Kazakhstan
				if (remainder <= 19999):
					publisher_len = 2
				elif (remainder <= 69999):
					publisher_len = 3
				elif (remainder <= 79999):
					publisher_len = 4
				elif (remainder <= 84999):
					publisher_len = 5
				elif (remainder <= 99999):
					publisher_len = 2
			elif (group3 == '602'):
				# Indonesia
				if (remainder <= 19999):
					publisher_len = 2
				elif (remainder <= 79999):
					publisher_len = 3
				elif (remainder <= 94999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '603'):
				# Saudi Arabia
				if (remainder <= 4999):
					publisher_len = 2
				elif (remainder <= 49999):
					publisher_len = 2
				elif (remainder <= 79999):
					publisher_len = 3
				elif (remainder <= 89999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '604'):
				# Vietnam
				if (remainder <= 49999):
					publisher_len = 1
				elif (remainder <= 89999):
					publisher_len = 2
				elif (remainder <= 97999):
					publisher_len = 3
				elif (remainder <= 99999):
					publisher_len = 4
			elif (group3 == '605'):
				# Turkey
				if (remainder <= 999):
					publisher_len = 0
				elif (remainder <= 9999):
					publisher_len = 2
				elif (remainder <= 39999):
					publisher_len = 3
				elif (remainder <= 59999):
					publisher_len = 4
				elif (remainder <= 89999):
					publisher_len = 5
				elif (remainder <= 99999):
					publisher_len = 2
			elif (group3 == '606'):
				# Romania
				if (remainder <= 9999):
					publisher_len = 1
				elif (remainder <= 49999):
					publisher_len = 2
				elif (remainder <= 79999):
					publisher_len = 3
				elif (remainder <= 91999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '607'):
				# Mexico
				if (remainder <= 39999):
					publisher_len = 2
				elif (remainder <= 74999):
					publisher_len = 3
				elif (remainder <= 94999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '608'):
				# Macedonia
				if (remainder <= 9999):
					publisher_len = 1
				elif (remainder <= 19999):
					publisher_len = 2
				elif (remainder <= 44999):
					publisher_len = 3
				elif (remainder <= 64999):
					publisher_len = 4
				elif (remainder <= 69999):
					publisher_len = 5
				elif (remainder <= 99999):
					publisher_len = 1
			elif (group3 == '609'):
				# Lithuania
				if (remainder <= 39999):
					publisher_len = 2
				elif (remainder <= 79999):
					publisher_len = 3
				elif (remainder <= 94999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '611'):
				# Thailand
				if (remainder <= 99999):
					publisher_len = 0
			elif (group3 == '612'):
				# Peru
				if (remainder <= 29999):
					publisher_len = 2
				elif (remainder <= 39999):
					publisher_len = 3
				elif (remainder <= 44999):
					publisher_len = 4
				elif (remainder <= 49999):
					publisher_len = 5
				elif (remainder <= 99999):
					publisher_len = 2
			elif (group3 == '613'):
				# Mauritius
				if (remainder <= 99999):
					publisher_len = 0
			elif (group3 == '614'):
				# Lebanon
				if (remainder <= 39999):
					publisher_len = 2
				elif (remainder <= 79999):
					publisher_len = 3
				elif (remainder <= 94999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '615'):
				# Hungary
				if (remainder <= 9999):
					publisher_len = 2
				elif (remainder <= 49999):
					publisher_len = 3
				elif (remainder <= 79999):
					publisher_len = 4
				elif (remainder <= 89999):
					publisher_len = 5
				elif (remainder <= 99999):
					publisher_len = 0
			elif (group3 == '616'):
				# Thailand
				if (remainder <= 19999):
					publisher_len = 2
				elif (remainder <= 69999):
					publisher_len = 3
				elif (remainder <= 89999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
			elif (group3 == '617'):
				# Ukraine
				if (remainder <= 49999):
					publisher_len = 2
				elif (remainder <= 69999):
					publisher_len = 3
				elif (remainder <= 89999):
					publisher_len = 4
				elif (remainder <= 99999):
					publisher_len = 5
		elif (group1 == '7'):
			# China, People's Republic
			group_len = 1
			if (remainder <= 999999):
				publisher_len = 2
			elif (remainder <= 4999999):
				publisher_len = 3
			elif (remainder <= 7999999):
				publisher_len = 4
			elif (remainder <= 8999999):
				publisher_len = 5
			elif (remainder <= 9999999):
				publisher_len = 6
		elif (group1 == '8'):
			# All groups starting with 8 are two digits
			group_len = 2
			group2 = newISBN[0:2]
			remainder = int(newISBN[group_len:8])
			if (group2 == '80'):
				# Czech Republic and Slovakia
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 699999):
					publisher_len = 3
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '81'):
				# India
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 699999):
					publisher_len = 3
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '82'):
				# Norway
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 699999):
					publisher_len = 3
				elif (remainder <= 899999):
					publisher_len = 4
				elif (remainder <= 989999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '83'):
				# Poland
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 599999):
					publisher_len = 3
				elif (remainder <= 699999):
					publisher_len = 5
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '84'):
				# Spain
				if (remainder <= 149999):
					publisher_len = 2
				elif (remainder <= 199999):
					publisher_len = 5
				elif (remainder <= 699999):
					publisher_len = 3
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 919999):
					publisher_len = 4
				elif (remainder <= 923999):
					publisher_len = 6
				elif (remainder <= 929999):
					publisher_len = 5
				elif (remainder <= 949999):
					publisher_len = 6
				elif (remainder <= 969999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 4
			elif (group2 == '85'):
				# Brazil
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 599999):
					publisher_len = 3
				elif (remainder <= 699999):
					publisher_len = 5
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 979999):
					publisher_len = 6
				elif (remainder <= 999999):
					publisher_len = 5
			elif (group2 == '86'):
				# Serbia and Montenegro
				if (remainder <= 299999):
					publisher_len = 2
				elif (remainder <= 599999):
					publisher_len = 3
				elif (remainder <= 799999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '87'):
				# Denmark
				if (remainder <= 299999):
					publisher_len = 2
				elif (remainder <= 399999):
					publisher_len = 0
				elif (remainder <= 649999):
					publisher_len = 3
				elif (remainder <= 699999):
					publisher_len = 0
				elif (remainder <= 799999):
					publisher_len = 4
				elif (remainder <= 849999):
					publisher_len = 0
				elif (remainder <= 949999):
					publisher_len = 5
				elif (remainder <= 969999):
					publisher_len = 0
				elif (remainder <= 999999):
					publisher_len = 6
			elif (group2 == '88'):
				# Italy
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 599999):
					publisher_len = 3
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 899999):
					publisher_len = 5
				elif (remainder <= 949999):
					publisher_len = 6
				elif (remainder <= 999999):
					publisher_len = 5
			elif (group2 == '89'):
				# Korea, Republic
				if (remainder <= 249999):
					publisher_len = 2
				elif (remainder <= 549999):
					publisher_len = 3
				elif (remainder <= 849999):
					publisher_len = 4
				elif (remainder <= 949999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6
		elif (group1 == '9'):

			# Groups starting with 9 have varying lengths.
			#
			#      90 -    94: 2
			#     950 -   989: 3
			#    9900 -  9989: 4
			#   99900 - 99999: 5

			if (int(newISBN[1]) <= 4):
				group_len = 2
				group2 = newISBN[0:2]
				remainder = int(newISBN[group_len:8])
				if (group2 == '90'):
					# Netherlands
					if (remainder <= 199999):
						publisher_len = 2
					elif (remainder <= 499999):
						publisher_len = 3
					elif (remainder <= 699999):
						publisher_len = 4
					elif (remainder <= 799999):
						publisher_len = 5
					elif (remainder <= 849999):
						publisher_len = 6
					elif (remainder <= 899999):
						publisher_len = 4
					elif (remainder <= 909999):
						publisher_len = 2
					elif (remainder <= 939999):
						publisher_len = 6
					elif (remainder <= 949999):
						publisher_len = 2
					elif (remainder <= 999999):
						publisher_len = 6
				elif (group2 == '91'):
					# Sweden
					if (remainder <= 199999):
						publisher_len = 1
					elif (remainder <= 499999):
						publisher_len = 2
					elif (remainder <= 649999):
						publisher_len = 3
					elif (remainder <= 699999):
						publisher_len = 0
					elif (remainder <= 799999):
						publisher_len = 4
					elif (remainder <= 849999):
						publisher_len = 0
					elif (remainder <= 949999):
						publisher_len = 5
					elif (remainder <= 969999):
						publisher_len = 0
					elif (remainder <= 999999):
						publisher_len = 6
				elif (group2 == '92'):
					# International NGO Publishers and EC Organizations
					if (remainder <= 599999):
						publisher_len = 1
					elif (remainder <= 799999):
						publisher_len = 2
					elif (remainder <= 899999):
						publisher_len = 3
					elif (remainder <= 949999):
						publisher_len = 4
					elif (remainder <= 989999):
						publisher_len = 5
					elif (remainder <= 999999):
						publisher_len = 6
				elif (group2 == '93'):
					# India
					if (remainder <= 99999):
						publisher_len = 2
					elif (remainder <= 499999):
						publisher_len = 3
					elif (remainder <= 799999):
						publisher_len = 4
					elif (remainder <= 949999):
						publisher_len = 5
					elif (remainder <= 999999):
						publisher_len = 6
				elif (group2 == '94'):
					# Netherlands
					if (remainder <= 599999):
						publisher_len = 3
					elif (remainder <= 899999):
						publisher_len = 4
					elif (remainder <= 999999):
						publisher_len = 5

			elif (int(newISBN[2]) <= 8):
				group_len = 3
				group3 = newISBN[0:3]
				remainder = int(newISBN[group_len:8])
				if (group3 == '950'):
					# Argentina
					if (remainder <= 49999):
						publisher_len = 2
					elif (remainder <= 89999):
						publisher_len = 3
					elif (remainder <= 98999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '951'):
					# Finland
					if (remainder <= 19999):
						publisher_len = 1
					elif (remainder <= 54999):
						publisher_len = 2
					elif (remainder <= 88999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '952'):
					# Finland
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 49999):
						publisher_len = 3
					elif (remainder <= 59999):
						publisher_len = 4
					elif (remainder <= 65999):
						publisher_len = 2
					elif (remainder <= 66999):
						publisher_len = 4
					elif (remainder <= 69999):
						publisher_len = 5
					elif (remainder <= 79999):
						publisher_len = 4
					elif (remainder <= 94999):
						publisher_len = 2
					elif (remainder <= 98999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '953'):
					# Croatia
					if (remainder <= 9999):
						publisher_len = 1
					elif (remainder <= 14999):
						publisher_len = 2
					elif (remainder <= 54999):
						publisher_len = 3
					elif (remainder <= 59999):
						publisher_len = 5
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '954'):
					# Bulgaria
					if (remainder <= 28999):
						publisher_len = 2
					elif (remainder <= 29999):
						publisher_len = 4
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 92999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '955'):
					# Sri Lanka
					if (remainder <= 19999):
						publisher_len = 4
					elif (remainder <= 54999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '956'):
					# Chile
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '957'):
					# Taiwan
					if (remainder <= 2999):
						publisher_len = 2
					elif (remainder <= 4999):
						publisher_len = 4
					elif (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 20999):
						publisher_len = 4
					elif (remainder <= 27999):
						publisher_len = 2
					elif (remainder <= 30999):
						publisher_len = 5
					elif (remainder <= 43999):
						publisher_len = 2
					elif (remainder <= 81999):
						publisher_len = 3
					elif (remainder <= 96999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '958'):
					# Colombia
					if (remainder <= 56999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 5
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '959'):
					# Cuba
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '960'):
					# Greece
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 65999):
						publisher_len = 3
					elif (remainder <= 68999):
						publisher_len = 4
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 92999):
						publisher_len = 5
					elif (remainder <= 93999):
						publisher_len = 2
					elif (remainder <= 97999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '961'):
					# Slovenia
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 94999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 0
				elif (group3 == '962'):
					# Hong Kong, China
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 86999):
						publisher_len = 5
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 3
				elif (group3 == '963'):
					# Hungary
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 89999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '964'):
					# Iran
					if (remainder <= 14999):
						publisher_len = 2
					elif (remainder <= 24999):
						publisher_len = 3
					elif (remainder <= 29999):
						publisher_len = 4
					elif (remainder <= 54999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 96999):
						publisher_len = 5
					elif (remainder <= 98999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '965'):
					# Israel
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 3
					elif (remainder <= 69999):
						publisher_len = 0
					elif (remainder <= 79999):
						publisher_len = 4
					elif (remainder <= 89999):
						publisher_len = 0
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '966'):
					# Ukraine
					if (remainder <= 14999):
						publisher_len = 2
					elif (remainder <= 16999):
						publisher_len = 4
					elif (remainder <= 19999):
						publisher_len = 3
					elif (remainder <= 29999):
						publisher_len = 4
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '967'):
					# Malaysia
					if (remainder <= 29999):
						publisher_len = 2
					elif (remainder <= 49999):
						publisher_len = 3
					elif (remainder <= 59999):
						publisher_len = 4
					elif (remainder <= 89999):
						publisher_len = 2
					elif (remainder <= 98999):
						publisher_len = 3
					elif (remainder <= 99899):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '968'):
					# Mexico
					if (remainder <= 39999):
						publisher_len = 2
					elif (remainder <= 49999):
						publisher_len = 3
					elif (remainder <= 79999):
						publisher_len = 4
					elif (remainder <= 89999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '969'):
					# Pakistan
					if (remainder <= 19999):
						publisher_len = 1
					elif (remainder <= 39999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '970'):
					# Mexico
					if (remainder <= 59999):
						publisher_len = 2
					elif (remainder <= 89999):
						publisher_len = 3
					elif (remainder <= 90999):
						publisher_len = 4
					elif (remainder <= 96999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '971'):
					# Philippines
					if (remainder <= 1599):
						publisher_len = 3
					elif (remainder <= 1999):
						publisher_len = 4
					elif (remainder <= 2999):
						publisher_len = 2
					elif (remainder <= 5999):
						publisher_len = 4
					elif (remainder <= 9999):
						publisher_len = 2
					elif (remainder <= 49999):
						publisher_len = 2
					elif (remainder <= 84999):
						publisher_len = 3
					elif (remainder <= 90999):
						publisher_len = 4
					elif (remainder <= 98999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '972'):
					# Portugal
					if (remainder <= 19999):
						publisher_len = 1
					elif (remainder <= 54999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '973'):
					# Romania
					if (remainder <= 9999):
						publisher_len = 1
					elif (remainder <= 16999):
						publisher_len = 3
					elif (remainder <= 19999):
						publisher_len = 4
					elif (remainder <= 54999):
						publisher_len = 2
					elif (remainder <= 75999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 88999):
						publisher_len = 5
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '974'):
					# Thailand
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 84999):
						publisher_len = 4
					elif (remainder <= 89999):
						publisher_len = 5
					elif (remainder <= 94999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '975'):
					# Turkey
					if (remainder <= 999):
						publisher_len = 5
					elif (remainder <= 1999):
						publisher_len = 2
					elif (remainder <= 24999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 3
					elif (remainder <= 91999):
						publisher_len = 4
					elif (remainder <= 98999):
						publisher_len = 5
					elif (remainder <= 99999):
						publisher_len = 3
				elif (group3 == '976'):
					# Caribbean Community
					if (remainder <= 39999):
						publisher_len = 1
					elif (remainder <= 59999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '977'):
					# Egypt
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 49999):
						publisher_len = 3
					elif (remainder <= 69999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 3
				elif (group3 == '978'):
					# Nigeria
					if (remainder <= 19999):
						publisher_len = 3
					elif (remainder <= 29999):
						publisher_len = 4
					elif (remainder <= 79999):
						publisher_len = 5
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 3
				elif (group3 == '979'):
					# Indonesia
					if (remainder <= 9999):
						publisher_len = 3
					elif (remainder <= 14999):
						publisher_len = 4
					elif (remainder <= 19999):
						publisher_len = 5
					elif (remainder <= 29999):
						publisher_len = 2
					elif (remainder <= 39999):
						publisher_len = 4
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '980'):
					# Venezuela
					if (remainder <= 19999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '981'):
					# Singapore
					if (remainder <= 11999):
						publisher_len = 2
					elif (remainder <= 19999):
						publisher_len = 4
					elif (remainder <= 28999):
						publisher_len = 3
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '982'):
					# South Pacific
					if (remainder <= 9999):
						publisher_len = 2
					elif (remainder <= 69999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 2
					elif (remainder <= 99999):
						publisher_len = 4
				elif (group3 == '983'):
					# Malaysia
					if (remainder <= 1999):
						publisher_len = 2
					elif (remainder <= 19999):
						publisher_len = 3
					elif (remainder <= 39999):
						publisher_len = 4
					elif (remainder <= 44999):
						publisher_len = 5
					elif (remainder <= 49999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 2
					elif (remainder <= 89999):
						publisher_len = 3
					elif (remainder <= 98999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '984'):
					# Bangladesh
					if (remainder <= 39999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '985'):
					# Belarus
					if (remainder <= 39999):
						publisher_len = 2
					elif (remainder <= 59999):
						publisher_len = 3
					elif (remainder <= 89999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '986'):
					# Taiwan
					if (remainder <= 11999):
						publisher_len = 2
					elif (remainder <= 55999):
						publisher_len = 3
					elif (remainder <= 79999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '987'):
					# Argentina
					if (remainder <= 9999):
						publisher_len = 2
					elif (remainder <= 19999):
						publisher_len = 4
					elif (remainder <= 29999):
						publisher_len = 5
					elif (remainder <= 49999):
						publisher_len = 2
					elif (remainder <= 89999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '988'):
					# Hong Kong, China
					if (remainder <= 16999):
						publisher_len = 2
					elif (remainder <= 19999):
						publisher_len = 5
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 96999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5
				elif (group3 == '989'):
					# Portugal
					if (remainder <= 19999):
						publisher_len = 1
					elif (remainder <= 54999):
						publisher_len = 2
					elif (remainder <= 79999):
						publisher_len = 3
					elif (remainder <= 94999):
						publisher_len = 4
					elif (remainder <= 99999):
						publisher_len = 5

			elif (int(newISBN[3]) <= 8):
				group_len = 4
				group4 = newISBN[0:4]
				remainder = int(newISBN[group_len:8])
				# Note: As of 25-APR-2010, no groups 9900 - 9927
				if (group4 == '9928'):
					# Albania
					if (remainder <= 999):
						publisher_len = 2
					elif (remainder <= 3999):
						publisher_len = 3
					elif (remainder <= 4999):
						publisher_len = 4
					elif (remainder <= 9999):
						publisher_len = 0
				elif (group4 == '9929'):
					# Guatemala
					if (remainder <= 3999):
						publisher_len = 1
					elif (remainder <= 5499):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9930'):
					# Costa Rica
					if (remainder <= 4999):
						publisher_len = 2
					elif (remainder <= 9399):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9931'):
					# Algeria
					if (remainder <= 2999):
						publisher_len = 1
					elif (remainder <= 5999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9932'):
					# Lao People's Democratic Republic
					if (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9933'):
					# Syria
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9934'):
					# Latvia
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 4999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9935'):
					# Iceland
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9936'):
					# Afghanistan
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9937'):
					# Nepal
					if (remainder <= 2999):
						publisher_len = 1
					elif (remainder <= 4999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9938'):
					# Tunisia
					if (remainder <= 7999):
						publisher_len = 2
					elif (remainder <= 9499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9939'):
					# Armenia
					if (remainder <= 4999):
						publisher_len = 1
					elif (remainder <= 7999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9940'):
					# Montenegro
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 4999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9941'):
					# Georgia
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9942'):
					# Ecuador
					if (remainder <= 8999):
						publisher_len = 2
					elif (remainder <= 9949):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9943'):
					# Uzbekistan
					if (remainder <= 2999):
						publisher_len = 2
					elif (remainder <= 3999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9944'):
					# Turkey
					if (remainder <= 999):
						publisher_len = 4
					elif (remainder <= 4999):
						publisher_len = 3
					elif (remainder <= 5999):
						publisher_len = 4
					elif (remainder <= 6999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 8999):
						publisher_len = 2
					elif (remainder <= 9999):
						publisher_len = 3
				elif (group4 == '9945'):
					# Dominican Republic
					if (remainder <= 99):
						publisher_len = 2
					elif (remainder <= 799):
						publisher_len = 3
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 5699):
						publisher_len = 3
					elif (remainder <= 5799):
						publisher_len = 2
					elif (remainder <= 8499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9946'):
					# Korea, P.D.R.
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9947'):
					# Algeria
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 7999):
						publisher_len = 2
					elif (remainder <= 9999):
						publisher_len = 3
				elif (group4 == '9948'):
					# United Arab Emirates
					if (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9949'):
					# Estonia
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9950'):
					# Palestine
					if (remainder <= 2999):
						publisher_len = 2
					elif (remainder <= 8499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9951'):
					# Kosova
					if (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 8499):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9952'):
					# Azerbaijan
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9953'):
					# Lebanon
					if (remainder <= 999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 5999):
						publisher_len = 3
					elif (remainder <= 8999):
						publisher_len = 2
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9954'):
					# Morocco
					if (remainder <= 1999):
						publisher_len = 1
					elif (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 7999):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9955'):
					# Lithuania
					if (remainder <= 3999):
						publisher_len = 2
					elif (remainder <= 9299):
						publisher_len = 3
					elif (remainder <= 9999):
						publisher_len = 4
				elif (group4 == '9956'): 
					# Cameroon 
					if (remainder <= 999): 
						publisher_len = 1 
					elif (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9957'): 
					# Jordan 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 6999): 
						publisher_len = 3 
					elif (remainder <= 8499): 
						publisher_len = 2 
					elif (remainder <= 8799): 
						publisher_len = 4 
					elif (remainder <= 9999): 
						publisher_len = 2 
				elif (group4 == '9958'): 
					# Bosnia and Herzegovina 
					if (remainder <= 999): 
						publisher_len = 1 
					elif (remainder <= 4999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9959'): 
					# Libya 
					if (remainder <= 1999): 
						publisher_len = 1 
					elif (remainder <= 7999): 
						publisher_len = 2 
					elif (remainder <= 9499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9960'): 
					# Saudi Arabia 
					if (remainder <= 5999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9961'): 
					# Algeria 
					if (remainder <= 2999): 
						publisher_len = 1 
					elif (remainder <= 6999): 
						publisher_len = 2 
					elif (remainder <= 9499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9962'): 
					# Panama 
					if (remainder <= 5499): 
						publisher_len = 2 
					elif (remainder <= 5599): 
						publisher_len = 4 
					elif (remainder <= 5999): 
						publisher_len = 2 
					elif (remainder <= 8499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9963'): 
					# Cyprus 
					if (remainder <= 2999): 
						publisher_len = 1 
					elif (remainder <= 5499): 
						publisher_len = 2 
					elif (remainder <= 7499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9964'): 
					# Ghana 
					if (remainder <= 6999): 
						publisher_len = 1 
					elif (remainder <= 9499): 
						publisher_len = 2 
					elif (remainder <= 9999): 
						publisher_len = 3 
				elif (group4 == '9965'): 
					# Kazakhstan 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9966'): 
					# Kenya 
					if (remainder <= 1999): 
						publisher_len = 3 
					elif (remainder <= 6999): 
						publisher_len = 2 
					elif (remainder <= 7499): 
						publisher_len = 4 
					elif (remainder <= 9599): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9967'): 
					# Kyrgyz Republic 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9968'): 
					# Costa Rica 
					if (remainder <= 4999): 
						publisher_len = 2 
					elif (remainder <= 9399): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9970'): 
					# Uganda 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9971'): 
					# Singapore 
					if (remainder <= 5999): 
						publisher_len = 1 
					elif (remainder <= 8999): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9972'): 
					# Peru 
					if (remainder <= 999): 
						publisher_len = 2 
					elif (remainder <= 1999): 
						publisher_len = 1 
					elif (remainder <= 2499): 
						publisher_len = 3 
					elif (remainder <= 2999): 
						publisher_len = 4 
					elif (remainder <= 5999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9973'): 
					# Tunisia 
					if (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 899): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 4 
					elif (remainder <= 6999): 
						publisher_len = 2 
					elif (remainder <= 9699): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9974'): 
					# Uruguay 
					if (remainder <= 2999): 
						publisher_len = 1 
					elif (remainder <= 5499): 
						publisher_len = 2 
					elif (remainder <= 7499): 
						publisher_len = 3 
					elif (remainder <= 9499): 
						publisher_len = 4 
					elif (remainder <= 9999): 
						publisher_len = 2 
				elif (group4 == '9975'): 
					# Moldova 
					if (remainder <= 999): 
						publisher_len = 1 
					elif (remainder <= 3999): 
						publisher_len = 3 
					elif (remainder <= 4499): 
						publisher_len = 4 
					elif (remainder <= 8999): 
						publisher_len = 2 
					elif (remainder <= 9499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9976'): 
					# Tanzania 
					if (remainder <= 5999): 
						publisher_len = 1 
					elif (remainder <= 8999): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9977'): 
					# Costa Rica 
					if (remainder <= 8999): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9978'): 
					# Ecuador 
					if (remainder <= 2999): 
						publisher_len = 2 
					elif (remainder <= 3999): 
						publisher_len = 3 
					elif (remainder <= 9499): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9979'): 
					# Iceland 
					if (remainder <= 4999): 
						publisher_len = 1 
					elif (remainder <= 6499): 
						publisher_len = 2 
					elif (remainder <= 6599): 
						publisher_len = 3 
					elif (remainder <= 7599): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9980'): 
					# Papua New Guinea 
					if (remainder <= 3999): 
						publisher_len = 1 
					elif (remainder <= 8999): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9981'): 
					# Morocco 
					if (remainder <= 999): 
						publisher_len = 2 
					elif (remainder <= 1599): 
						publisher_len = 3 
					elif (remainder <= 1999): 
						publisher_len = 4 
					elif (remainder <= 7999): 
						publisher_len = 2 
					elif (remainder <= 9499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9982'): 
					# Zambia 
					if (remainder <= 7999): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9983'): 
					# Gambia 
					if (remainder <= 7999): 
						publisher_len = 0 
					elif (remainder <= 9499): 
						publisher_len = 2 
					elif (remainder <= 9899): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9984'): 
					# Latvia 
					if (remainder <= 4999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9985'): 
					# Estonia 
					if (remainder <= 4999): 
						publisher_len = 1 
					elif (remainder <= 7999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9986'): 
					# Lithuania 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8999): 
						publisher_len = 3 
					elif (remainder <= 9399): 
						publisher_len = 4 
					elif (remainder <= 9699): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 2 
				elif (group4 == '9987'): 
					# Tanzania 
					if (remainder <= 3999): 
						publisher_len = 2 
					elif (remainder <= 8799): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9988'): 
					# Ghana 
					if (remainder <= 2999): 
						publisher_len = 1 
					elif (remainder <= 5499): 
						publisher_len = 2 
					elif (remainder <= 7499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 
				elif (group4 == '9989'): 
					# Macedonia 
					if (remainder <= 999): 
						publisher_len = 1 
					elif (remainder <= 1999): 
						publisher_len = 3 
					elif (remainder <= 2999): 
						publisher_len = 4 
					elif (remainder <= 5999): 
						publisher_len = 2 
					elif (remainder <= 9499): 
						publisher_len = 3 
					elif (remainder <= 9999): 
						publisher_len = 4 


			elif (int(newISBN[4]) <= 8):
				group_len = 5
				group5 = newISBN[0:5]
				remainder = int(newISBN[group_len:8])
				if (group5 == '99901'): 
					# Bahrain 
					if (remainder <= 499): 
						publisher_len = 2 
					elif (remainder <= 799): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99902'): 
					# Gabon 
					if (remainder <= 999): 
						publisher_len = 0 
				elif (group5 == '99903'): 
					# Mauritius 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99904'): 
					# Netherlands Antilles and Aruba 
					if (remainder <= 599): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99905'): 
					# Bolivia 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99906'): 
					# Kuwait 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 699): 
						publisher_len = 3 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 1 
				elif (group5 == '99908'): 
					# Malawi 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99909'): 
					# Malta 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 949): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99910'): 
					# Sierra Leone 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99911'): 
					# Lesotho 
					if (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99912'): 
					# Botswana 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 3 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99913'): 
					# Andorra 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 359): 
						publisher_len = 2 
					elif (remainder <= 599): 
						publisher_len = 0 
					elif (remainder <= 604): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 0 
				elif (group5 == '99914'): 
					# Suriname 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99915'): 
					# Maldives 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99916'): 
					# Namibia 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99917'): 
					# Brunei Darussalam 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99918'): 
					# Faroe Islands 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99919'): 
					# Benin 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 399): 
						publisher_len = 3 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 899): 
						publisher_len = 0 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99920'): 
					# Andorra 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99921'): 
					# Qatar 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 799): 
						publisher_len = 3 
					elif (remainder <= 899): 
						publisher_len = 1 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99922'): 
					# Guatemala 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99923'): 
					# El Salvador 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99924'): 
					# Nicaragua 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99925'): 
					# Paraguay 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99926'): 
					# Honduras 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99927'): 
					# Albania 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99928'): 
					# Georgia 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99929'): 
					# Mongolia 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99930'): 
					# Armenia 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99931'): 
					# Seychelles 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99932'): 
					# Malta 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 699): 
						publisher_len = 3 
					elif (remainder <= 799): 
						publisher_len = 1 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99933'): 
					# Nepal 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99934'): 
					# Dominican Republic 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99935'): 
					# Haiti 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 699): 
						publisher_len = 3 
					elif (remainder <= 899): 
						publisher_len = 1 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99936'): 
					# Bhutan 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99937'): 
					# Macau 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99938'): 
					# Srpska, Republic of 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 899): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99939'): 
					# Guatemala 
					if (remainder <= 599): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99940'): 
					# Georgia 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99941'): 
					# Armenia 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99942'): 
					# Sudan 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99943'): 
					# Albania 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99944'): 
					# Ethiopia 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99945'): 
					# Namibia 
					if (remainder <= 599): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99946'): 
					# Nepal 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99947'): 
					# Tajikistan 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99948'): 
					# Eritrea 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99949'): 
					# Mauritius 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99950'): 
					# Cambodia 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99951'): 
					# Congo 
					if (remainder <= 999): 
						publisher_len = 0 
				elif (group5 == '99952'): 
					# Mali 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99953'): 
					# Paraguay 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 939): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99954'): 
					# Bolivia 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 699): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99955'): 
					# Srpska, Republic of 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 899): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99956'): 
					# Albania 
					if (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 859): 
						publisher_len = 3 
					elif (remainder <= 999): 
						publisher_len = 2 
				elif (group5 == '99957'): 
					# Malta 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99958'): 
					# Bahrain 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 949): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99959'): 
					# Luxembourg 
					if (remainder <= 299): 
						publisher_len = 1 
					elif (remainder <= 599): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99960'): 
					# Malawi 
					if (remainder <= 99): 
						publisher_len = 1 
					elif (remainder <= 949): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99961'): 
					# El Salvador 
					if (remainder <= 399): 
						publisher_len = 1 
					elif (remainder <= 899): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99962'): 
					# Mongolia 
					if (remainder <= 499): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99963'): 
					# Cambodia 
					if (remainder <= 499): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
				elif (group5 == '99964'): 
					# Nicaragua 
					if (remainder <= 199): 
						publisher_len = 1 
					elif (remainder <= 799): 
						publisher_len = 2 
					elif (remainder <= 999): 
						publisher_len = 3 
	elif (prefix == '979'):
		# NORMAL CASES
		group1 = newISBN[0]

		# Only valid group as of 25-APR-2010 is 10.
		if (group1 == '1'):
			group2 = newISBN[0:2]
			group_len = 2
			remainder = int(newISBN[group_len:8])
			if (group2 == '10'):
				# France
				if (remainder <= 199999):
					publisher_len = 2
				elif (remainder <= 699999):
					publisher_len = 3
				elif (remainder <= 899999):
					publisher_len = 4
				elif (remainder <= 975999):
					publisher_len = 5
				elif (remainder <= 999999):
					publisher_len = 6

	# Format the string based on what we determined above.
	if (group_len == 0):
		# No group.  Just add one hyphen before the checksum digit.
		retval = "%s-%s" % (newISBN[0:9], newISBN[9])
	elif (publisher_len == 0):
		# No publisher.  Add one hyphen after the group and one hyphen before the checksum.
		retval = "%s-%s-%s" % (newISBN[0:group_len], newISBN[group_len:9], newISBN[9])
	else:
		# We have all parts.  Add one hypen after the group, one after the publisher,
		# and one before the checksum
		retval = "%s-%s-%s-%s" % (newISBN[0:group_len], newISBN[group_len:group_len+publisher_len], newISBN[group_len+publisher_len:9], newISBN[9])

	# If we're handling an ISBN-13, restore the prefix.
	if isbn13:
		retval = prefix + '-' + retval

	return retval

def isbnVariations(original):
        ######################################################################
        # Given a candidate ISBN, builds an array of
        # possible legitimate variations:
        # - Always check for the candidate as it was supplied
        # - If the passed in candidate was a valid ISBN, then also search for:
        #   - The hyphenated forms of the ISBN-10 and the ISBN-13
        #   - The unhyphenated forms of the ISBN-10 and the ISBN-13
        ######################################################################
	variations = []
	# Always original
	variations.append(original)
	if validISBN(original):
		collapsedOrig = string.replace(original, '-', '')
		collapsedOrig = string.replace(collapsedOrig, ' ', '')
		origLen = len(original)
		collapsedLen = len(collapsedOrig);
		if collapsedLen == origLen:
			# original not punctuated, add punctuated
			variations.append(convertISBN(original))
		else:
			# original punctuated, add unpunctuated
			variations.append(collapsedOrig)
		if collapsedLen == 10:
			# ISBN-10; need ISBN-13
			otherISBN = toISBN13(collapsedOrig)
		else:
			# ISBN-13; need ISBN-10
			otherISBN = toISBN10(collapsedOrig)
		variations.append(otherISBN)
		variations.append(convertISBN(otherISBN))
	return variations
