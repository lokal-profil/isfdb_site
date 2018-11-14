#!_PYTHONLOC
#
#     (C) COPYRIGHT 2017-2018   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$


import cgi
import sys
import string
import os
from isfdb import *
from SQLparsing import *
from common import *
from biblio import *
from library import ServerSideRedirect

class ExtIDSearch:
        def __init__(self):
                self.operator = ''
                self.operators = ('exact', 'contains', 'notcontains', 'starts_with', 'not_starts_with', 'ends_with', 'not_ends_with')
                self.pubs = []
                self.clause = ''
                self.id_value = ''
                self.id_type = 0

        def get_search_parameters(self):
                form = cgi.FieldStorage()
                try:
                        id_types = SQLLoadIdentifierTypes()
                        self.id_type = int(form['ID_TYPE'].value)
                        if self.id_type not in id_types:
                                raise
                except:
                        self.display_error('Invalid External ID Type')

                try:
                        self.id_value = form['ID_VALUE'].value
                        self.id_value = string.strip(self.id_value)
                except:
                        self.display_error('No search value specified')

                try:
                        self.operator = form['OPERATOR'].value
                        if self.operator not in self.operators:
                                raise
                except:
                        self.display_error('Invalid operator specified')

        def display_error(self, message):
                self.print_headers()
                print '<h2>%s</h2>' % message
                PrintTrailer('search', '', 0)
                sys.exit(0)

        def build_query_clause(self):
                escaped_value = db.escape_string(self.id_value)
                if self.operator == 'exact':
                        self.clause = "like '%s'" % escaped_value
                elif self.operator == 'contains':
                        self.clause = "like '%%%s%%'" % escaped_value
                elif self.operator == 'contains':
                        self.clause = "not like '%%%s%%'" % escaped_value
                elif self.operator == 'starts_with':
                        self.clause = "like '%s%%'" % escaped_value
                elif self.operator == 'not_starts_with':
                        self.clause = "not like '%s%%'" % escaped_value
                elif self.operator == 'ends_with':
                        self.clause = "like '%%%s'" % escaped_value
                elif self.operator == 'not_ends_with':
                        self.clause = "not like '%%%s'" % escaped_value

        def get_pubs(self):
                query = """select p.*
                        from (
                        select distinct pub_id from identifiers
                        where identifier_type_id = %d
                        and identifier_value %s
                        limit 300
                        ) as xx, pubs p
                        where p.pub_id = xx.pub_id
                        order by p.pub_title""" % (self.id_type, self.clause)
                db.query(query)
                result = db.store_result()
                self.num = result.num_rows()
                record = result.fetch_row()
                while record:
                        pub_data = record[0]
                        self.pubs.append(pub_data)
                        record = result.fetch_row()

        def print_headers(self):
                PrintHeader("ISFDB Publication Search by External ID")
                PrintNavbar('search', 0, 0, 0, 0)
                
        def print_pubs(self):
                matches = len(self.pubs)
                if matches == 1:
                        ServerSideRedirect('http:/%s/pl.cgi?%d' % (HTFAKE, self.pubs[0][PUB_PUBID]))
                self.print_headers()
                if not matches:
                        print '<h2>No matching records found.</h2>'
                        return
                print '<p><h3>%d matches found.' % matches
                print 'Publication Search by External ID is currently limited to the first 300 publication matches.</h3>'
                PrintPubsTable(self.pubs, 'adv_search')

if __name__ == '__main__':


        search = ExtIDSearch()
        search.get_search_parameters()
        search.build_query_clause()
        search.get_pubs()
        search.print_pubs()

	print '<p>'
	PrintTrailer('search', 0, 0)

