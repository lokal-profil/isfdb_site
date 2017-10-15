/* 
   add_private_tag.sql is a MySQL script intended to
   alter table tags" to add column "tag_private"

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/01/21 17:30:40 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE tags ADD COLUMN tag_status TINYINT(1) DEFAULT 0 AFTER tag_name;
