#!_PYTHONLOC
#
#     (C) COPYRIGHT 2018   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $


import cgi
import sys
import string
import os
from isfdb import *
from library import AutoVivification, ISFDBLink
from SQLparsing import *
from common import *

class WebPagesSearch:
        def __init__(self):
                self.operator = ''
                self.operators = ('exact', 'contains', 'starts_with', 'ends_with')
                self.clause = ''
                self.records = AutoVivification()
                self.webpages = AutoVivification()
                self.record_types = {
                        'Authors': ('author_id', 'author_canonical', 'ea', 'authors'),
                        'Titles': ('title_id', 'title_title', 'title', 'titles'),
                        'Series': ('series_id', 'series_title', 'pe', 'series'),
                        'Publishers': ('publisher_id', 'publisher_name', 'publisher', 'publishers'),
                        'Publication Series': ('pub_series_id', 'pub_series_name', 'pubseries', 'pub_series'),
                        'Award Categories': ('award_cat_id', 'award_cat_name', 'award_category', 'award_cats'),
                        'Award Types': ('award_type_id', 'award_type_name', 'awardtype', 'award_types')
                        }

        def get_search_parameters(self):
                form = cgi.FieldStorage()
                try:
                        self.operator = form['OPERATOR'].value
                        if self.operator not in self.operators:
                                raise
                except:
                        self.display_error('Invalid operator specified')

                try:
                        self.note_value = form['WEBPAGE_VALUE'].value
                        self.note_value = string.strip(self.note_value)
                except:
                        self.display_error('No Web Page value specified')

        def build_query_clause(self):
                escaped_value = db.escape_string(self.note_value)
                if self.operator == 'exact':
                        self.clause = "like '%s'" % escaped_value
                elif self.operator == 'contains':
                        self.clause = "like '%%%s%%'" % escaped_value
                elif self.operator == 'starts_with':
                        self.clause = "like '%s%%'" % escaped_value
                elif self.operator == 'ends_with':
                        self.clause = "like '%%%s'" % escaped_value
                
        def display_error(self, message):
                print '<h2>%s</h2>' % message
                PrintTrailer('search', '', 0)
                sys.exit(0)

        def get_web_pages(self):
                query = "select * from webpages where url %s limit 1000" % self.clause
                db.query(query)
                result = db.store_result()
                self.num = result.num_rows()
                record = result.fetch_row()
                while record:
                        fields = record[0]
                        if fields[WEBPAGE_AUTHOR]:
                                record_type = 'Authors'
                                record_id = fields[WEBPAGE_AUTHOR]
                        elif fields[WEBPAGE_PUBLISHER]:
                                record_type = 'Publishers'
                                record_id = fields[WEBPAGE_PUBLISHER]
                        elif fields[WEBPAGE_PUB_SERIES]:
                                record_type = 'Publication Series'
                                record_id = fields[WEBPAGE_PUB_SERIES]
                        elif fields[WEBPAGE_TITLE]:
                                record_type = 'Titles'
                                record_id = fields[WEBPAGE_TITLE]
                        elif fields[WEBPAGE_AWARD_TYPE]:
                                record_type = 'Award Types'
                                record_id = fields[WEBPAGE_AWARD_TYPE]
                        elif fields[WEBPAGE_SERIES]:
                                record_type = 'Series'
                                record_id = fields[WEBPAGE_SERIES]
                        elif fields[WEBPAGE_AWARD_CAT]:
                                record_type = 'Award Categories'
                                record_id = fields[WEBPAGE_AWARD_CAT]
                        else:
                                raise
                        self.webpages[record_type][record_id] = fields[WEBPAGE_URL]
                        record = result.fetch_row()

        def get_records(self):
                if not self.webpages:
                        return

                for record_type in self.webpages:
                        in_clause = dict_to_in_clause(self.webpages[record_type])
                        id_field = self.record_types[record_type][0]
                        name_field = self.record_types[record_type][1]
                        table = self.record_types[record_type][3]
                        query = "select %s, %s from %s where %s in (%s)" % (id_field, name_field, table, id_field, in_clause)
                        db.query(query)
                        result = db.store_result()
                        self.num = result.num_rows()
                        record = result.fetch_row()
                        while record:
                                record_id = record[0][0]
                                record_name = record[0][1]
                                self.records[record_type][record_name][record_id] = self.webpages[record_type][record_id]
                                record = result.fetch_row()

        def print_results(self):
                if not self.records:
                        print '<b>No matching records found.</b>'
                        return
                print '<b>Web Page Search is currently limited to the first 1000 matches across all record types.</b>'
                print '<p><b>Jump to record type:</b>'
                print '<ul>'
                for record_type in sorted(self.record_types):
                        if record_type in self.records:
                                count = 0
                                for record_name in self.records[record_type]:
                                        count += len(self.records[record_type][record_name])
                                print '<li><a href="#%s">%s</a> (%d)' % (record_type.replace(' ',''), record_type, count)
                print '</ul>'
                for record_type in sorted(self.record_types):
                        if record_type not in self.records:
                                continue
                        print '<h3 id="%s" class="centered">%s</h3>' % (record_type.replace(' ',''), record_type)
                        print '<table>'
                        print '<tr class="table1">'
                        print '<th>#</th>'
                        print '<th>Record Name</th>'
                        print '<th>Web Page URL</th>'
                        print '</tr>'
                        cgi_script = self.record_types[record_type][2]
                        bgcolor = 1
                        count = 1
                        for record_name in sorted(self.records[record_type]):
                                for record_id in self.records[record_type][record_name]:
                                        print '<tr class="table%d">' % (bgcolor+1)
                                        print '<td>%d</td>' % count
                                        print '<td>%s</td>' % ISFDBLink('%s.cgi' % cgi_script, record_id, record_name)
                                        print '<td>%s</td>' % self.records[record_type][record_name][record_id]
                                        print '</tr>'
                                        bgcolor ^= 1
                                        count += 1
                        print '</table>'

if __name__ == '__main__':

        PrintHeader('ISFDB Web Page Search')
        PrintNavbar('search', 0, 0, 0, 0)

        search = WebPagesSearch()
        search.get_search_parameters()
        search.build_query_clause()
        search.get_web_pages()
        search.get_records()
        search.print_results()
        PrintTrailer('webpages_search_results', 0, 0)
