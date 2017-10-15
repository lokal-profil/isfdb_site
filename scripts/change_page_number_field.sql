/* 
   change_page_number_field.sql is a MySQL script intended to change the length
   of the pubc_page column in table pub_content from varcar(8) to varchar(20).

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/02/18 04:27:40 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

alter table pub_content modify pubc_page varchar(20);
