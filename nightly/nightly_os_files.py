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

import os
import sys
import shutil
import string
from operator import itemgetter
from library import *
from SQLparsing import *
from library import *
from nightly_lib import elapsedTime

class Output():
        def __init__(self):
                self.data = ''

        def start(self, new_line):
                self.data = '%s\n' % new_line

        def append(self, new_line):
                self.data += '%s\n' % new_line

        def file(self, report_id, report_param):
                delete = 'delete from reports where report_id = %d and report_param = %d' % (report_id, report_param)
                db.query(delete)
                insert = """insert into reports (report_id, report_param, report_data)
                        VALUES(%d, %d, "%s")""" % (report_id, report_param, db.escape_string(self.data))
                db.query(insert)

        def topModerators(self):
                self.start('<h2>Top ISFDB Moderators</h2>')
                self.append('<p>')
                self.append('<table class="generic_table">')
                self.append('<tr align=left class="table1">')
                self.append('<th>Moderator</th>')
                self.append('<th>Total</th>')
                self.append('<th>Others</th>')
                self.append('<th>Self</th>')
                self.append('<th>Last User Activity</th>')

                query = """select sub_reviewer, count(*) as total,
                        sum(case when sub_reviewer <> sub_submitter then 1 else 0 end)
                        from submissions
                        where sub_state='I'
                        and sub_reviewer != 0
                        group by sub_reviewer
                        order by total desc"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()

                color = 0
                while record:
                        user_id = record[0][0]
                        user_name = SQLgetUserName(user_id)
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name))
                        self.append('<td>%d</td>' % (record[0][1]))
                        self.append('<td>%d</td>' % (record[0][2]))
                        self.append('<td>%d</td>' % (record[0][1] - record[0][2]))
                        last_user_activity = LastUserActivity(user_id)
                        self.append('<td>%s</td>' % last_user_activity)
                        self.append('</tr>')
                        color = color ^ 1
                        record = result.fetch_row()
                self.append('</table><p>')
                self.file(1, 0)

        def topVerifiers(self):
                details = {}
                primary = {}
                secondary = {}
                total = {}
                headers = {}

                # Primary verifications
                query = """select distinct count(pv.user_id), u.user_name
                        from primary_verifications pv, mw_user u
                        where exists(select 1 from pubs where pubs.pub_id = pv.pub_id)
                        and pv.user_id = u.user_id
                        group by pv.user_id"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        count = record[0][0]
                        user = record[0][1]
                        total[user] = total.get(user, 0) + count
                        primary[user] = primary.get(user, 0) + count
                        record = result.fetch_row() 

                # Secondary verifications
                query = """select distinct r.reference_label, count(v.user_id), u.user_name
                        from verification v, mw_user u, reference r
                        where v.ver_status='1'
                        and exists(select 1 from pubs where pubs.pub_id=v.pub_id)
                        and v.user_id=u.user_id
                        and v.reference_id=r.reference_id
                        group by v.user_id, v.reference_id"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        source = record[0][0]
                        count = record[0][1]
                        user = record[0][2]
                        if user not in details:
                                details[user] = {}
                        if source not in details[user]:
                                details[user][source] = 0
                        details[user][source] += count
                        if source not in headers:
                                headers[source] = 0
                        total[user] = total.get(user, 0) + count
                        secondary[user] = secondary.get(user, 0) + count
                        record = result.fetch_row() 

                self.start('<table cellpadding="1" class="publications">')
                self.append('<tr class="generic_table_header">')
                self.append('<th class="verifiers_user">User</th>')
                self.append('<th>Total</th>')
                self.append('<th>Primary</th>')
                self.append('<th>Secondary</th>')
                for header in sorted(headers):
                        self.append('<th>%s</th>' % header)
                self.append('</tr>')
                color = 0
                for user in sorted(total, key=total.get, reverse=True):
                        if total[user] < 10:
                                break
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user, user))

                        self.append('<td>%s</td>' % total.get(user, '&nbsp;'))

                        self.append('<td>%s</td>' % primary.get(user, '&nbsp;'))

                        self.append('<td>%s</td>' % secondary.get(user, '&nbsp;'))

                        for header in sorted(headers):
                                if user in details and header in details[user]:
                                        self.append('<td>%d</td>' % details[user][header])
                                else:
                                        self.append('<td>&nbsp;</td>')
                        self.append('</tr>')
                        color = color ^ 1

                        record = result.fetch_row()
                self.append('</table>')
                self.file(2, 0)

        def contributorStatistics(self):
                query = """select distinct sub_submitter,count(sub_submitter) as xx
                        from submissions
                        where sub_state='I'
                        group by sub_submitter
                        order by xx desc"""
                self.oneTypeContributorStatistics(query, 0)

                for sub_type in sorted(SUBMAP.keys()):
                        if SUBMAP[sub_type][3]:
                                query = """select distinct sub_submitter, count(sub_submitter) as xx
                                        from submissions
                                        where sub_state='I'
                                        and sub_type='%s'
                                        group by sub_submitter
                                        order by xx desc""" % (sub_type)
                                self.oneTypeContributorStatistics(query, sub_type)

        def oneTypeContributorStatistics(self, query, sub_type):
                self.start('<table class="generic_table">')
                self.append('<tr class="table1">')
                self.append('<th>User</th>')
                self.append('<th>Count</th>')
                self.append('<th>Moderator</th>')
                self.append('<th>Last User Activity</th>')
                self.append('</tr>')

                db.query(query)
                result = db.store_result()
                record = result.fetch_row()

                color = 0
                while record:
                        user_id = record[0][0]
                        count = record[0][1]
                        # Stop once we have reached the first user with fewer than 10 contributions
                        if count <10:
                                break
                        user_name = SQLgetUserName(user_id)
                        moderator = 'No'
                        if SQLisUserModerator(user_id):
                                moderator = 'Yes'
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name))
                        self.append('<td>%d</td>' % count)
                        self.append('<td>%s</td>' % moderator)
                        last_user_activity = LastUserActivity(user_id)
                        self.append('<td>%s</td>' % last_user_activity)
                        self.append('</tr>')
                        color = color ^ 1
                        record = result.fetch_row()
                self.append('</table><p>')
                self.file(3, sub_type)

        def summaryStatistics(self):
                self.start("<ul>")

                query = "select count(author_id) from authors"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Authors:</b> %d" % record[0][0])

                query = "select count(pub_id) from pubs"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Publications:</b> %d" % record[0][0])
                total_pubs = float(record[0][0])

                self.append("<ul>")
                query = "select distinct pub_ctype, count(pub_ctype) from pubs group by pub_ctype"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = result.fetch_row()
                self.append("</ul>")

                query = "select count(distinct pub_id) from primary_verifications"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Verified Publications:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_pubs))

                query = "select count(publisher_id) from publishers"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Publishers:</b> %d" % record[0][0])
                total_pubs = float(record[0][0])

                query = "select count(title_id) from titles"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Titles:</b> %d" % record[0][0])
                total_titles = float(record[0][0])

                self.append("<ul>")
                query = "select distinct title_ttype, count(title_ttype) from titles group by title_ttype"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = result.fetch_row()
                self.append("</ul>")
                query = "select count(distinct title_id) from votes"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Titles with Votes:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_titles))
                
                query = "select count(distinct title_id) from tag_mapping"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Titles with Tags:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_titles))


                query = "select count(award_id) from awards"
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                self.append("<li><b>Awards:</b> %d" % record[0][0])

                self.append("<ul>")
                query = """select at.award_type_name, count(at.award_type_id)
                        from awards AS aw, award_types AS at
                        where aw.award_type_id = at.award_type_id
                        group by at.award_type_name"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = result.fetch_row()
                self.append("</ul>")

                self.append("</ul>")
                self.file(4, 0)

