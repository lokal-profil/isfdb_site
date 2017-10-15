/* 
   add_author_note.sql is a MySQL script intended to split
   the storylen field in the titles table into 4 fields. See
   FR 163 for details.

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/03/08 21:53:19 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE authors ADD author_note mediumtext;
