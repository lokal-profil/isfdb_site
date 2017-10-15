/* 
   change_author_birthplace_len.sql is a MySQL script intended to change the length
   of the author_birthplace column in table authors from varcar(64) to mediumtext.

   Version: $Revision: 1.1 $
   Date:    $Date: 2013/04/30 20:35:09 $

  (C) COPYRIGHT 2013 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

alter table authors modify author_birthplace mediumtext;
