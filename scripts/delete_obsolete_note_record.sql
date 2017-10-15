/* 
   delete_obsolete_note_record.sql is a MySQL script intended to
   delete one note record that is no longer associated with a
   publisher record

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/09/30 00:14:16 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from notes where note_id=138708;
