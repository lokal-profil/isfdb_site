/* 
   fix_notes_with_mismatched_angle_brackets.sql is a MySQL script intended to
   fix Notes records with mismatched angle brackets

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/09/01 23:05:51 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE notes set note_note='' where note_id=222143;
DELETE from notes where note_id=343;
UPDATE authors set note_id=NULL where author_id=973;