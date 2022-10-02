# Number of ordered and paid licenses is counted

## Analyse payments

After payments have been received, you need to provide a CSV file with payment information. Our bank provides the possiblity to export transfer data as CSV file and I use the format of this CSV file here. The filename again is provided as Variable: `PAYMENT_DATA_CSV` in (`../src/ebook_config.py`)[../src/ebook_config.py]

*Example data* ((../data/payment-data_22-23_8.csv)[../data/payment-data_22-23_8.csv]):

```
"Auftragskonto";"Buchungstag";"Valutadatum";"Buchungstext";"Verwendungszweck";"Glaeubiger ID";"Mandatsreferenz";"Kundenreferenz (End-to-End)";"Sammlerreferenz";"Lastschrift Ursprungsbetrag";"Auslagenersatz Ruecklastschrift";"Beguenstigter/Zahlungspflichtiger";"Kontonummer/IBAN";"BIC (SWIFT-Code)";"Betrag";"Waehrung";"Info"
"DE12345678901234567890";"30.09.22";"30.09.22";"GUTSCHR. UEBERWEISUNG";"EBook/2223/8/1 ";;;;;;;"Delphi Phantasie";"DE12345678901234567890";"XXXXXXXXXX";"8,00";"EUR";"Umsatz gebucht"
"DE12345678901234567890";"30.09.22";"30.09.22";"ECHTZEIT-GUTSCHRIFT";"EBOOK/2223/8/2 Basic Traum";;;;;;;"Eiffel Traum";"DE12345678901234567890";"XXXXXXXXXX";"6,00";"EUR";"Umsatz gebucht"
"DE12345678901234567890";"31.08.22";"01.09.22";"ENTGELTABSCHLUSS";"Entgeltabrechnung siehe Anlage ";;;;;;;;"0000000000";"XXXXXXXXXX";"-0,80";"EUR";"Umsatz gebucht"
```

The script which reads the file with payment information files and updates the order data is (`../src/02_check_payment_data.py`)[../src/02_check_payment_data.py]. As not all parents use solely the purpose of use that was sent to them, some minor assumptions are made: Everything is compared using upper case and information, that seems to be important, is thrown away.

In our example, two payments were received, so that the updated order file (which overwrites `ORDER_DATA_JSON`) contains the following information now:

```
{
    "Phantasie, Ada": {
        "Lizenzen": [
            "D",
            "M",
            "La-1",
            "La-2"
        ],
        "Preis": 800,
        "Erziehungsberechtigte/r": "Delphi Phantasie",
        "E-Mail": "deph@beispiel.de",
        "Verwendungszweck": "EBOOK/2223/8/1",
        "bezahlt": true
    },
    "Traum, Basic": {
        "Lizenzen": [
            "D",
            "E",
            "M"
        ],
        "Preis": 600,
        "Erziehungsberechtigte/r": "Eiffel Traum",
        "E-Mail": "eit@beispiel.de",
        "Verwendungszweck": "EBOOK/2223/8/2",
        "bezahlt": true
    },
    "Wolke, Cobol": {
        "Lizenzen": [
            "D",
            "E"
        ],
        "Preis": 300,
        "Erziehungsberechtigte/r": "Fortran Cumulus",
        "E-Mail": "focu@beispiel.de",
        "Verwendungszweck": "EBOOK/2223/8/3"
    }
}
```

Please note, that two data sets contain `"bezahlt": true` now, while one does not.

Of course, you can edit this file manually, after having run the script.

## Count ordered and paid licenses

Now, based on the updated order data (`ORDER_DATA_JSON` in (`../src/ebook_config.py`)[../src/ebook_config.py]) and the list of available books (`AVAILABLE_EBOOK_LIST_TXT` in [`../src/ebook_config.py`](../src/ebook_config.py) are used to count both
- the number of ordered instances of each book, and
- the number of ordered and paid instances of each book.

The results are written to a CSV-file again (`PAID_AND_ORDERED_EBOOKS_CSV` in (`../src/ebook_config.py`)[../src/ebook_config.py]), which can be used as basis for ordering.

The script which reads input files and writes the output file is (`../src/03_count_paid_licenses.py`)[../src/03_count_paid_licenses.py].

*Example for resulting file* (`../data/number-of-paid-licenses_22-23_8.csv`)[../data/number-of-paid-licenses_22-23_8.csv]:

```
ID;Buchbezeichnung;Preis;Verlag;bezahlterPreis;Anzahl (bestellt);Anzahl (bezahlt)
D;Deutschbuch;100;Athene;;3;2
E;Englischbuch;200;Zeus;;2;1
M;Mathebuch;300;Hera;;2;2
La-1;Lateinbuch;200;Zeus;;1;1
La-2;Latein-Grammatik;200;Zeus;;1;1
```
