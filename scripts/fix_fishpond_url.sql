/* 
   fix_fishpond_url.sql is a MySQL script intended to  fix FishPond URLs

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/08/26 01:12:42 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites SET site_url='http://www.fishpond.com.au/advanced_search_result.php?keywords=%s'
where site_name='Fishpond';
