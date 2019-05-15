/* 
   correct_european_library_links.sql is a MySQL script intended to  
   delete one of the two European Library rows in the websites tables
   and correct the other one.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

DELETE from websites where site_name='European Library (complex)';
UPDATE websites SET site_name='European Library' where site_name='European Library (simple)';
UPDATE websites SET site_url='http://www.theeuropeanlibrary.org/tel4/search?query=%s'
where site_name='European Library';

