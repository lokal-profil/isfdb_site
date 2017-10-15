/* 
   change_missing_pub_formats_to_unknown.sql is a MySQL script intended to
   change empty or NULL publication format values to 'unknown'

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/01/09 23:23:51 $

  (C) COPYRIGHT 2014   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update pubs set pub_ptype='unknown' where pub_ptype IS NULL or pub_ptype='';