def os_files():
        elapsed = elapsedTime()
        # First switch to the directory where the current Python module is located
        #
        # Retrieve the location of this Python module
        current_filename = os.path.abspath( __file__ )
        # Determine the directory of the current Python module
        current_dir = os.path.dirname(current_filename)
        # Determine the parent directory
        parent_dir = os.path.pardir
        # Change the current directory to the "nightly" directory
        # since cron may have started this script in a different dir
        os.chdir(current_dir)

        # Task 1: Update all SVG files
        rebuildSVG(parent_dir)
        elapsed.print_elapsed("SVG files", 0)

        # Task 2: Update summary database statistics page
        output = Output()
        output.summaryStatistics()
        elapsed.print_elapsed("Summary stats", 0)

        # Task 3: Update contributor statistics
        output.contributorStatistics()
        elapsed.print_elapsed("Contributor stats", 0)

        # Task 4: Update the list of top verifiers
        output.topVerifiers()
        elapsed.print_elapsed("Verifier stats", 0)
        
        # Task 5: Update the list of top moderators
        output.topModerators()
        elapsed.print_elapsed("Moderator stats", 0)

        # Task 6: Update the list of authors by debut date
        #AuthorsByDebutDate()
        elapsed.print_elapsed("Authors by debut date", 0)

        # Restore the original stdout
        sys.stdout = elapsed.stdout

