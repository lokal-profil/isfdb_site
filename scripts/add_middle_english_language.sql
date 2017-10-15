/* 
   add_middle_english_language.sql is a MySQL script intended to add
   Middle English to ISFDB

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/02/13 18:53:39 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (101, 'enm','Middle English');
