/* 
   change_JNB.sql is a MySQL script intended to
   change the JNB identifier type to "JNB/JPNO".

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_types set identifier_type_name = 'JNB/JPNO' where identifier_type_name = 'JNB';
