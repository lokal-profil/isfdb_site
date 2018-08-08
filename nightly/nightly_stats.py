#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2018   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 181 $
#     Date: $Date: 2018-08-06 22:48:08 -0400 (Mon, 06 Aug 2018) $

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
                self.elapsed = elapsedTime()

        def start(self, new_line):
                self.data = '%s\n' % new_line

        def append(self, new_line):
                self.data += '%s\n' % new_line

        def subheader(self, subheader):
                self.data += '<h3>%s</h3>\n' % subheader

        def file(self, report_id, report_param):
                delete = 'delete from reports where report_id = %d and report_param = %d' % (report_id, report_param)
                db.query(delete)
                insert = """insert into reports (report_id, report_param, report_data)
                        VALUES(%d, %d, "%s")""" % (report_id, report_param, db.escape_string(self.data))
                db.query(insert)

        def report(self, method_name):
                method = getattr(self, method_name)
                method()
                self.elapsed.print_elapsed(method_name)

        def LastUserActivity(self, user_id):
                if WikiExists():
                        return SQLLastUserActivity(user_id)
                else:
                        return '&nbsp;'

        def outputGraph(self, height, startyear, xscale, yscale, years, maximum, results):
                xoffset = 15
                yoffset = 10

                self.append('<svgcode width="%d" height="%d" version="1.1">' % (xoffset+40+(years*xscale), height+30+yoffset))
                self.append('<svg width="100%%" height="%dpx" version="1.1" xmlns="http://www.w3.org/2000/svg">' % (height+30+yoffset))

                ###################################################
                # Output the grid and labels - Horizontal Lines
                ###################################################
                y = 0
                increment = maximum/4
                value = increment * 4
                while y <= height:
                        self.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="svg1"/>' % (xoffset, y+yoffset, xoffset+5+(years*xscale), y+yoffset))
                        self.append('<text x="%d" y="%d" font-size="10">%d</text>' % (xoffset+10+(years*xscale), y+5+yoffset, value))
                        value -= increment
                        y = y + 50

                ###################################################
                # Output the grid and labels - Vertical Lines
                ###################################################
                x = 0
                while x < years:
                        self.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="svg1"/>' % (xoffset+(xscale*x), yoffset, xoffset+(xscale*x), height+10+yoffset))
                        self.append('<text x="%d" y="%d" font-size="10">%d</text>' % ((xscale*x)-12+xoffset, height+20+yoffset, x+startyear))
                        x += 10

                ###################################################
                # Output the data
                ###################################################
                for line_color in results:
                        index = 0
                        last = (0, 0)
                        while index < years:
                                if index:
                                        self.append('<line x1="%d"' % (xoffset+(xscale * last[0])))
                                        self.append(' y1="%d"' % (yoffset+(int(yscale * float(last[1])))))
                                        self.append(' x2="%d"' % (xoffset+(xscale * results[line_color][index][0])))
                                        self.append(' y2="%d"' % (yoffset+(int(yscale * float(maximum-results[line_color][index][1])))))
                                        self.append('class="svg%s"/>' % line_color)
                                last = (results[line_color][index][0], maximum-results[line_color][index][1])
                                index += 1

                self.append('</svg>')
                self.append('</svgcode>')

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
                        last_user_activity = self.LastUserActivity(user_id)
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
                        last_user_activity = self.LastUserActivity(user_id)
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

        def titlesByYear(self):
                self.data = ''
                self.byYear('NOVEL', 'Novels')
                self.byYear('SHORTFICTION', 'Short Fiction')
                self.byYear('REVIEW', 'Reviews')
                self.file(5, 0)

        def publicationsByYear(self):
                self.data = ''
                self.byYear('PUBS', 'Publications (without magazines)')
                self.byYear('MAGAZINES', 'Magazines')
                self.byYear('VERIFIED', 'Verified Publications in Percent')
                self.file(6, 0)

        def titlesByAuthorAge(self):
                self.data = ''
                self.byAge('NOVEL', 'all', 'All Novels')
                self.byAge('NOVEL', 'first', 'First Novels')
                self.byAge('SHORTFICTION', 'all', 'All Short Fiction')
                self.byAge('SHORTFICTION', 'first', 'First Short Fiction')
                self.file(7, 0)

        def byYear(self, chart, subheader):
                self.subheader(subheader)
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the last year
                endyear = localtime()[0]-1
                results = []
                lastyear = startyear
                if chart in ('NOVEL', 'SHORTFICTION', 'REVIEW'):
                        query = """select YEAR(title_copyright),COUNT(*)
                                from titles where title_ttype='%s'
                                and title_parent=0
                                and YEAR(title_copyright)>%d
                                and YEAR(title_copyright)<%d
                                group by YEAR(title_copyright)""" % (chart, startyear-1, endyear+1)
                elif chart == 'VERIFIED':
                        query = """select YEAR(p.pub_year), count(distinct p.pub_id)
                                from pubs as p, primary_verifications as pv
                                where p.pub_id = pv.pub_id
                                and YEAR(p.pub_year)>%d
                                and YEAR(p.pub_year)<%d
                                group by YEAR(p.pub_year)""" % (startyear-1, endyear+1)
                else:
                        query = "select YEAR(pub_year),COUNT(*) from pubs where "
                        if chart == 'PUBS':
                            query += "pub_ctype!='MAGAZINE'"
                        else:
                            query += "pub_ctype='MAGAZINE'"
                        query += " and YEAR(pub_year)>%d and YEAR(pub_year)<%s group by YEAR(pub_year)" % (startyear-1, endyear+1)
                
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
                if chart == 'VERIFIED':
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
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

        def byAge(self, title_type, chart, subheader):
                self.subheader(subheader)
                # Set the start age to 0
                startage = 0
                # Set the end age to 100
                endage = 101
                results = []
                lastage=startage-1

                if chart == 'all':
                    query = "select YEAR(t.title_copyright)-YEAR(a.author_birthdate),count(t.title_id) from titles t, "
                    query += "canonical_author c, authors a where t.title_id=c.title_id and c.author_id=a.author_id and "
                    query += "YEAR(t.title_copyright)<8888 and YEAR(t.title_copyright)>0 and title_ttype='%s' " % title_type
                    query += "and a.author_birthdate IS NOT NULL group by YEAR(t.title_copyright)-YEAR(a.author_birthdate) limit 120"
                else:
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
                self.outputGraph(height, startage, xscale, yscale, ages, maximum, results_dict)

        def novelsInSeries(self):
                self.start('<h3>Legend: Red - novels, Blue - short fiction</h3>')
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the current year
                endyear = localtime()[0]

                results_dict = {}
                results_dict['red'] = self.novelsInSeriesoneType('NOVEL', startyear, endyear)
                results_dict['blue'] = self.novelsInSeriesoneType('SHORTFICTION', startyear, endyear)

                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(8, 0)

        def novelsInSeriesoneType(self, title_type, startyear, endyear):
                query = """select substring(title_copyright,1,4),count(*) as total,
                        count(series_id>0) as in_series, count(series_id>0)/count(*)*100 as ratio
                        from titles
                        where title_ttype="%s"
                        and substring(title_copyright,1,4)>%d
                        and substring(title_copyright,1,4)<%d
                        and title_parent=0
                        group by substring(title_copyright,1,4)""" % (title_type, startyear-1, endyear+1)

                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                results = []
                while record:
                        year = record[0][0]
                        percent = record[0][3]
                        data_tuple = (int(year)-startyear, int(round(float(percent))))
                        results.append(data_tuple)
                        record = result.fetch_row()
                return results

        def titlesByTypeByYear(self):
                self.start('<h3>Legend: Red - novels, Blue - collections, Green - anthologies, Yellow - omnibuses, Orange - chapbooks</h3>')
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the current year
                endyear = localtime()[0]

                # Retrieve the data from the database
                query = """select YEAR(title_copyright),title_ttype,count(*) from titles
                        where YEAR(title_copyright)>%d
                        and YEAR(title_copyright)<%d
                        and title_ttype in ('ANTHOLOGY', 'NOVEL', 'COLLECTION', 'CHAPBOOK', 'OMNIBUS')
                        and title_parent=0
                        group by YEAR(title_copyright), title_ttype""" % (startyear-1, endyear+1)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                total = AutoVivification()
                bytype = AutoVivification()
                while record:
                    year = record[0][0]
                    title_type = record[0][1]
                    count = record[0][2]
                    if not total[year]:
                            total[year] = 0
                    total[year] += count
                    if not bytype[title_type][year]:
                            bytype[title_type][year] = 0
                    bytype[title_type][year] += count
                    record = result.fetch_row()

                # Add any missing years
                for title_type in bytype.keys():
                        for year in range(startyear,endyear+1):
                                if year not in bytype[title_type]:
                                        bytype[title_type][year] = 0

                colors = {'red' : 'NOVEL',
                          'blue': 'COLLECTION',
                          'green': 'ANTHOLOGY',
                          'yellow':  'OMNIBUS',
                          'orange': 'CHAPBOOK'}
                results_dict = {}
                for color in colors:
                        title_type = colors[color]
                        results_dict[color] = []
                        for year in bytype[title_type]:
                                percent = bytype[title_type][year] * 100 / total[year]
                                year_tuple = (int(year) - startyear, percent)
                                results_dict[color].append(year_tuple)

                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(9, 0)

        def pubsByFormat(self):
                self.start('<h3>Legend:')
                self.append('Red - %s, ' % ISFDBPubFormat('pb'))
                self.append('Blue - %s, ' % ISFDBPubFormat('tp'))
                self.append('Green - %s, ' % ISFDBPubFormat('hc'))
                self.append('Yellow - %s, ' % ISFDBPubFormat('pulp'))
                self.append('Orange - %s, ' % ISFDBPubFormat('digest'))
                self.append('Pink - %s, ' % ISFDBPubFormat('ebook'))
                self.append('Black - all other formats</h3>')
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the last year (current year may not have enough data points)
                endyear = localtime()[0]-1
                # Define recognize formats
                recognized = ('pb','tp','hc','pulp','digest','ebook')

                # Retrieve the data from the database
                query = """select YEAR(pub_year), pub_ptype, count(*)
                           from pubs where YEAR(pub_year)>%d
                           and YEAR(pub_year)<%d and pub_ptype!="unknown"
                           group by pub_ptype, YEAR(pub_year)""" % (startyear-1, endyear+1)
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                total = AutoVivification()
                bytype = AutoVivification()
                while record:
                    year = record[0][0]
                    pub_type = record[0][1]
                    count = record[0][2]
                    if not total[year]:
                            total[year] = 0
                    total[year] += count
                    if pub_type not in recognized:
                            pub_type = 'other'
                    if not bytype[pub_type][year]:
                            bytype[pub_type][year] = 0
                    bytype[pub_type][year] += count
                    record = result.fetch_row()

                # Add any missing years
                for pub_type in bytype.keys():
                        for year in range(startyear,endyear+1):
                                if year not in bytype[pub_type]:
                                        bytype[pub_type][year] = 0

                colors = {'red' : 'pb',
                          'blue': 'tp',
                          'green': 'hc',
                          'yellow':  'pulp',
                          'orange': 'digest',
                          'black': 'other',
                          'pink': 'ebook'}
                results_dict = {}
                for color in colors:
                        pub_type = colors[color]
                        results_dict[color] = []
                        for year in bytype[pub_type]:
                                percent = bytype[pub_type][year] * 100 / total[year]
                                year_tuple = (int(year) - startyear, percent)
                                results_dict[color].append(year_tuple)

                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(10, 0)

        def authorsByDebutDate(self):
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

        def submissionsByYear(self):
                # Set the start year to 2007
                startyear = 2007
                # Set the end year to the last year
                currentyear = localtime()[0]
                lastyear = currentyear - 1
                years = lastyear - startyear + 1

                # Retrieve the data from the database
                query = """select YEAR(sub_time), count(*)
                        from submissions
                        where YEAR(sub_time) > 2006
                        group by YEAR(sub_time)
                        order by YEAR(sub_time)"""
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                results_dict = {}
                results_dict['black'] = []
                minimum = 0
                maximum = 0
                while record:
                        year = record[0][0]
                        count = record[0][1]
                        data_tuple = (int(year) - startyear, int(count))
                        results_dict['black'].append(data_tuple)
                        if count > maximum:
                                maximum = count
                        record = result.fetch_row()

                height = 200
                xscale = 50
                yscale = float(height)/float(maximum - minimum)
                self.start('')
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(11, 0)

def nightly_stats():
        output = Output()
        output.report("submissionsByYear")
        output.report("titlesByYear")
        output.report("publicationsByYear")
        output.report("titlesByAuthorAge")
        output.report("summaryStatistics")
        output.report("contributorStatistics")
        output.report("topVerifiers")
        output.report("topModerators")
        output.report("novelsInSeries")
        output.report("titlesByTypeByYear")
        output.report("pubsByFormat")
        output.report("authorsByDebutDate")
