#!_PYTHONLOC
# -*- coding: cp1252 -*-
#
#     (C) COPYRIGHT 2017   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.1 $
#     Date: $Date: 2017/05/08 17:31:05 $

import string
from SQLparsing import *
from library import *
from nightly_lib import *

def OneRecordType(report_id, in_clause, table, note_field, record_id_field):
        query = "select %s from %s where %s in (%s)" % (record_id_field, table, note_field, in_clause)
        standardReport(query, report_id)

def nightly_html():
        query = "select note_id from notes where "
        query += BadHtmlClause('note_note')
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()
        note_list = []
        while record:
                note_id = record[0][0]
                note_list.append(note_id)
                record = result.fetch_row()
        in_clause = list_to_in_clause(note_list)
        record_types = (('pubs', 'note_id', 'pub_id', 208),
                    ('titles', 'note_id', 'title_id', 209),
                    ('publishers', 'note_id', 'publisher_id', 210),
                    ('series', 'series_note_id', 'series_id', 211),
                    ('pub_series', 'pub_series_note_id', 'pub_series_id', 212),
                    ('awards', 'award_note_id', 'award_id', 213),
                    ('award_types', 'award_type_note_id', 'award_type_id', 214),
                    ('award_cats', 'award_cat_note_id', 'award_cat_id', 215),
                    ('titles', 'title_synopsis', 'title_id', 216))
        for record_data in record_types:
                table = record_data[0]
                note_field = record_data[1]
                record_id_field = record_data[2]
                report_id = record_data[3]
                OneRecordType(report_id, in_clause, table, note_field, record_id_field)

        # Author notes are processed separately since they are stored in the main author table
        query = "select author_id from authors where "
        query += BadHtmlClause('author_note')
        standardReport(query, 217)
