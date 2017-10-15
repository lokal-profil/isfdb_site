/* 
   add_title_language.sql is a MySQL script intended to
   alter table "titles" to include column "title_language".

   Version: $Revision: 1.1 $
   Date:    $Date: 2011/05/12 00:37:34 $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD title_language INT(11) AFTER title_ctl;
