/* 
   fix_verso_publisher.sql is a MySQL script intended to fix "Verso" publisher

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/10/26 23:19:37 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE publishers SET note_id = NULL where publisher_id=12421;
