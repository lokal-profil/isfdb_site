#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2017   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.7 $
#     Date: $Date: 2017/07/08 01:24:36 $

import os
import sys
import shutil
import string
from operator import itemgetter
from library import *
from SQLparsing import *
from library import *
from nightly_lib import elapsedTime

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

        # Task 1: Update the ISFDB banner by rotating the available images
        updateBanner(parent_dir)
        
        # Task 2: Update all SVG files
        rebuildSVG(parent_dir)
        elapsed.print_elapsed("SVG files", 0)

        # Task 3: Update summary database statistics page
        summaryStatistics(parent_dir)
        elapsed.print_elapsed("Summary stats", 0)

        # Task 4: Update contributor statistics
        contributorStatistics(parent_dir)
        elapsed.print_elapsed("Contributor stats", 0)

        # Task 5: Update the list of top verifiers
        topVerifiers(parent_dir)
        elapsed.print_elapsed("Verifier stats", 0)
        
        # Task 6: Update the list of top moderators
        topModerators(parent_dir)
        elapsed.print_elapsed("Moderator stats", 0)

        # Task 7: Update the list of authors by debut date
        AuthorsByDebutDate(parent_dir)
        elapsed.print_elapsed("Authors by debut date", 0)

        # Restore the original stdout
        sys.stdout = elapsed.stdout

def updateBanner(parent_dir):

	# Load the current banner number
	fd = open('CurrentBanner')
	current = fd.readline()
	fd.close()

        # Create a list of recognized banner/jpg files
        list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	# Calculate the next banner number
	next = int(current)+1;
	# If the next number is greater than the last existing file, use the first one
	if next <= list[-1]:
		pass
	else:
		next = int(list[0])

	# Copy the banner
	nextFile = 'IsfdbBanner'+str(next)+'.jpg'
        # Copy the current banner file to the parent directory
        shutil.copy(nextFile, parent_dir + os.sep + 'IsfdbBanner.jpg')
	
	# Update the CurrentBanner file
	fd = open('CurrentBanner', 'w+')
	fd.write(str(next))
	fd.close()
	return

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

def summaryStatistics(parent_dir):
        # Redirect output to the Summary Statistics file
        file_name = parent_dir + os.sep + "summary_statistics.html"
        sys.stdout = open(file_name, 'w')
        
	print "<ul>"

	query = "select count(author_id) from authors"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Authors:</b>", record[0][0]

	query = "select count(pub_id) from pubs"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Publications:</b>", record[0][0]
	total_pubs = float(record[0][0])

	print "<ul>"
	query = "select distinct pub_ctype, count(pub_ctype) from pubs group by pub_ctype"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		print "<li>%s: %d" % (record[0][0], record[0][1])
		record = result.fetch_row()
	print "</ul>"

	query = "select count(distinct pub_id) from primary_verifications"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Verified Publications:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_pubs)

	query = "select count(publisher_id) from publishers"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Publishers:</b>", record[0][0]
	total_pubs = float(record[0][0])

	query = "select count(title_id) from titles"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Titles:</b>", record[0][0]
	total_titles = float(record[0][0])

	print "<ul>"
	query = "select distinct title_ttype, count(title_ttype) from titles group by title_ttype"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		print "<li>%s: %d" % (record[0][0], record[0][1])
		record = result.fetch_row()
	print "</ul>"
	query = "select count(distinct title_id) from votes"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Titles with Votes:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_titles)
	
	query = "select count(distinct title_id) from tag_mapping"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Titles with Tags:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/total_titles)


	query = "select count(award_id) from awards"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	print "<li><b>Awards:</b>", record[0][0]

	print "<ul>"
	query = "select at.award_type_name, count(at.award_type_id) from awards AS aw, award_types AS at where aw.award_type_id = at.award_type_id group by at.award_type_name"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	while record:
		print "<li>%s: %d" % (record[0][0], record[0][1])
		record = result.fetch_row()
	print "</ul>"

	print "</ul>"

def contributorStatistics(parent_dir):
        file_name = parent_dir + os.sep + "top_contributors_all.html"
        sys.stdout = open(file_name, 'w')
        query = "select distinct sub_submitter,count(sub_submitter) as xx from submissions where sub_state='I' group by sub_submitter order by xx desc"
        oneTypeContributorStatistics(query)

	for type in sorted(SUBMAP.keys()):
                if SUBMAP[type][3]:
                        file_name = '%s%stop_contributors%d.html' % (parent_dir, os.sep, type)
                        sys.stdout = open(file_name, 'w')
                        query = "select distinct sub_submitter, count(sub_submitter) as xx from "
                        query += "submissions where sub_state='I' and sub_type='%s' group by sub_submitter order by xx desc" % (type)
                        oneTypeContributorStatistics(query)


def oneTypeContributorStatistics(query):
	print '<table class="generic_table">'
	print '<tr class="table1">'
	print '<th>User</th>'
	print '<th>Count</th>'
	print '<th>Last User Activity</th>'
	print '</tr>'

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
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
                print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name)
		print '<td>%d</td>' % count
		print '<td>%s</td>' % SQLLastUserActivity(user_id)
		print '</tr>'
		color = color ^ 1
        	record = result.fetch_row()
	print '</table><p>'

