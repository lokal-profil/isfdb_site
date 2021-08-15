#
#     (C) COPYRIGHT 2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 203 $
#     Date: $Date: 2018-09-12 17:38:34 -0400 (Wed, 12 Sep 2018) $

import cgi
from isfdb import *
from library import XMLescape
from SQLparsing import SQLGetVerificationSource


class VerificationSource():
        def __init__(self):
                self.used_id = 0
                self.used_label = 0
                self.used_name = 0
                self.used_url = 0

                self.id = ''
                self.label = ''
                self.name = ''
                self.url = ''

                self.error = ''

        def load(self, record_id):
                if not record_id:
                        return
                self.id = record_id
                self.used_id = 1
                record = SQLGetVerificationSource(self.id)
                if not record:
                        return
                if record[REFERENCE_LABEL]:
                        self.label = record[REFERENCE_LABEL]
                        self.used_label = 1
                if record[REFERENCE_NAME]:
                        self.name = record[REFERENCE_NAME]
                        self.used_name = 1
                if record[REFERENCE_URL]:
                        self.url = record[REFERENCE_URL]
                        self.used_url = 1

        def cgi2obj(self):
		self.form = cgi.FieldStorage()
		if self.form.has_key('source_id'):
			self.id = XMLescape(self.form['source_id'].value)
			self.used_id = 1
		else:
                        self.error = 'Verification Source ID is a required field'
                        return
                if not SQLGetVerificationSource(self.id):
                        self.error = 'This Verification Source ID is not on file'
                        return

                if self.form.has_key('source_label'):
                        self.label = XMLescape(self.form['source_label'].value)
                        self.used_label = 1
                else:
                        self.error = 'Verification Source Label is a required field'
                        return

                if self.form.has_key('source_name'):
                        self.name = XMLescape(self.form['source_name'].value)
                        self.used_name = 1
                else:
                        self.error = 'Verification Source name is a required field'
                        return

                if self.form.has_key('source_url'):
                        self.url = XMLescape(self.form['source_url'].value)
                        self.used_url = 1
                else:
                        self.error = 'Verification Source URL is a required field'
                        return
