/* 
   add_author_indexes.sql is a MySQL script intended to
   add a new index (author_id) to table "webpages" and
   a new index (author_id) to table "emails"

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX author_id USING BTREE ON webpages(author_id);
CREATE INDEX author_id USING BTREE ON emails(author_id);

