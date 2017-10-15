/* 
   add_keep_spaces_in_searches.sql is a MySQL script intended to
   alter table "user_preferences" to add field add_keep_spaces_in_searches

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/03/01 19:23:49 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN keep_spaces_in_searches TINYINT(1);