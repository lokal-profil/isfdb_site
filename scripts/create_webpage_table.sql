/* 
   create_webpage_tables.sql is a MySQL script intended to add
   table "websites" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1.1 $
   Date:    $Date: 2009/10/10 23:41:00 $

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS websites (
  site_id int(11) NOT NULL auto_increment,
  site_name tinytext,
  site_url mediumtext,
  PRIMARY KEY  (site_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
