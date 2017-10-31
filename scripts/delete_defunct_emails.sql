/* 
   delete_defunct_emails.sql is a MySQL script intended to
   delete authors' e-mail addresses for previously deleted
   authors.

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from emails where not exists (select 1 from authors where authors.author_id=emails.author_id);
	
