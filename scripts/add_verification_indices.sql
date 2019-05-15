/* 
   add_verification_indices.sql is a MySQL script intended
   to add indices to primary and secondary verification tables

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX user_ver_time ON primary_verifications (user_id, ver_time);

CREATE INDEX user_ver_time ON verification (user_id, ver_time);
