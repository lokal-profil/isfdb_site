/* 
   change_BNB.sql is a MySQL script intended to
   change the URLs for BNB identifiers.

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/06/01 22:19:43 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_url =
'http://search.bl.uk/primo_library/libweb/action/search.do?fn=search&vl(freeText0)=%s'
where site_url like '%vid=BLBNB%';
