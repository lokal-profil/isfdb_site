/* 
   create_trans_author_table.sql is a MySQL script intended to
   create a table of transliterated author titles

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/08/21 22:11:53 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS trans_authors (
	trans_author_id int(11) NOT NULL auto_increment,
	trans_author_name mediumtext,
	author_id int(11),
	PRIMARY KEY (trans_author_id),
	KEY author_id (author_id),
        KEY trans_author_name (trans_author_name(50))
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
