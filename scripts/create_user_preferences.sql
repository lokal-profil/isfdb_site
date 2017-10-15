/* 
   create_user_preferences.sql is a MySQL script intended to add
   table "user_preferences" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1.1 $
   Date:    $Date: 2009/11/10 02:52:10 $

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS `user_preferences` (
  `user_pref_id` int(11) NOT NULL auto_increment,
  `user_id` int(11),
  `concise_disp` int(1),
  PRIMARY KEY  (`user_pref_id`),
  KEY `user_id` (`user_id`),
  KEY `concise_disp` (`concise_disp`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;