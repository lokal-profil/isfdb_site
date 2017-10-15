/* 
   create_seiun_and_nihon_SF_awards.sql is a MySQL script intended
   to create entries for Seiun and Nihon SF Taisho awards

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/08/07 04:06:37 $

  (C) COPYRIGHT 2015   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id, award_type_by, award_type_for) VALUES (61, 'Se', 'Seiun Award', NULL, NULL, NULL, NULL);

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id, award_type_by, award_type_for) VALUES (62, 'Ni', 'Nihon SF Taisho Award', NULL, NULL, NULL, NULL);
