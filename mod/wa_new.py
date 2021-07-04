#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2021   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision$
#     Date: $Date$

from isfdb import *
from isfdblib import *
from common import *
from authorClass import *
from awardtypeClass import *
from library import *
from SQLparsing import *


debug = 0

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('New Award - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

	print "<h1>SQL Updates:</h1>"
	print "<hr>"
	print "<ul>"

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('NewAward'):
                merge = doc.getElementsByTagName('NewAward')
                submitter = GetElementValue(merge, 'Submitter')

                AwardType = GetElementValue(merge, 'AwardType')
                AwardYear = GetElementValue(merge, 'AwardYear')
                AwardCategory = GetElementValue(merge, 'AwardCategory')
                AwardLevel = GetElementValue(merge, 'AwardLevel')
                AwardMovie = GetElementValue(merge, 'AwardMovie')

                #######################################
                # Get the title and author data
                #######################################
                if TagPresent(merge, 'Record'):
                        Record = GetElementValue(merge, 'Record')
                        title = SQLloadTitle(int(Record))
                        tistring = title[TITLE_TITLE]
                        authors = SQLTitleAuthors(int(Record))
                        counter = 0
                        austring = ''
                        for author in authors:
                                if counter:
                                        austring +=  "+"
                                austring += author 
                                counter += 1
                else:
                        tistring = GetElementValue(merge, 'AwardTitle')
                        counter = 0
                        austring = ''
                        value = GetElementValue(merge, 'AwardAuthors')
                        if value:
                                authors = doc.getElementsByTagName('AwardAuthor')
                                for author in authors:
                                        data = author.firstChild.data.encode('iso-8859-1')
                                        if counter:
                                                austring +=  "+"
                                        austring += data 
                                        counter += 1


                #####################################
                # Insert into the awards table
                #####################################
                insert = "insert into awards(award_title, award_author, award_year, award_level, award_movie, award_type_id, award_cat_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%d')" % (db.escape_string(tistring), db.escape_string(austring), db.escape_string(AwardYear), db.escape_string(AwardLevel), db.escape_string(AwardMovie), int(AwardType), int(AwardCategory))
                print "<li> ", insert
                if debug == 0:
                        db.query(insert)
                award_id = db.insert_id()

                #####################################
                # Insert a title mapping record
                #####################################
                if TagPresent(merge, 'Record'):
                        insert = "insert into title_awards(award_id, title_id) values(%d, %d)" % (int(award_id), int(Record))
                        print "<li> ", insert
                        if debug == 0:
                                db.query(insert)

                #####################################
                # Insert into the Notes table
                #####################################
                note_id = ''
                note = GetElementValue(merge, 'AwardNote')
                if note:
                        insert = "insert into notes(note_note) values('%s');" % db.escape_string(note)
                        print "<li> ", insert
                        db.query(insert)
                        note_id = int(db.insert_id())
                        update = "update awards set award_note_id = %d where award_id=%d" % (note_id, award_id)
                        print "<li> ", update
                        db.query(update)

        if debug == 0:
                markIntegrated(db, submission, award_id)

        try:
                # Only display title links if this award was entered for a Title record
                if TagPresent(merge, 'Record'):
                        print '[<a href="http:/' +HTFAKE+ '/edit/edittitle.cgi?%d">Edit This Title</a>]' % (int(Record))
                        print '[<a href="http:/' +HTFAKE+ '/title.cgi?%d">View This Title</a>]' % (int(Record))

                print '[<a href="http:/%s/award_details.cgi?%d">View This Award</a>]' % (HTFAKE, int(award_id))
                print '[<a href="http:/' +HTFAKE+ '/edit/editaward.cgi?%d">Edit This Award</a>]' % (int(award_id))
                print '[<a href="http:/' +HTFAKE+ '/ay.cgi?%s+%s">View Award Year</a>]' % (AwardType, AwardYear[:4])
        except:
                pass
        print "<p>"

        PrintPostMod(0)
