/* 
   add_short_award_name.sql is a MySQL script intended to
   alter table "award_types" to add field award_type_short_name

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE award_types ADD COLUMN award_type_short_name MEDIUMTEXT;
