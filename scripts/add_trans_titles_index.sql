/* 
   add_trans_titles_index.sql is a MySQL script intended to
   add a new index (trans_title_title ) to table "trans_titles"

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX trans_title_title USING BTREE ON trans_titles(trans_title_title(50));

