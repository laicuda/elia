"""
This module reads data regarding available ebook licences from a CSV file
(see ebook_functions.get_available_books). The filename is provided as value
of the data object AVAILABLE_EBOOK_LIST_CSV in ebook_config.py.

Afterwards data regarding the orders that have been placed by parents are read
from a second CSV file (see ebook_functions.get_order_data).
The filename is provided as value of the data object ORDER_DATA_CSV
in ebook_config.py.

All data regarding the orders are now stored in a JSON object in a file
(see ebook_functions.dump_order_data), the filename of which is provided 
in ORDER_DATA_JSON in ebook_config.py.
The data from this file will be used in the next scripts to check whether the
payment occurred and to allocate and send licence information.

Finally, an email is sent to each pupil (and in CC to the sender) using the 
information provided in EMAIL_* (see ebook_config.py). In "dry run" mode, 
the emails will not be sent, but merely printed on the screen.
"""


#######################################################################################
import ebook_config
import ebook_functions
import getpass
import smtplib
from email.message import EmailMessage


#######################################################################################
dry_run = False  # if true, no emails will be sent, but printed on the screen; if false, emails will be sent


#######################################################################################
def send_emails(
    order_data,
    available_books,
    sender_address,
    server_name,
    server_port,
    username,
    subject,
):
    """send emails with information on the order and the payment information for all orders

    keyword arguments:
    order_data - list of all orders as obtained by ebook_functions.get_order_data
    available_books - available ebooks as obtained by ebook_functions.get_available_books
    sender_address - e-mail address of sender of e-mail
    server_name - name of SMTP server
    server_port - port of SMPT port
    username - username to log in to SMTP server
    subject - subject of e-mail, will be extended by name of pupil
    """
    # ask for password only, if e-mails will be sent
    password = ""
    if not dry_run:
        password = getpass.getpass()

    # send mail for each order
    for pupil, data in order_data.items():
        # generate list with a short desription of each ordered book
        books = []
        for book in data["Lizenzen"]:
            description = (
                available_books[book]["Buchbezeichnung"]
                + " ("
                + available_books[book]["Verlag"]
                + ")"
            )
            books.append(description)
        # generate complete text for mail
        text = ebook_config.generate_mail_text_for_payment(
            data["Erziehungsberechtigte/r"],
            pupil,
            books,
            data["Preis"],
            data["Verwendungszweck"],
        )

        # define mail
        msg = EmailMessage()
        msg.set_content(text)
        msg["Subject"] = subject + pupil
        msg["From"] = sender_address
        msg["To"] = data["E-Mail"]
        msg["Cc"] = sender_address

        # show or send mail
        if dry_run:
            print("====================================================")
            print("E-Mail:")
            print("----------------------------------------------------")
            print(msg)
        else:
            s = smtplib.SMTP(server_name, port=server_port)
            s.starttls()
            s.ehlo()
            s.login(username, password)
            s.send_message(msg)
            s.quit()
            print("Sent to " + msg["To"])


#######################################################################################
def main():
    available_books = ebook_functions.get_available_books(
        ebook_config.AVAILABLE_EBOOK_LIST_CSV
    )
    print("====================================================")
    print("Available books:")
    print("----------------------------------------------------")
    print(available_books)

    order_data = ebook_functions.get_order_data(
        ebook_config.ORDER_DATA_CSV,
        available_books,
        ebook_config.TRANSFER_PURPOSE_OF_USE_PREFIX,
    )
    print("====================================================")
    print("Order data:")
    print("----------------------------------------------------")
    for name, data in order_data.items():
        print(name)
        print(data)
        print("***")

    ebook_functions.dump_order_data(order_data, ebook_config.ORDER_DATA_JSON)

    send_emails(
        order_data,
        available_books,
        ebook_config.EMAIL_SENDER_ADDRESS,
        ebook_config.EMAIL_SERVER,
        ebook_config.EMAIL_PORT,
        ebook_config.EMAIL_LOGIN,
        ebook_config.EMAIL_SUBJECT,
    )


#######################################################################################
if __name__ == "__main__":
    main()
