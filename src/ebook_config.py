"""This module contains all data and functions that are specific to a certain order.
It is included in the other scripts.
"""

# input file: available ebooks; for documentation of content see ebook_functions.py
AVAILABLE_EBOOK_LIST_CSV = "../data/available_ebooks_8.csv"
# name of automatically generated file with information on available ebooks that can be used to set up the poll in the web portal
AVAILABLE_EBOOK_LIST_TXT = "../data/available_ebooks_8.txt"

# input file: order data from web portal; for documentation of content see ebook_functions.py
ORDER_DATA_CSV = "../data/webportal_orders_22-23_8.csv"
# name of automatically generated file for (enriched) order data in JSON format
ORDER_DATA_JSON = "../data/order-data_22-23_8.json"

# input file: payment data (CSV format) from bank
PAYMENT_DATA_CSV = "../data/payment-data_22-23_8.csv"

TRANSFER_PURPOSE_OF_USE_PREFIX = "EBOOK/2223/8/"

# output file: number of ordered and paid licenses
PAID_AND_ORDERED_EBOOKS_CSV = "../data/number-of-paid-licenses_22-23_8.csv"

# input file: installation instrutions from publishers
INSTALLATION_INSTRUCTIONS = "../data/installation-details.json"

# output / input file: licenses for ebooks
EBOOK_LICENSES_JSON = "../data/ebook_licenses_22-23_8.json"

EMAIL_SENDER_ADDRESS = "ebooks@beispiel.de"
EMAIL_SUBJECT = "Überweisungdaten E-Book-Lizenzen "
EMAIL_SERVER = "smtp.beispiel.de"
EMAIL_PORT = 587
EMAIL_LOGIN = "username"


#######################################################################################
def generate_mail_text_for_payment(
    name_parents, name_pupil, books, amount_cent, purpose
):
    """function to put together text for emails to parents

    keyword arguments:
    name_parents - name of parents used for salutation
    name_pupil - name of child that will be put into the text
    books - list of ordered e-book licenses as strings (just short names, e.g. ["Deutschbuch", "Englischbuch"])
    amount_cent - the amount to be paid in cent (int)
    purpose - the individual purpose that has to be used for the bank transfoer
    """
    text = "Liebe(r) " + name_parents + "," + "\n"
    text += "\n"
    text += (
        'Sie haben für Ihr Kind "'
        + name_pupil
        + '" folgende E-Book-Lizenzen bestellt:\n'
    )
    for book in books:
        text += "- " + book + "\n"
    text += "\n"
    text += "Bitte überweisen Sie den Betrag von {:.2f} EUR bis Fr, 30.9.2022\n".format(
        amount_cent / 100.0
    )
    text += (
        "unter Angabe des Verwendungszwecks "
        + purpose
        + " (weitere Angaben sind nicht notwendig) auf folgendes Konto:\n"
    )
    text += "   Empfänger\n"
    text += "   IBAN: DE00 0000 0000 0000 0000 00\n"
    text += "   BIC: BICBICBICBIC (Bankname)\n\n"
    text += "Bei Unstimmigkeiten, Problemen oder Fragen kommen Sie gerne per E-Mail auf mich zu!\n\n"
    text += "Viele Grüße,\n"
    text += "Vorname Nachname"
    return text
