/* 
   auto_assign_languages_to_titles.sql is a MySQL script intended to add 
   auto-assign a language code to titles. This will be done in
   stages after a manual review of language-less titles. See
   FR 965 for the associated cleanup report. 

   Version: $Revision: 1.26 $
   Date:    $Date: 2017/02/27 20:41:39 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update titles set title_language=17 where title_language is null and title_ttype in ('OMNIBUS', 'COLLECTION', 'ANTHOLOGY', 'CHAPBOOK', 'EDITOR', 'NONFICTION', 'NOVEL', 'SHORTFICTION', 'INTERVIEW', 'POEM', 'REVIEW',
'COVERART', 'ESSAY', 'INTERIORART');
