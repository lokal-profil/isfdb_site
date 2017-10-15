#
#     (C) COPYRIGHT 2008   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2008/06/07 13:14:36 $

sql:
	./create_sql.py > isfdb.sql

charts:
	./svgChart.py novels > novels.svg
	./svgChart.py shortfiction > shortfiction.svg
	./svgChart.py reviews > reviews.svg
	./svgChart.py pubs > pubs.svg
	./svgChart.py magazines > magazines.svg
	./svgChart.py verif > verif.svg

clobber:
	rm -f localdefs.*
