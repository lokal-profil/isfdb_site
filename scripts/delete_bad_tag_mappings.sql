/* 
   delete_bad_tag_mappings.sql is a MySQL script intended to
   delete obsolete/bad entries in the table tag_mapping

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

DELETE from tag_mapping where not exists (select 1 from titles where titles.title_id=tag_mapping.title_id)