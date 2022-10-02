# Parents get an e-mail with payment information

The data on [available ebooks](A_provide_available_books.md) (`AVAILABLE_EBOOK_LIST_CSV` in [`../src/ebook_config.py`](../src/ebook_config.py)) and the [orders placed by the parents](B_parents_poll.md) (`ORDER_DATA_CSV` in (`../src/ebook_config.py`)[../src/ebook_config.py]) are used to automatically send e-mails with payment information. Please use (`../src/01_send_transfer_data.py`)[../src/01_send_transfer_data.py] for this.

The e-mails contain information on the ordered ebooks, the total amount in EUR that has to be transferred as well as unique purpose of use. This purpose of use is put together by a prefix (`TRANSFER_PURPOSE_OF_USE_PREFIX` in (`../src/ebook_config.py`)[../src/ebook_config.py]) and a continous number. In the example data, the prefix is `EBOOK/2223/8/`. As there are three orders, the following purposes are generated:
* `EBOOK/2223/8/1`
* `EBOOK/2223/8/2`
* `EBOOK/2223/8/3`

The text of the e-mail can be adapted in (`../src/ebook_config.py`)[../src/ebook_config.py].

*Example:*
```
====================================================
E-Mail:
----------------------------------------------------
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable
MIME-Version: 1.0
Subject: Überweisungdaten E-Book-Lizenzen Wolke, Cobol
From: ebooks@beispiel.de
To: focu@beispiel.de
Cc: ebooks@beispiel.de

Liebe(r) Fortran Cumulus,

Sie haben für Ihr Kind "Wolke, Cobol" folgende E-Book-Lizenzen bestellt:
- Deutschbuch (Athene)
- Englischbuch (Zeus)

Bitte überweisen Sie den Betrag von 3.00 EUR bis Fr, 30.9.2022
unter Angabe des Verwendungszwecks EBOOK/2223/8/3 (weitere Angaben sind nicht notwendig) auf folgendes Konto:
   Empfäger
   IBAN: DE00 0000 0000 0000 0000 00
   BIC: BICBICBICBIC (Bankname)

Bei Unstimmigkeiten, Problemen oder Fragen kommen Sie gerne per E-Mail auf mich zu!

Viele Grüße,
Vorname Nachname
```

Besides sending e-mails [`../src/01_send_transfer_data.py`](../src/01_send_transfer_data.py) saves the order data as JSON data in a file (`ORDER_DATA_JSON` in [`../src/ebook_config.py`](../src/ebook_config.py)) and the following scripts will update the information saved there. For the example, the JSON file initially contains the following data:

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
        "Verwendungszweck": "EBOOK/2223/8/1"
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
        "Verwendungszweck": "EBOOK/2223/8/2"
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
