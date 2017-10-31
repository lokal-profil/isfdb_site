/* 
   change_titles_defaults.sql is a MySQL script intended to
   alter table titles and change the default values of the
   fields 'title_non_genre' and "title_graphic' from NULL
   to No.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ALTER COLUMN title_non_genre SET DEFAULT 'No';

UPDATE titles SET title_non_genre='No' where title_non_genre IS NULL;

ALTER TABLE titles ALTER COLUMN title_graphic SET DEFAULT 'No';

UPDATE titles SET title_graphic='No' where title_graphic IS NULL;
