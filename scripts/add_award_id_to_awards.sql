/* 
   add_award_id_to_awards.sql is a MySQL script intended to
   alter table "awards" to add field award_type_id

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE awards ADD COLUMN award_type_id INT(11);