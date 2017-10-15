/* 
   add_transliterated_indices.sql is a MySQL script intended to
   add indices to the following "transliterated names" tables:
   trans_pub_series, trans_publisher, and trans_legal_names

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/05/04 20:01:13 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index author_id ON trans_legal_names(author_id);
create index publisher_id ON trans_publisher(publisher_id);
create index pub_series_id ON trans_pub_series(pub_series_id);
