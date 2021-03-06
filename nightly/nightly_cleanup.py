#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 844 $
#     Date: $Date: 2022-02-15 16:06:20 -0500 (Tue, 15 Feb 2022) $

from SQLparsing import *
from library import *
from shared_cleanup_lib import *

def nightly_cleanup():
        # Regenerate nightly cleanup reports
        #
        #   Report 2: VT-Pseudonym mismatches
        # Exclude VTs whose author credit is a pseudonym of the parent's author credit
        # Exclude VTs of:
        #    uncredited, unknown, The Editor, Afred Hitchcock, V. C. Andrews
        #    Warren Murphy, Richard Sapir, Bruce Boxleitner, The Editors, Anonymous
        # Exclude VTs whose parent has a credit to the same author.  These cases will be
        # variant where title text is different but author is the same and variant between
        # a single-author credit and a collaboration credit.
        query = "select t.title_id as vt from titles t \
                where t.title_parent is not null and t.title_parent <> 0 \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and vca.author_id = pca.author_id \
                ) \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca, pseudonyms p \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and p.pseudonym = vca.author_id and p.author_id = pca.author_id \
                ) \
                and not exists ( \
                  select * from canonical_author vca, canonical_author pca \
                  where vca.title_id = t.title_id and pca.title_id = t.title_parent \
                  and (pca.author_id = 20754 or pca.author_id = 2862 or pca.author_id = 38721 \
                  or vca.author_id = 20754 or vca.author_id = 2862 or vca.author_id = 38721 \
                  or vca.author_id = 7977 or vca.author_id = 1449 or vca.author_id = 1414 \
                  or vca.author_id = 3781 or vca.author_id = 6358 or vca.author_id = 38941 \
                  or pca.author_id = 6677 or vca.author_id = 6677) \
                )"
        standardReport(query, 2)
        
        #   Report 3: Titles without Pubs. Note that the logic ignores pub-less titles that have VTs.
        query = """select t1.title_id from titles t1
                where t1.title_copyright != '8888-00-00'
                and not exists (select 1 from pub_content where t1.title_id=pub_content.title_id)
                and not exists (select 1 from titles t2 where t1.title_id=t2.title_parent)"""
        standardReport(query, 3)

        #   Report 5: Notes with an odd number of angle brackets
        query = "select note_id, LENGTH(note_note) - LENGTH(REPLACE(note_note, '<', '')) openquote, \
                LENGTH(note_note) - LENGTH(REPLACE(note_note, '>', '')) closequote \
                from notes having openquote != closequote"
        standardReport(query, 5)

        #   Report 6: Authors with invalid Directory Entries
        query = """select author_id from authors
                   where author_lastname like '%&#%'
                   or not hex(author_lastname) regexp '^([0-7][0-9A-F])*$'"""
        standardReport(query, 6)

        #   Report 7: Authors with invalid spaces
	query = """select author_id from authors
                where author_canonical like ' %'
                or author_canonical like '% '
                or author_canonical like '%  %'
                or author_canonical like '%\"%'
                or (
                author_canonical NOT LIKE '%.com'
                and author_canonical NOT LIKE '%.co.uk'
                and """

	suffixes = []
	for suffix in RECOGNIZED_SUFFIXES:
                if suffix.count('.') < 2:
                        continue
                period_letter = 0
                for fragment in suffix.split('.'):
                        if not fragment.startswith(' '):
                                period_letter = 1
                                break
                if period_letter:
                        suffixes.append(suffix)

        subquery = ''
        for suffix in suffixes:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        query += subquery
        query += """ REGEXP '\\\\.[a-z]' = 1)"""
        standardReport(query, 7)

        #   Report 8: Authors that exist only due to reviews
	query =  "select ca.title_id from canonical_author ca, authors a, titles t"
	query += " WHERE ca.ca_status = 3 and ca.author_id = a.author_id and ca.title_id = t.title_id"
	query += " AND NOT EXISTS (SELECT 1 from canonical_author ca2, titles t"
	query += "                 where ca.author_id = ca2.author_id"
	query += " 		AND  ca2.title_id = t.title_id"
	query += " 		AND  t.title_ttype != 'REVIEW'"
	query += " 		and  ca2.ca_status = 1)"
        standardReport(query, 8)

        #   Report 10: Pseudonyms with Canonical Titles
        # First retrieve all pseudonyms on file
        query = 'select distinct(pseudonym) from pseudonyms'
        db.query(query)
        result = db.store_result()
        pseudos = {}
        record = result.fetch_row()
        while record:
                pseudo_id = record[0][0]
                # Retrieve the number of canonical titles for this pseudonym
                query2 = 'select count(t.title_id) from canonical_author c, titles t where c.author_id=%s \
                        and c.ca_status=1 and c.title_id=t.title_id and t.title_parent=0' % pseudo_id
                db.query(query2)
                result2 = db.store_result()
                record2 = result2.fetch_row()
                # If there are canonical titles for this pseudonym, then add it to the list of "problem pseudonyms"
                if record2[0][0] != 0:
                        pseudos[unicode(pseudo_id)] = record2[0][0]
                record = result.fetch_row()

        if pseudos:
                # Build a pseudo-query to be passed to standardReport()
                query = ''
                for pseudo_id in pseudos:
                        if query:
                                query += ',%s' % pseudo_id
                        else:
                                query = pseudo_id
                query = 'select author_id from authors where author_id in (%s)' % query
                standardReport(query, 10)

        #   Report 11: Prolific Authors without a Defined Language
        # Ignore the following authors: unknown, Anonymous, various, uncredited, The Readers, The Editors, Traditional
        query = 'select c.author_id from canonical_author as c, authors as a \
                where c.author_id=a.author_id and a.author_language IS NULL \
                and a.author_id not in (20754, 7311, 25179, 2862, 38941, 6677, 17640) \
                group by c.author_id order by count(c.author_id) desc limit 300'
        standardReport(query, 11)

        #   Report 12: Editor Records not in a Series
        query = "select title_id from titles where title_ttype = 'EDITOR' and series_id IS NULL and title_parent = 0"
        standardReport(query, 12)

        #   Report 16: Empty Series
	query =  """select series_id from series s1
                    where not exists
                    (select 1 from titles t where t.series_id = s1.series_id)
                    and not exists
                    (select 1 from series s2 where s2.series_parent = s1.series_id)"""
        standardReport(query, 16)

        #   Report 17: Series with Duplicate Series Numbers
        query = """select distinct series_id from titles
                where series_id IS NOT NULL
                and title_seriesnum IS NOT NULL
                group by series_id, title_seriesnum, title_seriesnum_2
                having count(*) >1"""
        standardReport(query, 17)

        #   Report 19: Interviews of Pseudonyms
	query = "select ca.title_id from titles t, canonical_author ca, authors a \
                where t.title_ttype = 'INTERVIEW' and ca.title_id = t.title_id \
                and ca.author_id = a.author_id and ca.ca_status = 2 \
                and a.author_canonical != 'uncredited' and exists \
                (select 1 from pseudonyms p where a.author_id = p.pseudonym)"
        standardReport(query, 19)

        #   Report 22: SERIALs without a Parent Title
	query = "select title_id from titles where title_ttype='SERIAL' and title_parent=0"
        standardReport(query, 22)

        #   Report 24: Suspect Untitled Awards
        # Ignore Locus awards for years prior to 2011, Aurealis awards for 2008, and Hugo awards for 1964
        # because they are known exceptions due to a single award given to multiple title records
	query = "select a.award_id from awards as a, award_cats as c where c.award_cat_id=a.award_cat_id and \
	         (c.award_cat_name like '%novel%' or c.award_cat_name like '% story%' \
	         or c.award_cat_name like '% book%' or c.award_cat_name like '%collection%' or c.award_cat_name like \
	         '%antholog%' or a.award_title like '%^%') and c.award_cat_name not like '%Traduction%' and \
	         c.award_cat_name not like '%graphic%' and c.award_cat_name not like '%novelist%' and c.award_cat_name \
	         not like '%publisher%' and c.award_cat_name not like '%editor%' and c.award_cat_name not like \
	         '%illustrator%' and a.award_level<100 and not exists(select 1 from title_awards where a.award_id= \
	         title_awards.award_id) and award_author not like '%****%' and award_title!='No Award' and \
	         award_title!='untitled'"
        standardReport(query, 24)

        #   Report 25: Empty Award Types
        query = 'select award_type_id from award_types where NOT EXISTS \
                (select 1 from awards where awards.award_type_id=award_types.award_type_id)'
        standardReport(query, 25)

        #   Report 26: Empty Award categories
        query = 'select award_cat_id from award_cats where NOT EXISTS \
                (select 1 from awards where awards.award_cat_id=award_cats.award_cat_id)'
        standardReport(query, 26)

        #   Report 30: Chapbooks with Mismatched Variant Types
	query = "select t1.title_id from titles t1, titles t2 where t1.title_ttype='CHAPBOOK' \
                and t2.title_parent=t1.title_id and t2.title_ttype!='CHAPBOOK' \
                UNION select t1.title_id from titles t1, titles t2 where t1.title_ttype!='CHAPBOOK' \
                and t2.title_parent=t1.title_id and t2.title_ttype='CHAPBOOK'"
        standardReport(query, 30)

        #   Report 31: Pre-2005 pubs with ISBN-13s and post-2007 pubs with ISBN-10s
	query = """select pub_id from pubs
                where (pub_isbn like '97%'
                and length(replace(pub_isbn,'-',''))=13
                and pub_year<'2005-00-00'
                and pub_year !='0000-00-00')
                or
                (length(replace(pub_isbn,'-',''))=10
                and pub_year>'2008-00-00'
                and pub_year !='8888-00-00'
                and pub_year !='9999-00-00')"""
        standardReport(query, 31)

        #   Report 33: Publication Authors that are not the Title Author
	query = """select distinct p.pub_id
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a
                where pa.pub_id = p.pub_id 
                and pa.author_id = a.author_id 
                and pc.title_id = t.title_id 
                and pc.pub_id = p.pub_id 
                and p.pub_ctype in ('ANTHOLOGY','NOVEL','COLLECTION','NONFICTION','OMNIBUS','CHAPBOOK')
                and t.title_ttype in ('ANTHOLOGY','NOVEL','COLLECTION','OMNIBUS','NONFICTION','CHAPBOOK') 
                and t.title_ttype = p.pub_ctype 
                and not exists (select 1 from canonical_author ca
                where ca.title_id = t.title_id and pa.author_id = ca.author_id)
                UNION
                select distinct p.pub_id
                from pub_authors pa, pubs p, pub_content pc, titles t, authors a
                where pa.pub_id = p.pub_id 
                and pa.author_id = a.author_id 
                and pc.title_id = t.title_id 
                and pc.pub_id = p.pub_id 
                and p.pub_ctype in ('FANZINE','MAGAZINE')
                and t.title_ttype = 'EDITOR'
                and t.title_language != 26
                and not exists (select 1 from canonical_author ca
                where ca.title_id = t.title_id and ca.author_id = pa.author_id)"""
        standardReport(query, 33)

        #   Report 36: Images Which We Don't Have Permission to Link to
	query =  "select pub_id from pubs where pub_frontimage!='' and pub_frontimage is not null "
	domains = RecognizedDomains()
        for domain in domains:
                # Skip domains that are "recognized", but we don't have permission to link to
                if domain[3] == 0:
                        continue
                query += " and pub_frontimage not like '%"
                query += "%s" % domain[0]
                query += "%'"
        query += " order by pub_frontimage"
        standardReport(query, 36)

        #   Report 39: Publications with Bad Ellipses
        query = "select pub_id from pubs where pub_title like '%. . .%'"
        standardReport(query, 39)

        #   Report 41: Reviews not Linked to Titles
        query = """select t1.title_id from titles t1 where title_ttype='REVIEW'
                and not exists (select 1 from title_relationships tr where tr.review_id=t1.title_id)
                and not exists (select 1 from titles t2 where t2.title_parent=t1.title_id)"""
        standardReport(query, 41)

        #   Report 42: Reviews of uncommon title types
        query = "select t1.title_id from titles t1 where t1.title_ttype='REVIEW' and exists \
                (select 1 from title_relationships tr, titles t2 where t1.title_id=tr.review_id \
                and t2.title_id=tr.title_id and t2.title_ttype in \
                ('CHAPBOOK', 'COVERART', 'INTERIORART', 'INTERVIEW', 'REVIEW'))"
        standardReport(query, 42)

        #   Report 44: Similar publishers
        elapsed = elapsedTime()
        standardDelete(44)
        suffixes = ('Inc', 'LLC', 'Books', 'Press', 'Publisher', 'Publishers', 'Publishing')
        separators = (' ', ',', ', ')
        post_suffixes = ('', '.')
        query = """select distinct p1.publisher_id, p2.publisher_id
                from publishers p1, publishers p2 where
                p1.publisher_id != p2.publisher_id
                and p1.publisher_name != p2.publisher_name
                and p1.publisher_name = replace(replace(p2.publisher_name, ' ',''), '/', '')
                UNION
                select distinct p1.publisher_id, p2.publisher_id
                from publishers p1, publishers p2 where
                p1.publisher_id != p2.publisher_id
                and p1.publisher_name != p2.publisher_name 
                and substr(p2.publisher_name,1,4) = 'The '
                and p1.publisher_name=substr(p2.publisher_name,5,999)"""

        for separator in separators:
                for suffix in suffixes:
                        for post_suffix in post_suffixes:
                                full_suffix = separator + suffix + post_suffix
                                query += """ UNION
                                            select distinct p1.publisher_id, p2.publisher_id
                                            from publishers p1, publishers p2
                                            where p1.publisher_id != p2.publisher_id
                                            and p1.publisher_name != p2.publisher_name
                                            and p1.publisher_name = substr(p2.publisher_name,1,length(p2.publisher_name)-%d)
                                            and substr(p2.publisher_name,length(p2.publisher_name)-%d, 999) = '%s'
                                            """ % (len(full_suffix), len(full_suffix)-1, full_suffix)
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        while record:
                publisher_id1 = int(record[0][0])
                publisher_id2 = int(record[0][1])
                query2 = """select 1 from cleanup where report_type=44
                        and ((record_id=%d and record_id_2=%d)
                        or (record_id=%d and record_id_2=%d))
                        """ % (publisher_id1, publisher_id2, publisher_id2, publisher_id1)
                db.query(query2)
                result2 = db.store_result()
                # Only add to the cleanup table if this publisher pair isn't in "cleanup"
                if not result2.num_rows():
                        update = """insert into cleanup (record_id, report_type, record_id_2)
                        values(%d, 44, %d)""" % (publisher_id1, publisher_id2)
                        db.query(update)
                record = result.fetch_row()
        elapsed.print_elapsed(44)

        #   Report 45: Variant Title Type Mismatches
        query = """select v.title_id from titles v, titles p
                where v.title_parent > 0
                and v.title_parent=p.title_id
                and v.title_ttype!=p.title_ttype
                and not (v.title_ttype='SERIAL' and p.title_ttype in ('NOVEL', 'SHORTFICTION', 'COLLECTION'))
                and not (v.title_ttype='INTERIORART' and p.title_ttype='COVERART')
                and not (v.title_ttype='COVERART' and p.title_ttype='INTERIORART')"""
        standardReport(query, 45)

        #   Report 47: Title Dates after Publication Dates
        query = """select distinct t.title_id from titles t, pubs p, pub_content pc
                where pc.title_id = t.title_id
		and pc.pub_id = p.pub_id
                and p.pub_year != '0000-00-00'
                and p.pub_year != '8888-00-00'
		and t.title_copyright != '0000-00-00'
		and t.title_copyright != '0000-00-00'
                and
                (
                        YEAR(t.title_copyright) > YEAR(p.pub_year)
                or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and MONTH(t.title_copyright) > MONTH(p.pub_year)
                        )
		or
                        (
                                YEAR(p.pub_year) = YEAR(t.title_copyright)
                                and MONTH(p.pub_year) = MONTH(t.title_copyright)
                                and MONTH(p.pub_year) != '00'
                                and DAY(p.pub_year) != '00'
				and DAY(t.title_copyright) > DAY(p.pub_year)
                        )
                )
                limit 1000"""
        standardReport(query, 47)

        #   Report 48: Series with Numbering Gaps
        query = "select series_id from titles where series_id IS NOT NULL \
                and title_seriesnum IS NOT NULL and title_seriesnum!=8888 \
                group by series_id having count(title_seriesnum) < \
                (max(title_seriesnum)-min(title_seriesnum)+1) \
                union \
                select s. series_id from series s where not exists \
                        (select 1 from titles t where t.series_id=s.series_id \
                         and t.title_seriesnum=1 \
                ) \
                and exists \
                         (select 1 from titles t where t.series_id=s.series_id \
                         and t.title_seriesnum>1 and t.title_seriesnum<1800 \
                )"
        standardReport(query, 48)

        #   Report 49: Publications with Invalid ISBN Formats
        query = """select p.pub_id from pubs p
                where p.pub_isbn is not NULL
                and p.pub_isbn != ''
                and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{9}[Xx]{1}$'
                and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{10}$'
                and REPLACE(p.pub_isbn,'-','') not REGEXP '^[[:digit:]]{13}$'
                """
        standardReport(query, 49)

        #   Report 50: Publications with Invalid ISBN Checksums
        query = "(select tmp.pub_id from \
                 (select pub_id, REPLACE(pub_isbn,'-','') AS isbn \
                 from pubs \
                 where LENGTH(REPLACE(pub_isbn,'-',''))=10) tmp \
                 where CONVERT((11-MOD( \
        	 (substr(isbn,1,1)*10) \
        	+(substr(isbn,2,1)*9) \
        	+(substr(isbn,3,1)*8) \
        	+(substr(isbn,4,1)*7) \
        	+(substr(isbn,5,1)*6) \
        	+(substr(isbn,6,1)*5) \
        	+(substr(isbn,7,1)*4) \
        	+(substr(isbn,8,1)*3) \
        	+(substr(isbn,9,1)*2) \
        	, 11)),CHAR) \
                 != REPLACE(REPLACE(SUBSTR(tmp.isbn,10,1),0,11),'X',10)) \
                union \
                (select tmp.pub_id from \
                 (select pub_id, REPLACE(pub_isbn,'-','') AS isbn \
                 from pubs \
                 where LENGTH(REPLACE(pub_isbn,'-',''))=13) tmp \
                 where MOD(10-MOD( \
        	 (substr(isbn,1,1)*1) \
        	+(substr(isbn,2,1)*3) \
        	+(substr(isbn,3,1)*1) \
        	+(substr(isbn,4,1)*3) \
        	+(substr(isbn,5,1)*1) \
        	+(substr(isbn,6,1)*3) \
        	+(substr(isbn,7,1)*1) \
        	+(substr(isbn,8,1)*3) \
        	+(substr(isbn,9,1)*1) \
        	+(substr(isbn,10,1)*3) \
        	+(substr(isbn,11,1)*1) \
                +(substr(isbn,12,1)*3) \
        	,10),10) \
                 != SUBSTR(isbn,13,1))"
        standardReport(query, 50)

        #   Report 51: Publications with Identical ISBNs and Different Titles
        # Note that we have to store publication IDs rather than ISBNs in the
        # "cleanup" table because ISBNs can be non-numeric and the record_id
        # column can only store integers
        query = """select record_id from cleanup where
                report_type=51 and resolved IS NOT NULL"""
	db.query(query)
	result = db.store_result()
        resolved_ids = []
        record = result.fetch_row()
        while record:
                resolved_ids.append(str(record[0][0]))
                record = result.fetch_row()
        resolved_string = "','".join(resolved_ids)

        query = """select pub_isbn 
                from pubs 
                where pub_isbn IS NOT NULL 
                and pub_isbn != '' 
                and pub_ctype != 'MAGAZINE' 
		and pub_id not in ('%s')
                group by pub_isbn 
                having count(distinct(REPLACE(pub_title,'-',''))) > 1 
                AND INSTR(MIN(pub_title), MAX(pub_title)) = 0 
                AND INSTR(MAX(pub_title), MIN(pub_title)) = 0""" % resolved_string
	db.query(query)
	result = db.store_result()
        isbns = []
        record = result.fetch_row()
        while record:
                isbns.append(str(record[0][0]))
                record = result.fetch_row()

        # Only run the report if there are matching ISBNs; if the 'isbns; list is empty,
        # then running this report would display thousands of pubs with empty ISBN values
        if isbns:
                isbns_string = "','".join(isbns)
                query = "select distinct pub_id from pubs where pub_isbn in ('%s')" % isbns_string
                standardReport(query, 51)

        #   Report 52: Publications with 0 or 2+ Reference Titles
        only_one = {'ANTHOLOGY': ['ANTHOLOGY'],
                    'COLLECTION': ['COLLECTION'],
                    'CHAPBOOK': ['CHAPBOOK'],
                    'MAGAZINE': ['EDITOR'],
                    'FANZINE': ['EDITOR'],
                    'NONFICTION': ['NONFICTION'],
                    'NOVEL': ['NOVEL'],
                    'OMNIBUS': ['OMNIBUS']}
                      
        query = ""
        for pub_type in only_one:
                if query:
                        query += " UNION "
                query += "(select p.pub_id from pubs p where p.pub_ctype='%s'" % pub_type
                query += " and (select count(*) from pub_content pc, titles t"
                query += " where pc.pub_id=p.pub_id and t.title_id=pc.title_id"
                query += " and "
                subquery = ""
                for title_type in only_one[pub_type]:
                        if subquery:
                                subquery += " or "
                        subquery += "(t.title_ttype='%s')" % title_type
                query += "(" + subquery + "))!=1)"
        standardReport(query, 52)

        #   Report 57: Invalid SFE image links
        query = """select pub_id from pubs where
                   pub_frontimage like '%sf-encyclopedia.uk%'
                   and pub_frontimage not like '%/clute/%'
                   and pub_frontimage not like '%/langford/%'
                   and pub_frontimage not like '%/robinson/%'"""
        standardReport(query, 57)

        # Excluded authors are 'uncredited', 'unknown', 'various' and 'The Readers'
        excluded_authors = '2862, 20754, 7311, 25179'
        #   Report 58: Suspected Dutch Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 16
                 )>0""" % excluded_authors
        standardReport(query, 58)

        #   Report 59: Suspected French Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 22
                 )>0""" % excluded_authors
        standardReport(query, 59)

        #   Report 60: Suspected German Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language = 26
                 )>0""" % excluded_authors
        standardReport(query, 60)

        #   Report 61: Suspected Other Non-English Authors without a Language Code
        query = """select a.author_id from authors a where a.author_language is null
                   and a.author_id not in (%s)
                and (
                 select count(t.title_id) from titles t, canonical_author ca
                 where a.author_id = ca.author_id
                 and ca.title_id = t.title_id
                 and ca.ca_status = 1
                 and t.title_language is not null
                 and t.title_language not in (16,17,22,26)
                 )>0""" % excluded_authors
        standardReport(query, 61)

        #   Report 63: Non-genre/genre VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_non_genre != t2.title_non_genre
                """
        standardReport(query, 63)

        #   Report 64: Series with a mix of EDITOR and non-EDITOR titles
        query = """select s.series_id from series s
                 where exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype = 'EDITOR')
                 and exists(select 1 from titles t where t.series_id = s.series_id and t.title_ttype != 'EDITOR')"""
        standardReport(query, 64)

        #   Reports 65-70: Publishers, pub series, series, authors, titles
        #                  pubs with invalid Unicode characters
        badUnicodeReport('publishers', 'publisher_name', 'publisher_id', 65)
        badUnicodeReport('pub_series', 'pub_series_name', 'pub_series_id', 66)
        badUnicodeReport('series', 'series_title', 'series_id', 67)
        badUnicodeReport('authors', 'author_canonical', 'author_id', 68)
        badUnicodeReport('titles', 'title_title', 'title_id', 69)
        badUnicodeReport('pubs', 'pub_title', 'pub_id', 70)

        #   Report 71: Forthcoming Titles: 9999-00-00 and more than 3 months out
        query = """select title_id from titles where title_copyright >
                DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and title_copyright != '8888-00-00'"""
        standardReport(query, 71)

        #   Report 72: Forthcoming (9999-00-00) Publications
        query = """select pub_id from pubs where pub_year >
                DATE_ADD(NOW(), INTERVAL 3 MONTH)
                and pub_year != '8888-00-00'"""
        standardReport(query, 72)

        #   Report 73: Publishers with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('publisher_name')
        query = """select publisher_id from publishers where %s""" % pattern_match
        standardReport(query, 73)

        #   Report 74: Titles with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('title_title')
        query = """select title_id from titles where %s""" % pattern_match
        standardReport(query, 74)

        #   Report 75: Publications with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('pub_title')
        query = """select pub_id from pubs where %s""" % pattern_match
        standardReport(query, 75)

        #   Report 76: Series with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('series_title')
        query = """select series_id from series where %s""" % pattern_match
        standardReport(query, 76)

        #   Report 77: Publication Series with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('pub_series_name')
        query = """select pub_series_id from pub_series where %s""" % pattern_match
        standardReport(query, 77)

        #   Report 78: Authors with Suspect Unicode Characters
        pattern_match = suspectUnicodePatternMatch('author_canonical')
        query = """select author_id from authors where %s""" % pattern_match
        standardReport(query, 78)

        #   Report 79: NOVEL publications with fewer than 80 pages
        query = """select pub_id from pubs
                where
                (
                  (REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(pub_pages,'[',''),']',''),'+',''),'v',''),'i',''),'x','') < 80
                  and pub_pages!='' and pub_pages!='0'
                  and pub_pages not like '%+%')
                or
                  (pub_pages like '%+%' and pub_pages not REGEXP '[[:digit:]]{3}')
                )
                and pub_ctype='NOVEL'"""
        standardReport(query, 79)

        #   Report 81: Series with Slashes and no Spaces
        query = """select series_id from series
                where series_title like '%/%'
                and series_title not like '% / %'"""
        standardReport(query, 81)

        #   Report 82: Invalid Record URLs in Notes
        query = """select note_id, note_note from notes
                where note_note like '%isfdb.org%'"""
	db.query(query)
	result = db.store_result()
        problems = []
        notes = {}
        pub_tag_notes = {}
        ignored_scripts = ('se', 'note')
        scripts = {'title': ('titles', 'title_id'),
                   'pl': ('pubs', 'pub_id'),
                   'ea': ('authors', 'author_id'),
                   'publisher': ('publishers', 'publisher_id'),
                   'pubseries': ('pub_series', 'pub_series_id'),
                   'pe': ('series', 'series_id'),
                   'seriesgrid': ('series', 'series_id'),
                   'ay': ('award_types', 'award_type_id'),
                   'awardtype': ('award_types', 'award_type_id'),
                   'award_details': ('awards', 'award_id'),
                   'award_category': ('award_cats', 'award_cat_id'),
                   'publisheryear': ('publishers', 'publisher_id')
                   }
        for script in scripts:
                notes[script] = {}
        pub_tag_notes[script] = {}
        record = result.fetch_row()
        while record:
                note_id = record[0][0]
                note_body = record[0][1].lower()
                link_list = note_body.split("isfdb.org/cgi-bin/")
                for link in link_list:
                        if ".cgi?" not in link:
                                continue
                        split_link = link.split('.cgi?')
                        if len(split_link) != 2:
                                continue
                        script = split_link[0]
                        if script in ignored_scripts:
                                continue
                        record_id = split_link[1]
                        # If the record ID is followed by a double quote, strip everything to the right of the ID
                        if '"' in record_id:
                                record_id = record_id.split('"')[0]
                        # If the record ID is followed by a single quote, strip everything to the right of the ID
                        if "'" in record_id:
                                record_id = record_id.split("'")[0]
                        # If the record ID is followed by a plus sign, strip everything to the right of the ID
                        if '+' in record_id:
                                record_id = record_id.split('+')[0]
                        # If the script is not one of the recognized script types, report it
                        if script not in scripts:
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # For numeric record IDs, add them to the main record list and continue the loop
                        if record_id.isdigit():
                                if record_id not in notes[script]:
                                        notes[script][record_id] = []
                                notes[script][record_id].append(note_id)
                                continue
                        # If the record ID is not numeric and it's not a Publication record, it is bad
                        if script != 'pl':
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # For publication records, record IDs may also be alphanumeric tags, but
                        # if the string contains punctuation, then it is not a valid ID or tag
                        if not record_id.isalnum():
                                if note_id not in problems:
                                        problems.append(note_id)
                                continue
                        # Otherwise this is a publication tag, so we add it to a special list of tag notes
                        if record_id not in pub_tag_notes:
                                pub_tag_notes[record_id] = []
                        pub_tag_notes[record_id].append(note_id)
                        
                record = result.fetch_row()
        
        for script in notes:
                if notes[script]:
                        in_clause = ''
                        for record_id in notes[script]:
                                if in_clause:
                                        in_clause += ", "
                                in_clause += "'%s'" % str(record_id)
                        table_name = scripts[script][0]
                        field_name = scripts[script][1]
                        query = """select %s from %s where %s in (%s)""" % (field_name, table_name, field_name, in_clause)
                        db.query(query)
                        result = db.store_result()
                        record = result.fetch_row()
                        while record:
                                existing_id = str(record[0][0])
                                del notes[script][existing_id]
                                record = result.fetch_row()
                        for record_id in notes[script]:
                                for note_id in notes[script][record_id]:
                                        if note_id not in problems:
                                                problems.append(note_id)

        if pub_tag_notes:
                in_clause = ''
                for record_id in pub_tag_notes:
                        if in_clause:
                                in_clause += ", "
                        in_clause += "'%s'" % str(record_id)
                query = """select pub_tag from pubs where pub_tag in (%s)""" % in_clause
                db.query(query)
                result = db.store_result()
                record = result.fetch_row()
                while record:
                        existing_tag = record[0][0].lower()
                        del pub_tag_notes[existing_tag]
                        record = result.fetch_row()
                for record_id in pub_tag_notes:
                        for note_id in pub_tag_notes[record_id]:
                                if note_id not in problems:
                                        problems.append(note_id)

        in_clause = ''
        for problem in problems:
                if in_clause:
                        in_clause += ", "
                in_clause += str(problem)
        if in_clause:
                query = "select note_id from notes where note_id in (%s)" % in_clause
                standardReport(query, 82)

        #   Report 83: Serials without parenthetical disambiguations
        query = """select title_id from titles where
                (title_title not like '%(Complete Novel)')
                and (title_title not like '%(Part % of %)')
                and title_ttype='SERIAL'"""
        standardReport(query, 83)

        #   Report 84: Serials with Potentially Unnecessary Disambiguation
        query = """select x.title_id
                from (
                select min(t.title_id) as "title_id",
                substring(t.title_title,1,LOCATE("(", t.title_title)), count(*)
                from titles t
                where t.title_ttype = 'SERIAL'
                and t.title_title like '%(Part % of %)'
                group by substring(t.title_title,1,LOCATE("(", t.title_title))
                having count(*) = 1
                ) x"""
        standardReport(query, 84)

        #   Report 86: Primary-verified pubs with "unknown" format
        query = """select distinct p.pub_id
                from pubs p, primary_verifications pv
                where p.pub_id = pv.pub_id 
                and p.pub_ptype = 'unknown'"""
        standardReport(query, 86)

        #   Report 87: Author/title language mismatches
        query = """select distinct t.title_id from titles t,
                canonical_author ca, authors a
                where t.title_id=ca.title_id
                and ca.author_id=a.author_id
                and ca.ca_status=1
                and t.title_parent=0
                and t.title_language is not null
                and a.author_language is not null
                and t.title_language != a.author_language
                and a.author_canonical not in ('uncredited', 'unknown')
                and t.title_ttype in ('NOVEL', 'EDITOR', 'NONFICTION', 'SHORTFICTION')
                """
        standardReport(query, 87)

        #   Report 88: Pubs with multiple COVERART titles
        query = """select p.pub_id from pubs p,
                (select pc.pub_id, count(*) from titles t, pub_content pc
                where t.title_id = pc.title_id and t.title_ttype='COVERART'
                group by pc.pub_id having count(*) > 1) x
                where p.pub_id = x.pub_id"""
        standardReport(query, 88)

        #   Report 89: Authors with Invalid Birthplaces
        query = """select author_id from authors
                where
                (author_birthplace like '%, US')
                or
                  (author_birthplace like "%England%"
                  and author_birthplace not like "%Kingdom of England"
                  and author_birthplace not like "%England, Kingdom of Great Britain"
                  and author_birthplace not like "%England, UK")
                or
                  (author_birthplace like "%Scotland%"
                  and author_birthplace not like "%Kingdom of Scotland"
                  and author_birthplace not like "%Scotland, Kingdom of Great Britain"
                  and author_birthplace not like "%Scotland, UK")
                or
                  (YEAR(author_birthdate) <1801 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, UK')
                or (author_birthplace like '%United Kingdom')
                or (author_birthplace like '%Alabama%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Alaska%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Arizona%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Arkansas%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%California%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Baja California%')
                or (author_birthplace like '%Colorado%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Connecticut%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Delaware%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Florida%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Georgia%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%USSR' and author_birthplace not like '%Russia%')
                or (author_birthplace like '%Hawaii%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Kingdom of Hawaii')
                or (author_birthplace like '%Idaho%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Illinois%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Indiana%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Iowa%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Kansas%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Kentucky%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Louisiana%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Maine%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Maine-et-Loire%'
                    and author_birthplace not like '%Domaine de la Devi%'
                    and author_birthplace not like '%Castlemaine%')
                or (author_birthplace like '%Maryland%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Massachusetts%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%British Empire')
                or (author_birthplace like '%Michigan%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Minnesota%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Mississippi%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Missouri%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Montana%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%Bulgaria')
                or (author_birthplace like '%Nebraska%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Nevada%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%New Hampshire%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%New Jersey%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%New Mexico%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%New York%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%British Empire')
                or (author_birthplace like '%North Carolina%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%North Dakota%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Ohio%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Oklahoma%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Oregon%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Pennsylvania%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%British Empire')
                or (author_birthplace like '%Rhode Island%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%South Carolina%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%South Dakota%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Tennessee%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Texas%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Utah%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Vermont%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Virginia%' and author_birthplace not like '%, USA'
                    and author_birthplace not like '%British Empire')
                or (author_birthplace like '%Washington%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%West Virginia%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Wisconsin%' and author_birthplace not like '%, USA')
                or (author_birthplace like '%Wyoming%' and author_birthplace not like '%, USA')
                or
                  (YEAR(author_birthdate) < 1917 and YEAR(author_birthdate) != '0000'
                  and
                    (author_birthplace like '%, Russia%'
                    or
                    author_birthplace like '%, Ukraine%')
                  and author_birthplace not like '%Russian Empire')
                or
                  (YEAR(author_birthdate) > 1922 and YEAR(author_birthdate) < 1992
                  and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, Russia%'
                  and author_birthplace not like '%, USSR')
                or
                  (YEAR(author_birthdate) < 1923 and YEAR(author_birthdate) != '0000'
                  and author_birthplace like '%, USSR')
                or
                  (YEAR(author_birthdate) > 1991 and author_birthplace like '%, USSR')
                or
                  (author_birthplace like '%Russian Federation%')
                """
        standardReport(query, 89)

        #   Report 90: Duplicate sub-series numbers within a series
        query = """select series_id from series
                where series_parent_position is not null
                group by series_parent, series_parent_position
                having count(*) >1
                """
        standardReport(query, 90)

        #   Report 91: Non-Art Titles by Non-English Authors without a Language
        query = """select distinct t.title_id from authors a, titles t, canonical_author ca
                   where a.author_language != 17
                   and a.author_language is not null
                   and a.author_id = ca.author_id
                   and ca.title_id = t.title_id
                   and ca.ca_status = 1
                   and t.title_ttype not in ('COVERART', 'INTERIORART')
                   and t.title_language is null
                """
        standardReport(query, 91)

        #   Report 93: Publication Title/Reference Title Mismatches
        query = """select p.pub_id from pubs p
          where p.pub_ctype in ('CHAPBOOK', 'OMNIBUS', 'ANTHOLOGY', 'COLLECTION', 'NONFICTION', 'NOVEL')
          and not exists
           (select 1 from titles t, pub_content pc
           where p.pub_id = pc.pub_id
           and pc.title_id = t.title_id
           and t.title_ttype = p.pub_ctype
           and (
                (
                REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(p.pub_title,',',''),".",''),":",''),";",''),"-",''),' ',''),"\\\\",'')
                LIKE CONCAT('%', 
                 REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(t.title_title,',',''),".",''),":",''),";",''),"-",''),' ',''),"\\\\",''),
                '%')
                )
            or
                (
                REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(t.title_title,',',''),".",''),":",''),";",''),"-",''),' ',''),"\\\\",'')
                LIKE CONCAT('%',
                 REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(p.pub_title,',',''),".",''),":",''),";",''),"-",''),' ',''),"\\\\",''),
                '%')
                )
            )
           )"""
        standardReport(query, 93)

        #   Report 96: COVERART titles with a "Cover:" prefix
        query = """select title_id from titles
                   where title_ttype = 'COVERART'
                   and title_title like 'Cover:%'
                   UNION
                   select tt.title_id from trans_titles tt, titles t
                   where trans_title_title like 'Cover:%'
                   and tt.title_id = t.title_id
                   and t.title_ttype = 'COVERART'"""
        standardReport(query, 96)

        #   Report 100: Invalid prices
        query = """select pub_id from pubs
                where pub_price like '%$ %'
                or pub_price like concat('%',CHAR(0xA3),' ','%')
                or pub_price like concat('%',CHAR(0xA5),' ','%')
                or pub_price like concat('%',CHAR(0x80),'%',' ','%')
                or pub_price like concat('%','_',CHAR(0x80),'%')
                or pub_price like concat('%',CHAR(0x80),'%',',','%')
                or pub_price like '%CDN%'
                or pub_price like '%EUR%'
                or (pub_price like '$%,%' and pub_price not like '$%.%')
                or (pub_price like 'C$%,%' and pub_price not like 'C$%.%')
                or (pub_price like concat(CHAR(0xA3),'%',',','%') and pub_price not like concat(CHAR(0xA3),'%',".",'%'))
                or pub_price regexp '^[[:digit:]]{1,}[,.]{0,}[[:digit:]]{0,}$'
                or (pub_price regexp '[.]{1}[[:digit:]]{3,}' and pub_price not like 'BD %')
                or (pub_price regexp '^[[:digit:]]{1,}' and pub_price not like '%/%')
                or pub_price regexp '[[:digit:]]{4,}$'
                or pub_price like 'http%'
                or pub_price like '%&#20870;%'
                or pub_price like '%JP%'
                or pub_price like '% % %'
                or pub_price like '% $%'
                or pub_price like '%+%'
                or pub_price regexp '[[:digit:]]{1,} '
                """
        standardReport(query, 100)

        #   Report 144: Series names potentially in need of disambiguation
        query = """select distinct s1.series_id
                   from series s1, series s2
                   where s1.series_id != s2.series_id
                   and s1.series_title = substring(s2.series_title, 1, LOCATE(' (', s2.series_title)-1)
                   and (
                           (s1.series_parent is not null and s1.series_parent != s2.series_id)
                           or (s2.series_parent is not null and s2.series_parent != s1.series_id)
                           or (s1.series_parent is null and s2.series_parent is null)
                        )
                   """
        standardReport(query, 144)

        #   Report 189: Publication series names potentially in need of disambiguation
        query = """select distinct ps1.pub_series_id from pub_series ps1, pub_series ps2
                   where ps1.pub_series_id != ps2.pub_series_id
                   and ps1.pub_series_name = substring(ps2.pub_series_name, 1, LOCATE(' (', ps2.pub_series_name)-1)
                   """
        standardReport(query, 189)

        #   Report 190: Awards with Invalid IMDB Links
        query = """select award_id from awards
                   where award_movie is not NULL
                   and award_movie != ''
                   and SUBSTRING(award_movie, 1, 2) != 'tt'
                   """
        standardReport(query, 190)

        #   Report 191: Invalid hrefs in notes
        query = """select note_id from notes
                where REPLACE(note_note, ' ', '') like '%<ahref=""%'
                or REPLACE(note_note, ' ', '') regexp 'ahref=http'
                or REPLACE(note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}>'
                or REPLACE(note_note, ' ', '') regexp 'ahref="http{1}[^\"\>]{1,}"">'"""
        standardReport(query, 191)

        #   Report 192: Authors without a Working Language
        query = """select author_id from authors
                   where author_language is null
                   and substring(author_lastname,1,1) > 'V'
                """
        standardReport(query, 192)

        #   Report 193: Multilingual publications
        query = """select p.pub_id from pubs p, (
                   select distinct pc.pub_id, t.title_language
                   from titles t, pub_content pc
                   where pc.title_id = t.title_id
                   and t.title_language is not null
                   and t.title_language != ''
                   ) x
                   where p.pub_id = x.pub_id
                   group by p.pub_id
                   having count(*) > 1
                   """
        standardReport(query, 193)

        #   Report 194: Titles without a language
        query = "select title_id from titles where title_language is null"
        standardReport(query, 194)

        #   Report 195: Invalid Title Content values
        query = """select title_id from titles
                   where (title_ttype != 'OMNIBUS' and title_content is not null)
                   or SUBSTRING(title_content,1,1) = '/'
                """
        standardReport(query, 195)

        #   Report 196: Juvenile VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_jvn != t2.title_jvn
                """
        standardReport(query, 196)

        #   Report 197: Novelization VT mismatches
        query = """select distinct t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_nvz != t2.title_nvz
                """
        standardReport(query, 197)

        #   Report 198: Author-pseudonym language mismatches
        query = """select distinct a2.author_id
                from authors a1, authors a2, pseudonyms p
                where a1.author_id = p.author_id
                and p.pseudonym = a2.author_id
                and (
        		(a1.author_language != a2.author_language)
        		or (a1.author_language is NULL and a2.author_language is not null)
        		or (a1.author_language is not NULL and a2.author_language is null)
                )
                """
        standardReport(query, 198)

        #   Report 218: Publications with ASINs in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like binary '%ASIN%'"""
        standardReport(query, 218)

        #   Report 219: Publications with .bl. (British Library) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.bl.%'"""
        standardReport(query, 219)

        #   Report 220: Publications with .sfbg.us (SFBG) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.sfbg.us%'"""
        standardReport(query, 220)

        #   Report 221: Publications with d-nb.info (direct Deutsche Nationalbibliothek links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%/d-nb.info/%'
                 order by p.pub_title"""
        standardReport(query, 221)

        #   Report 222: Publications with .fantlab.ru (FantLab) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%fantlab.ru/%'"""
        standardReport(query, 222)

        #   Report 223: Publications with .amazon.%dp (direct Amazon links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%.amazon.%dp%'"""
        standardReport(query, 223)

        #   Report 224: Publications with .bnf.fr (BNF) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%catalogue.bnf.fr%'"""
        standardReport(query, 224)

        #   Report 225: Publications with lccn.loc (direct Library of Congress links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%lccn.loc%'"""
        standardReport(query, 225)

        #   Report 226: Publications with worldcat.org (direct OCLC/WorldCat links) in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%worldcat.org/%'
                 order by p.pub_title"""
        standardReport(query, 226)

        #   Report 227: Titles with mismatched parentheses
        query = """select title_id,
                LENGTH(REPLACE(title_title, ')', '')) - LENGTH(REPLACE(title_title, '(', '')) as cnt
                from titles having cnt != 0"""
        standardReport(query, 227)

        #   Report 228: E-books without ASINs
        # Ignore Project Gutenberg publications
        query = """select p.pub_id from pubs p, publishers pb
                where p.pub_isbn is null
                and p.publisher_id = pb.publisher_id
                and pb.publisher_name not like '%Project Gutenberg%'
                and p.pub_ptype = 'ebook'
                and p.pub_ctype not in ('FANZINE','MAGAZINE')
                and not exists(
                         select 1 from identifiers
                         where identifier_type_id = 1 and pub_id = p.pub_id)"""
        standardReport(query, 228)

        #   Report 230: Mismatched OCLC URLs in Publication Notes
        query = """select p.pub_id, n.note_note from notes n, pubs p
                where p.note_id = n.note_id and n.note_note regexp
                '<a href=\"https:\/\/www.worldcat.org\/oclc\/[[:digit:]]{1,11}"\>[[:digit:]]{1,11}\<\/a>'"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        pubs = []
        while record:
                pub_id = int(record[0][0])
                note_note = record[0][1]
                record = result.fetch_row()
                two_numbers = note_note.lower().split('/oclc/')[1].split('</a>')[0]
                number_list = two_numbers.split('">')
                if number_list[0] != number_list[1]:
                        pubs.append(pub_id)
        if pubs:
                in_clause = list_to_in_clause(pubs)
                query = "select pub_id from pubs where pub_id in (%s)" % in_clause
                standardReport(query, 230)

        #   Report 231: Missing Required Web Pages for Cover Images
        query = "select pub_id from pubs where pub_frontimage not like '%|%' and ("
        for domain in domains:
                if len(domain) > 5 and domain[5]:
                        query += "pub_frontimage like '%%%s/%%' or " % domain[0]
        query = '%s)' % query [:-4]
        standardReport(query, 231)

        #   Report 232: Award Years with Month/Day Data
        query = "select award_id from awards where award_year not like '%-00-00'"
        standardReport(query, 232)

        #   Report 233: Potential Duplicate E-book Publications
        query = """select distinct p1.pub_id
                   from titles t, pub_content pc1, pub_content pc2, pubs p1, pubs p2
                   where t.title_id = pc1.title_id
                   and pc1.pubc_id != pc2.pubc_id
                   and pc1.pub_id = p1.pub_id
                   and p1.pub_ptype = 'ebook'
                   and t.title_id = pc2.title_id
                   and p2.pub_ptype = 'ebook'
                   and pc2.pub_id = p2.pub_id
                   and YEAR(p1.pub_year) = YEAR(p2.pub_year)
                   and MONTH(p1.pub_year) = MONTH(p2.pub_year)
                   and (p1.pub_isbn is null or p2.pub_isbn is null or p1.pub_isbn = p2.pub_isbn)
                   and not (p1.pub_catalog is not null and p2.pub_catalog is not null and p1.pub_catalog != p2.pub_catalog)
                   and p1.pub_ctype = p2.pub_ctype
                   and p1.pub_title = p2.pub_title
                   group by t.title_id"""
        standardReport(query, 233)

        #   Report 234: Publications with direct De Nederlandse Bibliografie links in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%picarta.pica.nl/%'"""
        standardReport(query, 234)

        #   Report 235: Publications with invalid BNF identifiers
        query = """select distinct p.pub_id from pubs p, identifiers i
                 where p.pub_id = i.pub_id
                 and i.identifier_type_id = 4
                 and i.identifier_value not regexp '^cb[[:digit:]]{8}[[:alnum:]]{1}$'"""
        standardReport(query, 235)

        #   Report 236: SFBC publications with an ISBN and no catalog ID
        query = """select distinct p.pub_id from pubs p, publishers pu
                 where p.publisher_id = pu.publisher_id
                 and (pu.publisher_name like '%SFBC%'
                      or pu.publisher_name = 'Science Fiction Book Club')
                 and p.pub_isbn is not NULL and p.pub_isbn != ""
                 and p.pub_catalog is NULL"""
        standardReport(query, 236)

        #   Report 237: Pubs with non-template LCCNs in notes
        query = """select p.pub_id from
                (select note_id from notes
                where note_note like '%LCCN:%'
                or note_note regexp 'LCCN [[:digit:]]{1}')
                as n, pubs p
                where p.note_id = n.note_id"""
        standardReport(query, 237)

        #   Report 242: CHAPBOOK/SHORTFICTION Juvenile Flag Mismatches
        query = """select distinct t1.title_id
                from titles t1, titles t2, pub_content pc1, pub_content pc2
                where t1.title_id = pc1.title_id
                and pc1.pub_id = pc2.pub_id
                and pc2.title_id = t2.title_id
                and t1.title_ttype = 'CHAPBOOK'
                and t2.title_ttype = 'SHORTFICTION'
                and t1.title_jvn != t2.title_jvn"""
        standardReport(query, 242)

        #   Report 243: Publication Images with Extra Formatting in Amazon URLs
        query = """select pub_id from pubs
                where pub_frontimage like '%amazon.com/%'
                and not
                (REPLACE(pub_frontimage,'%2B','+') REGEXP '/images/[PIG]/[0-9A-Za-z+-]{10}[LS]?(\._CR[0-9]+,[0-9]+,[0-9]+,[0-9]+)?\.(gif|png|jpg)$'
                or
                pub_frontimage REGEXP '\.images(\-|\.)amazon\.com/images/G/0[1-3]/ciu/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{22,24}\.L\.(gif|png|jpg)$'
                or
                pub_frontimage REGEXP '\.ssl-images-amazon\.com/images/S/amzn-author-media-prod/[0-9a-z]{26}\.(gif|png|jpg)$')
                """
        standardReport(query, 243)

        #   Report 244: Publications with Invalid Non-numeric External IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and
                (
                (it.identifier_type_name in
                ('Biblioman', 'BL', 'Bleiler Early Years', 'Bleiler Gernsback',
                'COBISS.BG', 'COBISS.SR', 'COPAC (defunct)', 'FantLab',
                'Goodreads', 'JNB/JPNO', 'KBR', 'Libris', 'LTF', 'NILF', 'NLA',
                'OCLC/WorldCat', 'PORBASE', 'SF-Leihbuch')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('DNB', 'PPN')
                and i.identifier_value not regexp '^[[:digit:]]{1,30}[Xx]{0,1}$')
                or
                (it.identifier_type_name = 'NDL'
                and i.identifier_value not regexp '^[b]{0,1}[[:digit:]]{1,30}$')
                or
                (it.identifier_type_name in ('Reginald-1', 'Reginald-3', 'Bleiler Supernatural')
                and i.identifier_value not regexp '^[[:digit:]]{1,6}[[:alpha:]]{0,1}$')
                or
                (it.identifier_type_name = 'NooSFere'
                and i.identifier_value not regexp '^[-]{0,1}[[:digit:]]{1,30}$')
                )
                """
        standardReport(query, 244)

        #   Report 245: Publications with non-standard ASINs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and (
                        (
                                it.identifier_type_name = 'ASIN'
                                and i.identifier_value not like 'B%'
                        )
                        or (
                                it.identifier_type_name = 'Audible-ASIN'
                                and i.identifier_value not like 'B%'
                                and i.identifier_value not regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                )
                """
        standardReport(query, 245)

        #   Report 246: Publications with non-standard Barnes & Noble IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BN'
                and i.identifier_value not like '294%'"""
        standardReport(query, 246)

        #   Report 247: Publications with Non-Standard LCCNs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'LCCN'
                and replace(i.identifier_value,'-','') not regexp '^[[:digit:]]{1,30}$'"""
        standardReport(query, 247)

        #   Report 248: Publications with Invalid Open Library IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Open Library'
                and i.identifier_value not like 'O%'"""
        standardReport(query, 248)

        #   Report 249: Publications with Invalid BNB IDs
        query = """select distinct p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'BNB'
                and i.identifier_value like 'BLL%'"""
        standardReport(query, 249)

        #   Report 250: Publications with OCLC IDs matching ISBNs
        # Note that the query currently uses idenitifier type IDs instead of
        # idenitifier type names in order to avoid a costly join
        query = """select distinct p.pub_id
                from pubs p, identifiers i
                where p.pub_id = i.pub_id
                and i.identifier_type_id = 12
                and replace(i.identifier_value,'-','') = replace(p.pub_isbn,'-','')"""
        standardReport(query, 250)

        #   Report 251: Publications with an OCLC Verification, no ISBN and no OCLC External ID
        query = """select distinct p.pub_id
            from pubs p, verification v, reference r
            where p.pub_id = v.pub_id
            and (p.pub_isbn is null or p.pub_isbn='')
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')"""
        standardReport(query, 251)

        #   Report 252: Publications with an OCLC Verification, no ISBN and no OCLC External ID
        query = """select distinct p.pub_id
            from pubs p, verification v, reference r
            where p.pub_id = v.pub_id
            and p.pub_isbn is not null
            and p.pub_isbn!=''
            and v.reference_id = r.reference_id
            and r.reference_label = 'OCLC/Worldcat'
            and v.ver_status = 1
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'OCLC/WorldCat')
            order by p.pub_title
            limit 1000"""
        standardReport(query, 252)

        #   Report 253: Pubs non-linking External IDs in Notes
        query = """select p.pub_id from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_id in (select distinct note_id from notes
                where note_note like '%{{BREAK}}%Reginald1%'
                or note_note like '%{{BREAK}}%Reginald3%'
                or note_note like '%{{BREAK}}%Bleiler%Early Years%'
                or note_note like '%{{BREAK}}%Bleiler%Gernsback%'
                or note_note like '%{{BREAK}}%Bleiler%Guide to Supernatural%')"""
        standardReport(query, 253)

        #   Report 254: Publications with www.noosfere.org in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%www.noosfere.org%'"""
        standardReport(query, 254)

        #   Report 255: Publications with nilf.it in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%nilf.it/%'"""
        standardReport(query, 255)

        #   Report 256: Publications with fantascienza.com/catalogo in Notes
        query = """select p.pub_id from notes n, pubs p
                 where p.note_id = n.note_id
                 and n.note_note like '%fantascienza.com/catalogo%'"""
        standardReport(query, 256)

        #   Report 272: Publications with incomplete contents and no Incomplete template
        query = """select p.pub_id from pubs p,
                (select n.note_id from notes n
                where note_note not like '%{{Incomplete}}%' and
                (note_note like '%not complete%'
                or note_note like '%incomplete%'
                or note_note like '%partial content%'
                or note_note like '%partial data%'
                or note_note like '%to be entered%'
                or note_note like '%to be added%'
                or note_note like '%more%added%'
                or note_note like '%not entered yet%')
                ) x
                where p.note_id = x.note_id
                """
        standardReport(query, 272)

        #   Report 273: Mismatched Braces
        query = """select note_id, LENGTH(note_note) - LENGTH(REPLACE(note_note, '{', '')) openbraces,
                LENGTH(note_note) - LENGTH(REPLACE(note_note, '}', '')) closebraces
                from notes having openbraces != closebraces"""
        standardReport(query, 273)

        #   Report 274: References to Non-Existent Templates
        query = "select note_id from notes where "
        replace_string = "REPLACE(lower(note_note), '{{break', '')"
        for template in ISFDBTemplates():
                query += "REPLACE("
                replace_string += ", '{{%s', '')" % template.lower()
        query += "%s like '%%{{%%'" % replace_string
        standardReport(query, 274)

        #   Report 275: Title Dates Before First Publication Dates
        query = """select t1.title_id from titles t1
                where t1.title_ttype in ('ANTHOLOGY', 'CHAPBOOK', 'COLLECTION', 'COVERART', 'OMNIBUS', 'SERIAL')
		and t1.title_parent > 0
                and YEAR(t1.title_copyright) <
                (select YEAR(min(p.pub_year))
                from pubs p, pub_content pc
                where pc.pub_id = p.pub_id
                and pc.title_id = t1.title_id)
                limit 1000"""
        standardReport(query, 275)

        #   Report 276: Variant Title Dates Before Canonical Title Dates
        query = """select t1.title_id from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and t1.title_copyright < t2.title_copyright
                and t1.title_copyright != '0000-00-00'
                and t2.title_copyright != '0000-00-00'
                and month(t1.title_copyright) != '00'
                and month(t2.title_copyright) != '00'
                and t1.title_ttype != 'SERIAL'"""
        standardReport(query, 276)

        #   Report 277: Publications with the 'Incomplete' Template in Notes
        elapsed = elapsedTime()
        standardDelete(277)
        query = """select p.pub_id,
                IF(p.pub_year='0000-00-00', 0, REPLACE(SUBSTR(p.pub_year, 1,7),'-',''))
                from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_note like '%{{Incomplete}}%'
                """
        db.query(query)
        result = db.store_result()
        containers = {}
        record = result.fetch_row()
        while record:
                pub_id = record[0][0]
                pub_month = record[0][1]
                containers[pub_id] = pub_month
                record = result.fetch_row()
        # Insert the new pub IDs and their months into the cleanup table
        for pub_id in containers:
                update = "insert into cleanup (record_id, report_type, record_id_2) values(%d, 277, %d)" % (int(pub_id), int(containers[pub_id]))
                db.query(update)
        elapsed.print_elapsed(277)

        #   Report 286: Variant Title Length Mismatches
        query = """select distinct t1.title_id
                from titles t1, titles t2
                where t1.title_parent = t2.title_id
                and (
                        (t1.title_storylen != t2.title_storylen)
                        or
                        (t1.title_storylen is not NULL and t2.title_storylen is NULL)
                )
                limit 1000
                """
        standardReport(query, 286)

        #   Report 287: Publications with Invalid Page Numbers
        query = """select distinct pub_id
                from pub_content
                where pubc_page like '%del%'
                or pubc_page like '%&#448;%'"""
        standardReport(query, 287)

        #   Report 288: Publications with an Invalid Page Count
        query = """select distinct pub_id from pubs
                where pub_pages REGEXP '[^\]\[0-9ivxlcdm+ ,]'"""
        standardReport(query, 288)

        #   Report 289: CHAPBOOKs with Multiple Fiction Titles
        query = """select distinct p.pub_id
                from pubs p
                where p.pub_ctype='CHAPBOOK'
                and
                        (select count(t.title_id)
                        from pub_content pc, titles t
                        where p.pub_id = pc.pub_id
                        and pc.title_id = t.title_id
                        and t.title_ttype in ('SHORTFICTION', 'POEM', 'SERIAL'))
                > 1"""
        standardReport(query, 289)

        #   Report 290: Suspected Ineligible Reviewed NONFICTION Titles (first 1000)
        query = """select distinct t1.title_id
        	from titles t1, title_relationships tr, titles t2, pubs p, pub_content pc
        	where t1.title_ttype = 'NONFICTION'
        	and t1.title_id = tr.title_id
        	and t2.title_id = tr.review_id
        	and t2.title_ttype = 'REVIEW'
        	and t1.title_id = pc.title_id
        	and p.pub_id = pc.pub_id
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 290
                        and c.record_id = t1.title_id
                        and c.resolved is not NULL
                        )
        	limit 1000"""
        standardReport(query, 290)

        #   Report 291: Suspected Invalid Uses of the Narrator Template
        query = """select distinct p.pub_id
                from pubs p, notes n
                where p.note_id = n.note_id
                and note_note like '%{{narrator%'
                and p.pub_ptype not like '%audio%'"""
        standardReport(query, 291)

        #   Report 292: Audio Books without the Narrator Template
        query = """select distinct p.pub_id
                from pubs p, notes n
                where p.pub_ptype like '%audio%'
                and p.note_id = n.note_id
                and n.note_note not like '%{{narrator%'
                limit 1000"""
        standardReport(query, 292)

        #   Report 293: Titles with Suspect English Capitalization
        query = """select t.title_id from titles t
                where binary title_title REGEXP "[^\:\.\!\;\/](%s)"
                and t.title_language = 17
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 293
                        and c.record_id = t.title_id
                        and c.resolved is not NULL
                        )
                limit 1000""" % requiredLowerCase()
        standardReport(query, 293)

        #   Report 294: Publications with Suspect English Capitalization
        query = """select distinct p.pub_id from pubs p
                where binary p.pub_title REGEXP "[^\:\.\!\;\/](%s)"
                and exists (
                        select 1 from titles t, pub_content pc
                        where t.title_id = pc.title_id
                        and p.pub_id = pc.pub_id
                        and t.title_language = 17
                )
                and not exists (
                        select 1 from cleanup c
                        where c.report_type = 294
                        and c.record_id = p.pub_id
                        and c.resolved is not NULL
                        )
                limit 1000""" % requiredLowerCase()
        standardReport(query, 294)

        #   Report 295: Publications with the 'WatchDate' Template in Notes
        query = """select p.pub_id
                from pubs p, notes n
                where p.note_id = n.note_id
                and n.note_note like '%{{WatchDate}}%'
                """
        standardReport(query, 295)

        #   Report 296: Stonecreek's EditPub submissions with 'first printing' in notes
        query = """select user_id from mw_user where user_name='Stonecreek'"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        user_id = record[0][0]

        query = """select affected_record_id from submissions
                where sub_submitter=%d
                and sub_data like "%%first printing%%"
                and sub_data not like "%%apparent first printing%%"
                and sub_data not like "%%assumed first printing%%"
                and affected_record_id is not null
                and sub_type = 4""" % user_id
        db.query(query)
        result = db.store_result()
        count = result.num_rows()
        pubs = []
        record = result.fetch_row()
        while record:
                pub_id = record[0][0]
                pubs.append(pub_id)
                record = result.fetch_row()

        in_clause = list_to_in_clause(pubs)
        if in_clause:
                query = """select p.pub_id
                        from pubs p
                        where p.pub_id in (%s)
                        and not exists(select 1 from primary_verifications pv
                                        where pv.pub_id = p.pub_id)""" % in_clause
                standardReport(query, 296)

        #   Report 297: Short Fiction Title Records with '(Part' in the Title field
        query = """select title_id, title_title, title_ttype from titles
                where title_title like '%(Part %'
                and title_ttype = 'SHORTFICTION'"""
        standardReport(query, 297)

        #   Report 298: Title-Based Awards with a Different Stored Author Name
        query = """select a.award_id, a.award_author from awards a 
                where exists(select 1 from title_awards ta1 where ta1.award_id = a.award_id) 
                and not exists( 
                select 1 from title_awards ta2, titles t, canonical_author ca, authors au 
                where ta2.award_id = a.award_id 
                and ta2.title_id = t.title_id 
                and t.title_id = ca.title_id 
                and ca.ca_status = 1 
                and ca.author_id = au.author_id 
                and ( 
                (au.author_canonical = a.award_author) 
                or (a.award_author like concat(au.author_canonical, '+%'))
                or (a.award_author like concat('%+', au.author_canonical))
                or (a.award_author like concat('%+', au.author_canonical, '+%'))
                )) """
        standardReport(query, 298)

        #   Report 299: Publications with Swedish Titles with no Libris XL ID
        query = """select distinct p.pub_id
            from pubs p, titles t, pub_content pc, languages l
            where p.pub_id = pc.pub_id
            and pc.title_id = t.title_id
            and t.title_language = l.lang_id
            and l.lang_name = 'Swedish'
            and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
            and t.title_ttype not in ('INTERIORART')
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris XL')"""
        standardReport(query, 299)

        #   Report 300: Publications with Swedish Titles with a Libris ID and no Libris XL ID
        query = """select distinct p.pub_id
            from pubs p, titles t, pub_content pc, languages l
            where p.pub_id = pc.pub_id
            and pc.title_id = t.title_id
            and t.title_language = l.lang_id
            and l.lang_name = 'Swedish'
            and p.pub_ctype not in ('MAGAZINE', 'FANZINE')
            and t.title_ttype not in ('INTERIORART')
            and exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris')
            and not exists
            (select 1 from identifiers i, identifier_types it
            where p.pub_id = i.pub_id
            and i.identifier_type_id = it.identifier_type_id
            and it.identifier_type_name = 'Libris XL')"""
        standardReport(query, 300)

        #   Report 301: Reviews Whose Language Doesn't Match the Language of the Reviewed Title
        query = """select r.title_id
                   from titles r, title_relationships tr, titles t
                   where r.title_ttype = 'REVIEW'
                   and r.title_id = tr.review_id
                   and tr.title_id = t.title_id
                   and r.title_language != t.title_language"""
        standardReport(query, 301)

        #   Report 302: Author Names with an Unrecognized Suffix
	query = """select author_id from authors
                where """

        subquery = ''
        for suffix in RECOGNIZED_SUFFIXES:
                if not subquery:
                        subquery = """replace(author_canonical, ', %s', '')""" % suffix
                else:
                        subquery = """replace(%s, ', %s', '')""" % (subquery, suffix)

        query += subquery
        query += """ like '%,%'"""
        standardReport(query, 302)

        #   Report 303: COVERART titles with 'uncredited' Author
        query = """select t.title_id
                from titles t, authors a, canonical_author ca
                where t.title_id = ca.title_id
                and t.title_ttype = 'COVERART'
                and ca.author_id = a.author_id
                and ca.ca_status = 1
                and a.author_canonical = 'uncredited'"""
        standardReport(query, 303)

        #   Report 304: Publications with COBISS references in notes and no template/External ID
        query = """select p.pub_id
                from pubs p, notes n 
                where p.note_id = n.note_id 
                and n.note_note like '%COBISS%' 
                and n.note_note not like '%{{COBISS%' 
                and not exists
                (select 1 from identifiers i, identifier_types it 
                where p.pub_id = i.pub_id 
                and i.identifier_type_id = it.identifier_type_id 
                and it.identifier_type_name like '%COBISS%')"""
        standardReport(query, 304)

        #   Report 305: Publications with Biblioman references in notes and no template/External ID
        query = """select p.pub_id
                from pubs p, notes n 
                where p.note_id = n.note_id 
                and n.note_note like '%Biblioman%' 
                and n.note_note not like '%{{Biblioman|%' 
                and not exists 
                (select 1 from identifiers i, identifier_types it 
                where p.pub_id = i.pub_id 
                and i.identifier_type_id = it.identifier_type_id 
                and it.identifier_type_name = 'Biblioman')"""
        standardReport(query, 305)

        #   Report 307: Awards Linked to Uncommon Title Types (currently limited to CHAPBOOK titles)
        query = """select ta.award_id
                from titles t, title_awards ta
                where ta.title_id = t.title_id
                and t.title_ttype in ('CHAPBOOK')"""
        standardReport(query, 307)

        #   Report 324: Pubs without an ISBN and with an Audible ASIN which is an ISBN-10
        query = """select p.pub_id
                from pubs p
                where (p.pub_isbn is NULL or p.pub_isbn = '')
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        and i.identifier_value regexp '^[[:digit:]]{9}[0-9Xx]{1}$'
                        )
                """
        standardReport(query, 324)

        #   Report 325: Digital audio download pubs with regular ASINs and no Audible ASINs
        query = """select p.pub_id
                from pubs p
                where p.pub_ptype = 'digital audio download'
                and (p.pub_price like '$%' or p.pub_price is NULL or p.pub_price = '')
                and exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'ASIN'
                        )
                and not exists
                        (select 1
                        from identifiers i, identifier_types it
                        where p.pub_id = i.pub_id
                        and i.identifier_type_id = it.identifier_type_id
                        and it.identifier_type_name = 'Audible-ASIN'
                        )
                """
        standardReport(query, 325)

        #   Report 326: Pubs with an Audible ASIN and a non-Audible format
        query = """select p.pub_id
                from pubs p, identifiers i, identifier_types it
                where p.pub_ptype != 'digital audio download'
                and p.pub_id = i.pub_id
                and i.identifier_type_id = it.identifier_type_id
                and it.identifier_type_name = 'Audible-ASIN'
                """
        standardReport(query, 326)

def requiredLowerCase():
        clause = ''
        for word in ENGLISH_LOWER_CASE:
                clause += ' %s |' % word.capitalize()
        clause = clause[:-1]
        return clause

def badUnicodeReport(table, record_title, record_id, report_number):
        pattern_match = ISFDBBadUnicodePatternMatch(record_title)
        where_clause = "%s like '%%&#%%' and (%s)" % (record_title, pattern_match)
        query = """select %s from %s where %s""" % (record_id, table, where_clause)
        standardReport(query, report_number)
