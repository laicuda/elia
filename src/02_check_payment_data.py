"""This module reads order data from JSON file that has been generated
by ebook_functions.dump_order_data (-> 01_send_transfer_data).

Moreover, data on received payments are read from a CSV file using 
get_payment_data. The format of this file depends on the export formats of
your bank account!

Information on whether a certain order has been paid or not is added to
order data and serves as the basis to determine the number of licenses that shall
be ordered.

The updated information is written to the JSON file again.
"""

#######################################################################################
import ebook_functions
import ebook_config
import csv


#######################################################################################
def get_payment_data(filename, expected_prefix):
    """function that reads all payments from CSV file

    It searches for a match of the transfer purpose and the expected prefix
    (both compared in upper case) and prints a list of not assignable payments
    on the screen.

    keyword arguments:
    filename - name of CSV file with payments
    expected_prefix - prefix expected in purpose of transfer to be able to match it with orders
    """
    payments = []
    purpose_not_found = []
    payments_with_prefix = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            payments.append(row)

    for payment in payments:
        purpose = payment["Verwendungszweck"].upper()
        if expected_prefix.upper() not in purpose:
            purpose_not_found.append(payment)
        else:
            payments_with_prefix.append(payment)

    print("====================================================")
    print("Payments that cannot be processed further:")
    print("----------------------------------------------------")
    for pnf in purpose_not_found:
        print(
            pnf["Beguenstigter/Zahlungspflichtiger"]
            + ": "
            + pnf["Verwendungszweck"]
            + " ("
            + pnf["Betrag"]
            + ")"
        )

    return payments_with_prefix


#######################################################################################
def update_order_data_with_payments(payments, order_data, expected_prefix):
    """function that tries to match payments and orders

    all payments that seem to contain the expected prefix are processed:
    - remove blanks and everything after the first blank after the found prefix
    - process purpose of transfers in upper case
    - search for an order with the same purpose of transfer
    - if amount paid and price match, mark order as paid 'True'

    keyword arguments:
    payments - list of payments as obtained from get_payment_data
    order_data - order data from previous scripts (read from JSON file)
    expected_prefix - prefix expected in purpose of transfer to be able to match it with orders
    """

    unprocessed_payments = []

    for payment in payments:
        purpose = payment["Verwendungszweck"].upper()
        amount = payment["Betrag"]
        amount = int(amount.replace(",", ""))

        # remove everything before expected prefix
        purpose = purpose[purpose.find(expected_prefix) :]
        # remove everything starting with first blank after expected prefix
        if purpose.find(" ") >= 0:
            purpose = purpose[: purpose.find(" ")]

        # search for order and mark it as paid, if purpose and amount do match
        found = False
        for name, data in order_data.items():
            if data["Verwendungszweck"].upper() == purpose and data["Preis"] == amount:
                data["bezahlt"] = True
                found = True

        # generate a list of payments that couldn't be processed
        if not found:
            unprocessed_payments.append(payment)

    if len(unprocessed_payments) > 0:
        print("====================================================")
        print("Payments that did not match any in order data:")
        print("----------------------------------------------------")
        for up in unprocessed_payments:
            print(
                up["Beguenstigter/Zahlungspflichtiger"]
                + ": "
                + up["Verwendungszweck"]
                + " ("
                + up["Betrag"]
                + ")"
            )


#######################################################################################
def main():
    order_data = ebook_functions.get_order_data_json(ebook_config.ORDER_DATA_JSON)
    payments = get_payment_data(
        ebook_config.PAYMENT_DATA_CSV, ebook_config.TRANSFER_PURPOSE_OF_USE_PREFIX
    )
    update_order_data_with_payments(
        payments, order_data, ebook_config.TRANSFER_PURPOSE_OF_USE_PREFIX
    )

    print("===========================================================")
    print("Orders that were not paid or payment could not be assigned:")
    print("-----------------------------------------------------------")
    for name, data in order_data.items():
        try:
            if not data["bezahlt"]:
                print(name)
                print(data)
        except:
            print(name)
            print(data)

    ebook_functions.dump_order_data(order_data, ebook_config.ORDER_DATA_JSON)


#######################################################################################
if __name__ == "__main__":
    main()
