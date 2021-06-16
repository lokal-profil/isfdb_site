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


from SQLparsing import *
from common import *


if __name__ == '__main__':

        year = SESSION.Parameter(0, 'int', 0)

	PrintHeader('Votes for Titles with More Than 5 Votes')
	PrintNavbar('stats', 0, 0, 'vstats.cgi', 0)

	print '<ol>'

	if year:
		query = "select titles.title_id,titles.title_title,AVG(votes.rating) from titles,votes where titles.title_id=votes.title_id and YEAR(titles.title_copyright)=%d group by titles.title_title having COUNT(votes.rating)>5 order by AVG(votes.rating) desc" % year
	else:
		query = "select titles.title_id,titles.title_title,AVG(votes.rating) from titles,votes where titles.title_id=votes.title_id group by titles.title_title having COUNT(votes.rating)>5 order by AVG(votes.rating) desc"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		print '<li>%d - %s' % (record[0][2], ISFDBLink('title.cgi', record[0][0], record[0][1]))
		record = result.fetch_row()

	print '</ol>'

	PrintTrailer('stats', 0, 0)
