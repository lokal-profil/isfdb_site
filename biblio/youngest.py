#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2013   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *

if __name__ == '__main__':
	query = "select YEAR(NOW())-YEAR(author_birthdate) as age, author_canonical, author_birthdate, "
	query += "author_id from authors where author_birthdate is not null and author_deathdate is null "
	query += "and YEAR(NOW())-YEAR(author_birthdate) < 40 order by author_birthdate desc"
        headers = ('Age', 'Date of Birth', 'Author')
        
        PrintListPage('ISFDB Youngest Living Authors',
                      'youngest', 0, 0, 'youngest.cgi', 0,
                      query, AuthorsDisplayFunc, headers)
