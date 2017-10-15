/* 
   add_serbo_croatian.sql is a MySQL script intended to add
   Serbo-Croatian-Cyrillic and Serbo-Croatian-Roman to ISFDB

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/03/10 00:18:14 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (96, 'scc','Serbo-Croatian Cyrillic');
INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (97, 'scr','Serbo-Croatian Roman');
