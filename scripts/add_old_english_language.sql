/* 
   add_old_english_language.sql is a MySQL script intended to add
   Old English to ISFDB

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/10/23 23:06:17 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (99, 'ang','Old English');
