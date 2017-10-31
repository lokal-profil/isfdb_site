/* 
   Delete defunct pseudonyms as per Bug 2834693

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2009  Al von Ruff
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from pseudonyms where not exists (select * from authors where authors.author_id = pseudonyms.author_id);
delete from pseudonyms where not exists (select * from authors where authors.author_id = pseudonyms.pseudonym);
