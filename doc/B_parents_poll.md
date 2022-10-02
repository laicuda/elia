# Parents answer a poll and thereby order ebook licenses

The results of the poll have to be provided as a CSV file - please use `ORDER_DATA_CSV` in [`../src/ebook_config.py`](../src/ebook_config.py) to provide the filename! 

The following format can easily be obtained from the webportal of our school and is thus used.

Here, you find again example data ([`../data/webportal_orders_22-23_8.csv`](../data/webportal_orders_22-23_8.csv)). Please note, that "Freitextantwort" contains the email address, which is used for sending payment information and the actual licenses, and afterwards, there is one column for each book. The name of the column *must* be the ID from the CSV containing the list of available books. An `X` means, that this book has been ordered.

```
Klasse;Name;Erziehungsberechtigte/r;Freitextantwort;D;E;M;La-1;La-2
08A;Phantasie, Ada;Delphi Phantasie;deph@beispiel.de;X;;X;X;X
08B;Traum, Basic;Eiffel Traum;eit@beispiel.de;X;X;X;;
08B;Wolke, Cobol;Fortran Cumulus;focu@beispiel.de;X;X;;;
```