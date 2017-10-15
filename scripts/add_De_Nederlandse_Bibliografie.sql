/* 
   add_Nederlandse_Bibliografie.sql is a MySQL script intended to
   add De Nederlandse Bibliografie as an external idenifier
	

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/08/20 20:04:41 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('PPN', 'De Nederlandse Bibliografie Pica Productie Nummer');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (16, 1, 'http://picarta.pica.nl/xslt/DB=3.9/XMLPRS=Y/PPN?PPN=%s');

