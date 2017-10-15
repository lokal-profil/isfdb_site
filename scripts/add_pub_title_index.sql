/* 
   add_pub_title_index.sql is a MySQL script intended
   to add a title/pub index to the pub_content table
   Version: $Revision: 1.1 $
   Date:    $Date: 2017/04/24 00:15:32 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index pubtitles on pub_content(pub_id,title_id);

