/* 
   add_title_graphic_flag.sql is a MySQL script intended to
   alter table "titles" to add field title_graphic

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/02/14 03:10:43 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD COLUMN title_graphic ENUM('Yes', 'No');
