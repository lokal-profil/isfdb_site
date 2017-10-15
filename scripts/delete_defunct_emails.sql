/* 
   delete_defunct_emails.sql is a MySQL script intended to
   delete authors' e-mail addresses for previously deleted
   authors.

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/01/19 22:42:13 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from emails where not exists (select 1 from authors where authors.author_id=emails.author_id);
	
