/* 
   create_trans_title_table.sql is a MySQL script intended to
   create a table of transliterated title titles

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/04/28 23:23:42 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS trans_titles (
	trans_title_id int(11) NOT NULL auto_increment,
	trans_title_title mediumtext,
	title_id int(11),
	PRIMARY KEY (trans_title_id),
	KEY title_id (title_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
