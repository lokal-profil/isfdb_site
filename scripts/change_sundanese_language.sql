/* 
   change_sundanese_language.sql is a MySQL script intended to
   change the value of the latin_script field for the
   Sundanese language from "No" to "Yes". It turns out that
   modern Sundanese support the Latin script.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE languages SET latin_script='Yes' where lang_name='Sundanese'
