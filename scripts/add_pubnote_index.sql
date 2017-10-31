/* 
   add_pubnote_index.sql is a MySQL script intended to
   alter table "pubs" to index the "note_id" column.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX note_id USING BTREE ON pubs (note_id);

