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

	query = """select YEAR(NOW())-YEAR(author_birthdate) as age,
                   author_canonical, author_birthdate, author_id from authors
                   where author_birthdate is not null
                   and author_birthdate !='0000-00-00'
                   and author_deathdate is null
                   and YEAR(NOW())-YEAR(author_birthdate) > 79
                   and YEAR(NOW())-YEAR(author_birthdate) < 117
                   order by author_birthdate"""
        headers = ('Age', 'Date of Birth', 'Author')
        note = """The following list includes authors whose year of birth
                  is between 80 and 116 years in the past and who do not
                  have a year of death on file"""

        PrintListPage('ISFDB Oldest Living Authors',
                      'oldest', 0, 0, 'oldest.cgi', 0,
                      query, AuthorsDisplayFunc, headers, note)
