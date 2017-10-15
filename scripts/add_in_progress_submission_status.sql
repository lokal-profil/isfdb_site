/* 
   add_in_progress_submission_status.sql is a MySQL script intended to
   alter table "submissions" to add value "P" ("In Progress") to field
   sub_state

   Version: $Revision: 1.2 $
   Date:    $Date: 2015/04/03 23:10:38 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE submissions CHANGE sub_state sub_state ENUM('N','R','I','P');