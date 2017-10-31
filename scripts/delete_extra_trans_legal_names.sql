/* 
   delete_extra_trans_legal_names.sql is a MySQL script intended to
   delete records from the trans_legal_names table which are
   associated with author records that are no longer in the database

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from trans_legal_names where not exists
(select 1 from authors a where a.author_id=trans_legal_names.author_id);
