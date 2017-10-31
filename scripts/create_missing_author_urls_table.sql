/* 
   create_missing_author_urls_table.sql is a MySQL script intended to
   create a table of missing URLs for authors.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS missing_author_urls (
	missing_id int(11) NOT NULL auto_increment,
	url_type smallint,
	url mediumtext,
	author_id int(11),
	resolved tinyint(1),
	PRIMARY KEY (missing_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
