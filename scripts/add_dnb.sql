/* 
   add_dnb.sql is a MySQL script intended to add Deutsche Nationalbibliothek 
   as another "Other Sites" option. 

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (22,'Deutsche Nationalbibliothek','https://portal.d-nb.de/opac.htm?query=%s&method=simpleSearch');
