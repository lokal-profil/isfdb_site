/* 
   add_akkadian_and_sumerian_languages.sql is a MySQL script intended to add
   mayan language to ISFDB

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/03/24 15:40:23 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (105, 'akk','Akkadian');
INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (106, 'sux','Sumerian');
