/* 
   add_angus_robertson.sql is a MySQL script intended to add 
   Angus & Robertson as an "Other Sites" option.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url, site_isbn13) VALUES
(29,'Angus & Robertson','http://www.angusrobertson.com.au/books/p/%s', 1);
