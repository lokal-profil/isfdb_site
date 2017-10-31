#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2016   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


from common import *

if __name__ == '__main__':
        query = """select YEAR(author_deathdate)-YEAR(author_birthdate) as age,
                   author_canonical, author_birthdate, author_id from authors
                   where author_birthdate is not null
                   and YEAR(author_birthdate) != '0000'
                   and author_deathdate is not null
                   and YEAR(author_deathdate) != '0000'
                   and YEAR(author_deathdate)-YEAR(author_birthdate) < 40
                   and YEAR(author_deathdate)-YEAR(author_birthdate) > 0
                   order by YEAR(author_deathdate)-YEAR(author_birthdate)"""
        headers = ('Age', 'Date of Birth', 'Author')
        
        PrintListPage('ISFDB Youngest Non-Living Authors',
                      'youngest_nl', 0, 0, 'youngest_nl.cgi', 0,
                      query, AuthorsDisplayFunc, headers)
