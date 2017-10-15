/* 
   add_state_reviewed_index_to_submissions.sql is a MySQL script intended to
   add a "state_reviewed" (i.e. a ombination of "sub_state" and "sub_reviewed")
   index to the table "submissions"

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/01/22 01:05:34 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX state_reviewed ON submissions (sub_state, sub_reviewed);

