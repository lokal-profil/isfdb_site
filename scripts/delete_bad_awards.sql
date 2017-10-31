/* 
   delete_bad_awards.sql is a MySQL script intended to
   delete bad award entries from "awards"

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

DELETE from awards where award_level=90 or award_level=80;