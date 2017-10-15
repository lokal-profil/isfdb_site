/* 
   add_librarything.sql is a MySQL script intended to add LibraryThing
   as another "Other Sites" option. 

   Version: $Revision: 1.1 $
   Date:    $Date: 2011/10/30 18:40:44 $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (19,'LibraryThing','http://www.librarything.com/isbn/%s');