def rebuildSVG(parent_dir):
        charts = ('year_novels','year_shortfiction','year_reviews','year_pubs','year_magazines','year_verif')
        for chart in charts:
                file_name = parent_dir + os.sep + chart + ".svg"
                sys.stdout = open(file_name, 'w')
                byYear(chart)
        
        charts = ('age_all_novels','age_all_short','age_first_novel','age_first_short')
        for chart in charts:
                file_name = parent_dir + os.sep + chart + ".svg"
                sys.stdout = open(file_name, 'w')
                byAge(chart)
        return

def byYear(chart):
	# Set the start year to 1900
	startyear = 1900
	# Set the end year to the last year
	endyear = localtime()[0]-1
	results = []
	lastyear = startyear
        if chart == "year_novels":
                query = buildQueryTitle('NOVEL', startyear, endyear)
        elif chart == "year_shortfiction":
                query = buildQueryTitle('SHORTFICTION', startyear, endyear)
        elif chart == "year_reviews":
                query = buildQueryTitle('REVIEW', startyear, endyear)
        elif chart == "year_pubs":
                query = buildQueryPub('PUBS', startyear, endyear)
        elif chart == "year_magazines":
                query = buildQueryPub('MAGAZINES', startyear, endyear)
        elif chart == "year_verif":
            query = """select YEAR(p.pub_year), count(distinct p.pub_id)
                        from pubs as p, primary_verifications as pv
                        where p.pub_id = pv.pub_id
                        and YEAR(p.pub_year)>%d
                        and YEAR(p.pub_year)<%d
                        group by YEAR(p.pub_year)""" % (startyear-1, endyear+1)
        
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
            year = record[0][0]
            count = record[0][1]
            # If there is a gap in years with no data, pad it with 0s
            if year > (lastyear+1):
                for missingyear in range(lastyear+1,year):
                    tuple = (missingyear-startyear, 0)
                    results.append(tuple)
            tuple = (year-startyear, count)
            results.append(tuple)
            record = result.fetch_row()
            # Save the last year that we had data for
            lastyear = year

        # Get the minimum and maximum values
        minimum = min(results,key=itemgetter(1))[1]
        maximum = max(results,key=itemgetter(1))[1]

        # If displaying verified pubs, do another query to get their totals for each year
        if chart == "year_verif":
            totals = []
            lastyear = startyear
            # Set the minimum and maximum value to 0 and 100 since we will be displaying percentages
            maximum = 100
            minimum = 0
            query = """select YEAR(pub_year), COUNT(pub_id) from pubs
                        where YEAR(pub_year)>%d and YEAR(pub_year)<%d
                        group by YEAR(pub_year)""" % (startyear-1, endyear+1)
            db.query(query)
            result = db.store_result()
            record = result.fetch_row()
            while record:
                total_count = record[0][1]
                year = record[0][0]
                # Calculate the relative position/index of this year in the results list
                index = year-startyear
                # Retrieve the tuple for this year
                tuple = results[index]
                # Calculate the percent of verified pubs for this year
                percent = tuple[1]*100/total_count
                # Build the new tuple, replacing the absolute value of verified pubs with the percent value for the year
                newtuple = (tuple[0], percent)
                # Replace this year's tuple in the list with the percent-based data
                results[index] = newtuple
                # Get the next year's data
                record = result.fetch_row()
                # Save the last year that we had data for
                lastyear = year
        
	years = endyear-startyear+1
	height = 200
	xscale = 6
	yscale = float(height)/float(maximum-minimum)
	results_dict = {}
	results_dict['black'] = results
	outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

