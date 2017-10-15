/* 
   Create_Sir_Julius_Vogel_Award.sql is a MySQL script intended to create an entry for the Sir Julius Vogel Award.

   Version: $Revision: 1.1 $
   Date:    $Date: 2013/07/07 04:21:48 $

  (C) COPYRIGHT 2013   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id)
VALUES (50, 'Sj', 'Sir Julius Vogel Award', NULL, NULL);
