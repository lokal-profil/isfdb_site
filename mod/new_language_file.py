#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 676 $
#     Date: $Date: 2021-07-05 12:14:45 -0400 (Mon, 05 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from SQLparsing import *
from library import *


if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

	PrintPreMod('Add New Language - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        merge = doc.getElementsByTagName('NewLanguage')
        if not merge:
		print '<div id="ErrorBox">'
		print '<h3>Error: Bad argument</h3>'
		print '</div>'
		PrintPostMod()
		sys.exit(0)

	print '<h1>SQL Updates:</h1>'
	print '<hr>'
	print '<ul>'
        lang_name = GetElementValue(merge, 'LanguageName')
        lang_code = GetElementValue(merge, 'LanguageCode')
        latin_script = GetElementValue(merge, 'Latin')
        insert = "insert into languages(lang_name, lang_code, latin_script) values('%s', '%s', '%s')" % (db.escape_string(lang_name),
                                                                                                         db.escape_string(lang_code),
                                                                                                         db.escape_string(latin_script))
        print '<li> ', insert
        db.query(insert)

        markIntegrated(db, submission)

	PrintPostMod(0)
