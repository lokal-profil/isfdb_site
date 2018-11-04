#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2018   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from SQLparsing import *
from library import *

class elapsedTime:
	def __init__(self):
                self.start = time()
                # Save the system stdout
                self.stdout = sys.stdout

        def print_elapsed(self, report_name, threshold = 2):
                sys.stdout = self.stdout
                # If the elapsed time is more than 1 second, print how long it took to compile this report
                elapsed = time() - self.start
                if elapsed > threshold:
                        print '%s took %.2f seconds to compile' % (report_name, elapsed)
                self.start = time()


def standardReport(query, report_type):
        elapsed = elapsedTime()
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

        records = []
	while record:
		records.append(record[0][0])
        	record = result.fetch_row()

        standardReportInsert(records, report_type)
        elapsed.print_elapsed(report_type)

def standardReportFromList(id_list, report_type):
        elapsed = elapsedTime()
        standardReportInsert(id_list, report_type)
        elapsed.print_elapsed(report_type)

def standardReportInsert(id_list, report_type):
        for record_id in id_list:
                query = "select 1 from cleanup where report_type=%d and record_id=%d and resolved=1" % (int(report_type), int(record_id))
                db.query(query)
                result = db.store_result()
                # Only add to the cleanup table if this record is not "resolved"
                if not result.num_rows():
                        update = "insert into cleanup (record_id, report_type) values(%d, %d)" % (int(record_id), int(report_type))
                        db.query(update)
