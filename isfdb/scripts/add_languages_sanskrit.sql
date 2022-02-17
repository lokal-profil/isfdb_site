/* 
   add_languages_sanskrit.sql is a MySQL script intended to add Sanskrit to the list of recognized languages. 

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2012 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (95, 'san','Sanskrit');