def topVerifiers(parent_dir):
        file_name = parent_dir + os.sep + "top_verifiers.html"
        sys.stdout = open(file_name, 'w')

	print '<table cellpadding="1" class="publications">'

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

	print '<tr class="generic_table_header">'
	print '<th class="verifiers_user">User</th>'
	print '<th>Total</th>'
	print '<th>Primary</th>'
	print '<th>Secondary</th>'
	for header in sorted(headers):
                print '<th>%s</th>' % header
 	print '</tr>'
	color = 0
	for user in sorted(total, key=total.get, reverse=True):
                if total[user] < 10:
                        break
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
                print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user, user)

                print '<td>%s</td>' % total.get(user, '&nbsp;')

                print '<td>%s</td>' % primary.get(user, '&nbsp;')

                print '<td>%s</td>' % secondary.get(user, '&nbsp;')

                for header in sorted(headers):
                        if user in details and header in details[user]:
                                print '<td>%d</td>' % details[user][header]
                        else:
                                print '<td>&nbsp;</td>'
		print '</tr>'
		color = color ^ 1

        	record = result.fetch_row()
	print '</table>'


def topModerators(parent_dir):
        file_name = parent_dir + os.sep + "top_moderators.html"
        sys.stdout = open(file_name, 'w')
	print '<h2>Top ISFDB Moderators</h2>'
	print '<p>'
	print '<table class="generic_table">'
	print '<tr align=left class="table1">'
	print '<th>Moderator</th>'
	print '<th>Total</th>'
	print '<th>Others</th>'
	print '<th>Self</th>'
	print '<th>Last User Activity</th>'

        query = "select sub_reviewer, count(*) as total, sum(case when sub_reviewer <> sub_submitter then 1 else 0 end) from submissions where sub_state='I' and sub_reviewer != 0 group by sub_reviewer order by total desc"
	#query = "select distinct sub_reviewer,count(sub_reviewer) as xx from submissions where sub_state='I' group by sub_reviewer order by xx desc"
	db.query(query)
	result = db.store_result()
        record = result.fetch_row()

	color = 0
	while record:
                user_id = record[0][0]
                user_name = SQLgetUserName(user_id)
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
                print '<td><a href="http://%s/index.php/User:%s">%s</a></td>' % (WIKILOC, user_name, user_name)
		print '<td>%d</td>' % (record[0][1])
		print '<td>%d</td>' % (record[0][2])
		print '<td>%d</td>' % (record[0][1] - record[0][2])
		print '<td>%s</td>' % SQLLastUserActivity(user_id)
		print '</tr>'
		color = color ^ 1
        	record = result.fetch_row()
	print '</table><p>'

def AuthorsByDebutDate(parent_dir):
        query = "select MIN(date_format(t.title_copyright,'%Y')) debut, a.author_id, a.author_canonical, count(*) NumTitles, a.author_lastname"
        query += " from titles t, canonical_author ca, authors a where t.title_copyright!='0000-00-00'"
        query += " and t.title_ttype IN ('NOVEL','COLLECTION','SHORTFICTION','SERIAL','POEM') and ca.ca_status=1"
        query += " and ca.title_id = t.title_id and ca.author_id = a.author_id and t.title_parent = 0"
        query += " and a.author_canonical not in ('Anonymous','unknown','uncredited')"
        query += " GROUP BY ca.author_id HAVING NumTitles > 5 ORDER BY 1,5,2"
	db.query(query)
	result = db.store_result()
	record = result.fetch_row()
	decades = {}
	while record:
                decade = int(record[0][0])/10
                # For years prior to 1900, put all authors into a single bucket, 100
                if decade < 190:
                        decade = 100
                if decade not in decades:
                        decades[decade] = [record[0]]
                else:
                        decades[decade].append(record[0])
        	record = result.fetch_row()
	for decade in decades:
                AuthorsForOneDecade(parent_dir, decade, decades[decade])

def AuthorsForOneDecade(parent_dir, decade, data):
        # Redirect output to a decade-specific file
        file_name =  '%s%sauthors_by_debut_year_%d.html' % (parent_dir, os.sep, decade)
        sys.stdout = open(file_name, 'w')
	print '<table cellpadding="3" bgcolor="#FFFFFF">'
	print '<tr align=left class="table1">'
	print '<td><b>Debut Year</b></td>'
	print '<td><b>Author</b></td>'
	print '<td><b>Number of Titles</b></td>'
	print '</tr>'
	color = 0
	for record in data:
		if color:
			print '<tr align=left class="table1">'
		else:
			print '<tr align=left class="table2">'
		print '<td>%s</td>' % (record[0])
		print '<td><a href="http:/%s/ea.cgi?%s">%s</a></td>' % (HTFAKE, record[1], record[2])
		print '<td>%d</td>' % (record[3])
		print '</tr>'
		color = color ^ 1
	print '</table><p>'

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
