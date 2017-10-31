/* 
   add_display_cover.sql is a MySQL script intended to
   alter table "user_preferences" to add field covers_display

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN covers_display TINYINT(1);