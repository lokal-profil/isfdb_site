/* 
   add_publisher_index.sql is a MySQL script intended to add
   a publisher index to the "pubs" table

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/10/22 23:08:41 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index publisher_id on pubs (publisher_id);
