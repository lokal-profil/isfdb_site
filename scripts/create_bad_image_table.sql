/* 
   create_bad_image_table.sql is a MySQL script intended to
   create a table of bad images.

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/02/02 05:18:06 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS bad_images (
	pub_id int(11) NOT NULL,
	image_url mediumtext,
	PRIMARY KEY (pub_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
