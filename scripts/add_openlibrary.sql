/* 
   add_openlibrary.sql is a MySQL script intended to add Open Library 
   as another "Other Sites" option. 

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (17,'Open Library','http://openlibrary.org/isbn/%s');

