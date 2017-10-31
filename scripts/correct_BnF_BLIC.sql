/* 
   correct_BnF_BLIC.sql is a MySQL script intended to fix the logic
   used to link to BnF by ISBN

   Version: $Revision$
   Date:    $Date$

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites
set site_url = 'http://catalogue.bnf.fr/rechercher.do?motRecherche=%s',
site_isbn13 = 2
where site_name = 'Bibliotheque nationale de France';

UPDATE websites
set site_isbn13 = 2
where site_name = 'Open Library';

UPDATE websites
set site_isbn13 = 1
where site_name = 'British Library';
