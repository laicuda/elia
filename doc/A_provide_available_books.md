# School provides information on available ebooks

This list on available ebooks is provided as CSV file:

In the example data this file is called [`../data/available_ebooks_8.csv`](../data/available_ebooks_8.csv) and contains the following data:
```
ID;Buchbezeichnung;Preis;Verlag;bezahlterPreis
D;Deutschbuch;100;Athene;
E;Englischbuch;200;Zeus;
M;Mathebuch;300;Hera;
La-1;Lateinbuch;200;Zeus;
La-2;Latein-Grammatik;200;Zeus;
```
The fields `ID` and `Verlag` are especially important - they will be used later on to uniquely identify books and publishers. The price has to be given as integer (in Cents). The price actually paid is not (yet) used - it could be used to give back money if discounts apply.

Please write the filename of the CSV file with available books to [`../src/ebook_config.py`](../src/ebook_config.py) to the variable `AVAILABLE_EBOOK_LIST_CSV` - it is used by many of the following scripts.

The script [`../src/00_generate_poll.py`](../src/00_generate_poll.py) can be used to generate a text file (`AVAILABLE_EBOOK_LIST_TXT` in [`../src/ebook_config.py`](../src/ebook_config.py)) which our school can use to generate a poll for the parents. For the example data, the generated file [`../data/available_ebooks_8.txt`](../data/available_ebooks_8.txt) contains the following data:

```
D - Deutschbuch (Athene; 1,00 €)
E - Englischbuch (Zeus; 2,00 €)
M - Mathebuch (Hera; 3,00 €)
La-1 - Lateinbuch (Zeus; 2,00 €)
La-2 - Latein-Grammatik (Zeus; 2,00 €)
```