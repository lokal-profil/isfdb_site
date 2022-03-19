/* 
   add_title_language.sql is a MySQL script intended to
   alter table "titles" to include column "title_language".

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD title_language INT(11) AFTER title_ctl;
