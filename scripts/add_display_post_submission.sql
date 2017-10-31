/* 
   add_display_post_submission.sql is a MySQL script intended to
   alter table "user_preferences" to add field display_post_submission

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN display_post_submission TINYINT(1);