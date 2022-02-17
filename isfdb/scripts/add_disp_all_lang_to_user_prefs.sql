/* 
   add_disp_all_lang_to_user_prefs.sql is a MySQL script intended to
   alter table "user_preferences" to include column "display_all_languages".

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE `user_preferences` ADD display_all_languages int(1);