/* 
   add_whsmith.sql is a MySQL script intended to add 
   W. H. Smith as "Other Sites" options.

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/10/30 22:14:19 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url, site_isbn13) VALUES(30,'WHSmith','https://www.whsmith.co.uk/pws/ProductDetails.ice?ProductID=%s',1);
