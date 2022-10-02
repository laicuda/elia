"""This module contains functions to read and write data regarding 
available ebooks and order data to and from files.
"""

import csv
import json


#######################################################################################
def get_available_books(filename):
    """reads data regarding available ebooks from a CSV file

    These data include an ID, a name, the usual price in cent, the publisher
    and the price that has actually been paid (in cent):
    ```
    ID;Buchbezeichnung;Preis;Verlag;bezahlterPreis
    D;Deutschbuch;100;Athene;98
    E;Englischbuch;200;Zeus;200
    ...
    ```

    keyword arguments:
    filename - name of the CSV file with information on available books
    """
    available_books = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            available_books[row["ID"]] = row
    return available_books


#######################################################################################
def get_order_data(filename, available_books, purpose_of_use):
    """reads data regarding ordered ebook licenses from parents from a CSV file

    These data include the class and name of the pupil, the name of the parents,
    the e-mail address ("Freitextantwort") and X for each ordered ebook.
    The IDs of the ebooks have to match those in the file describing the available
    ebooks.
    ```
    Klasse;Name;Erziehungsberechtigte/r;Freitextantwort;D;E;M;La-1;La-2
    08A;Phantasie, Ada;Delphi Phantasie;deph@beispiel.de;X;;X;X;X
    08B;Traum, Basic;Eiffel Traum;eit@beispiel.de;X;X;X;;
    08B;Wolke, Cobol;Fortran Cumulus;focu@beispiel.de;X;X;;;
    ...
    ```

    keyword arguments:
    filename - name of the CSV file with information on the orders obtained from the web portal
    available_books - dictionary of available ebooks as obtained from get_available_books
    purpose_of_use - prefix for purpose of use for bank transfer;
                     will be extended by a serial number, so that each bank transfer can be identified easily
    """
    order_data = {}
    serial_number = 1
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            print(row)
            order_data[row["Name"]] = {}
            order_data[row["Name"]]["Lizenzen"] = []
            order_data[row["Name"]]["Preis"] = 0
            order_data[row["Name"]]["Erziehungsberechtigte/r"] = row[
                "Erziehungsberechtigte/r"
            ]
            order_data[row["Name"]]["E-Mail"] = row["Freitextantwort"]
            for id, data in available_books.items():
                if row[id] == "X":
                    order_data[row["Name"]]["Lizenzen"].append(id)
                    order_data[row["Name"]]["Preis"] += int(data["Preis"])
            order_data[row["Name"]]["Verwendungszweck"] = purpose_of_use + str(
                serial_number
            )
            serial_number += 1
    return order_data


#######################################################################################
def dump_order_data(order_data, filename):
    """function to save order data as JSON file

    The JSON object is an array of records. There is one record for each pupil, that is
    identified by the name of the pupil. Moreover, this record contains
    - IDs of ordered licenses (see AVAILABLE_EBOOK_LIST_CSV above)
    - name of parents
    - email address
    - total amount to be paid (in cents)

    keyword arguments:
    order_data - information on orders as obtained from get_order_data
    filename - name of JSON file
    """
    json_string = json.dumps(order_data, indent=4)
    with open(filename, "w") as f:
        print(json_string, file=f)


#######################################################################################
def get_order_data_json(filename):
    """function to read order data from JSON file

    see dump_order_data for a short description of contents

    keyword arguments:
    filename - name of JSON file
    """
    order_data = {}
    with open(filename, "r") as f:
        order_data = json.loads(f.read())

    return order_data
