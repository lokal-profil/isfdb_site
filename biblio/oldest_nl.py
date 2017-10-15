#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2013   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.6 $
#     Date: $Date: 2013/12/20 18:04:48 $


from common import *

if __name__ == '__main__':

	query = "select YEAR(author_deathdate)-YEAR(author_birthdate) as age, author_canonical, author_birthdate, "
	query += "author_id from authors where author_birthdate is not null and author_deathdate is not null "
	query += "and author_birthdate != '0000-00-00' and author_deathdate !='0000-00-00' "
	query += "and YEAR(author_deathdate)-YEAR(author_birthdate) > 79 "
	query += "order by YEAR(author_deathdate)-YEAR(author_birthdate) desc"
        headers = ('Age', 'Date of Birth', 'Author')

        PrintListPage('ISFDB Oldest Non-Living Authors',
                      'oldest_nl', 0, 0, 'oldest_nl.cgi', 0,
                      query, AuthorsDisplayFunc, headers)
