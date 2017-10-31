/* 
   add_parent_series_index.sql is a MySQL script intended
   to add a parent series index to the series table
   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX parent_series ON series (series_parent);

