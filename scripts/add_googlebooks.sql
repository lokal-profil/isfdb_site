/* 
   add_googlebooks.sql is a MySQL script intended to add Google Books
   as another "Other Sites" option. 

   Version: $Revision: 1.1 $
   Date:    $Date: 2011/10/30 18:39:57 $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (18,'Google Books','http://books.google.com/books?vid=ISBN%s');

