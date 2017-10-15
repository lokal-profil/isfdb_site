/* 
   add_smashwords.sql is a MySQL script intended to add Smashwords 
   as another "Other Sites" option. 

   Version: $Revision: 1.2 $
   Date:    $Date: 2012/12/14 05:14:10 $

  (C) COPYRIGHT 2011 Bill Longley and Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (16,'Smashwords','http://www.smashwords.com/isbn/%s');
