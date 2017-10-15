/* 
   add_award_cat_pages.sql is a MySQL script intended to
   alter table "award_cats" to add field award_cat_id and
   alter table "webpages" to add field award_cat_note_id

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/07/05 12:17:43 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE webpages ADD COLUMN award_cat_id INT(11);
ALTER TABLE award_cats ADD COLUMN award_cat_note_id INT(11);
