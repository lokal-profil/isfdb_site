/* 
   change_award_types_to_autoincrement.sql is a MySQL script intended to
   alter table "award_types" to change field award_type_id to be "auto_increment"

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE award_types MODIFY COLUMN award_type_id INT(11) auto_increment;