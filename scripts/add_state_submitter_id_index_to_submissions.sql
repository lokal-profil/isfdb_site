/* 
   add_state_submitter_id_index_to_submissions.sql is a MySQL script intended to
   add a "state_reviewed" (i.e. a ombination of "sub_state" and "sub_reviewed")
   index to the table "submissions"

   Version: $Revision: 418 $
   Date:    $Date: 2021-01-12 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX state_submitter_id ON submissions (sub_state, sub_submitter, sub_id);