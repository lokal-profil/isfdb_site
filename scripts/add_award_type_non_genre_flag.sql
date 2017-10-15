/* 
   add_award_type_non_genre_flag.sql is a MySQL script intended to
   alter table "award_types" to add field award_type_non_genre

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/08/13 02:21:35 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE award_types ADD COLUMN award_type_non_genre ENUM('Yes', 'No');
UPDATE award_types set award_type_non_genre = 'No';
UPDATE award_types set award_type_non_genre = 'Yes' where award_type_id in (53, 52);