def byAge(chart):
	# Set the start age to 0
	startage = 0
	# Set the end age to 100
	endage = 101
	results = []
	lastage=startage-1

        if chart[:7] == "age_all":
            if chart == "age_all_novels":
                    title_type = 'NOVEL'
            else:
                    title_type = 'SHORTFICTION'
            query = "select YEAR(t.title_copyright)-YEAR(a.author_birthdate),count(t.title_id) from titles t, "
            query += "canonical_author c, authors a where t.title_id=c.title_id and c.author_id=a.author_id and "
            query += "YEAR(t.title_copyright)<8888 and YEAR(t.title_copyright)>0 and title_ttype='%s' " % title_type
            query += "and a.author_birthdate IS NOT NULL group by YEAR(t.title_copyright)-YEAR(a.author_birthdate) limit 120"
        elif chart[:9] == "age_first":
            if chart == "age_first_novel":
                    title_type = 'NOVEL'
            else:
                    title_type = 'SHORTFICTION'
            query = "select v.FIRST-v.DOB,count(v.FIRST-v.DOB) from (select YEAR(a.author_birthdate) as DOB, "
            query += "(select min(YEAR(t.title_copyright)) from titles t, canonical_author c where "
            query += "t.title_copyright!='0000-00-00' and t.title_id=c.title_id and t.title_ttype='%s' and " % title_type
            query += "c.author_id=a.author_id and c.ca_status=1) as FIRST from authors a where a.author_birthdate "
            query += "IS NOT NULL) as v where v.FIRST IS NOT NULL group by v.FIRST-v.DOB"
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
            age = record[0][0]
            count = record[0][1]
            record = result.fetch_row()
            if age is None:
                    continue
            if age < startage or age > endage:
                    continue
            #print age
            # If there is a gap in ages with no data, pad it with 0s
            if age > (lastage+1):
                for missingage in range(lastage+1,age):
                    tuple = (missingage, 0)
                    results.append(tuple)
            tuple = (age, count)
            results.append(tuple)
            # Save the last age that we had data for
            lastage = age

        # Get the minimum and maximum values
        minimum = min(results,key=itemgetter(1))[1]
        maximum = max(results,key=itemgetter(1))[1]

	ages = endage-startage
	height = 200
	xscale = 6
	yscale = float(height)/float(maximum-minimum)
	results_dict = {}
	results_dict['black'] = results
	outputGraph(height, startage, xscale, yscale, ages, maximum, results_dict)

def LastUserActivity(user_id):
        if WikiExists():
                return SQLLastUserActivity(user_id)
        else:
                return '&nbsp;'

def AuthorsByDebutDate():
        delete = "delete from authors_by_debut_date"
	db.query(delete)
        query = """insert into authors_by_debut_date (debut_year, author_id, title_count)
                select MIN(date_format(t.title_copyright,'%Y')) debut,
                a.author_id, count(t.title_id) NumTitles
                from titles t, canonical_author ca, authors a
                where t.title_copyright not in ('0000-00-00', '8888-00-00')
                and t.title_ttype IN ('NOVEL', 'COLLECTION', 'SHORTFICTION', 'POEM')
                and ca.ca_status=1
                and ca.title_id = t.title_id
                and ca.author_id = a.author_id
                and t.title_parent = 0
                and a.author_canonical not in ('Anonymous', 'unknown', 'uncredited')
                GROUP BY ca.author_id
                HAVING NumTitles > 5"""
	db.query(query)

def buildQueryTitle(type, startyear, endyear):
        query = "select YEAR(title_copyright),COUNT(*) from titles where title_ttype='%s' and title_parent=0 and " % (type)
        query += "YEAR(title_copyright)>%d and YEAR(title_copyright)<%s group by YEAR(title_copyright)" % (startyear-1, endyear+1)
        return query

def buildQueryPub(type, startyear, endyear):
        query = "select YEAR(pub_year),COUNT(*) from pubs where "
        if type == 'PUBS':
            query += "pub_ctype!='MAGAZINE'"
        else:
            query += "pub_ctype='MAGAZINE'"
        query += " and YEAR(pub_year)>%d and YEAR(pub_year)<%s group by YEAR(pub_year)" % (startyear-1, endyear+1)
        return query
