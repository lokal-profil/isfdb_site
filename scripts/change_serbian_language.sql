/* 
   change_serbian_language.sql is a MySQL script intended to
   change the value of the latin_script field for the
   Serbian language from "No" to "Yes". Modern Serbian uses
   both Latin and Cyrillic.

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/04/27 17:57:12 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE languages SET latin_script='Yes' where lang_name='Serbian'
