/* 
   add_suppress_warnings.sql is a MySQL script intended to
   alter table "user_preferences" to add two field:
   suppress_translation_warnings and suppress_bibliographic_warnings

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN suppress_translation_warnings TINYINT(1);
ALTER TABLE user_preferences ADD COLUMN suppress_bibliographic_warnings TINYINT(1);