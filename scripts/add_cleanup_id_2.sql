/* 
   add_cleanup_id_2.sql is a MySQL script intended to
   alter table "cleanup" to add field cleanup_id_2

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/02/19 22:47:07 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE cleanup MODIFY report_type INT(11);
ALTER TABLE cleanup ADD COLUMN record_id_2 INT(11);
