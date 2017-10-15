/* 
   create_trans_pub_series_table.sql is a MySQL script intended to
   create a table of transliterated publication series names

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/01/11 01:27:49 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS trans_pub_series (
	trans_pub_series_id int(11) NOT NULL auto_increment,
	trans_pub_series_name mediumtext,
	pub_series_id int(11),
	PRIMARY KEY (trans_pub_series_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
