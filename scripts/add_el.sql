/* 
   add_el.sql is a MySQL script intended to add the European Library
   as another "Other Sites" option. 

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (23,'European Library','http://search.theeuropeanlibrary.org/portal/en/search/%28%22isbn%22+all+%22%s%22%29.query#');
