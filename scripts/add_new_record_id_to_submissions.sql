/* 
   add_new_record_id_to_submissions.sql is a MySQL script intended to
   alter table "submissions" to add field "new_pub_id"

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE submissions ADD COLUMN new_record_id INT(11);