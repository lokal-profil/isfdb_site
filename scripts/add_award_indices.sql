/* 
   add_award_indices.sql is a MySQL script intended to
   add indices by award category and award type to table "awards".

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/06/13 20:30:20 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index award_cat ON awards(award_cat_id);
create index award_type ON awards(award_type_id);
