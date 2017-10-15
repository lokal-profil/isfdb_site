/* 
   delete_non_existing_pub_contents.sql is a MySQL script intended to
   delete pub_content entries for non-existing pubs.

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/10/29 04:38:24 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from pub_content where not exists (select 1 from pubs pu where pub_content.pub_id = pu.pub_id);