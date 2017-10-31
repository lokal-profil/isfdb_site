/* 
   add_working_language.sql is a MySQL script intended to add a new column
   to the authors table to indicate the main language the author wrote in

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE authors 
ADD author_language INT(11) DEFAULT NULL;
