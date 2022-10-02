""" This module reads
    - order data
    - license data
    - installation instructions
    and sends emails with all available licenses to those parents and pupils who paid.
    These email contain installation instructions from the publishers (if available)
    and hints if not all licenses are available yet.
    This means, that you can use this script several times, if you do not get all licenses
    at once.

    TODO:
    THIS MODULE CONTAINS MANY INFORMATION THAT IS NOT PASSED WELL
    (E-MAIL CONFIG NOT AS PARAMETERS, TEXT HARD-CODED HERE RATHER THAN IN CONFIG-FILE).
"""

import ebook_config
import ebook_functions
import json
import getpass
import smtplib
from email.message import EmailMessage
import mimetypes

#######################################################################################
dry_run = False  # if true, no emails will be sent, but printed on the screen; if false, emails will be sent


#######################################################################################
def get_json_data(filename):
    data = {}
    with open(filename, "r") as f:
        data = json.loads(f.read())

    return data


#######################################################################################
def send_licenses(order_data, license_data, installation_info):
    # ask for password only, if e-mails will be sent
    password = ""
    if not dry_run:
        password = getpass.getpass()

    for pupil, data in order_data.items():
        numberNewLicenses = (
            0  # a mail will only be sent if there is a new license for this pupil
        )
        try:
            data["bezahlt"]
        except:
            print("Skipping pupil " + pupil + "... (did not pay)")
        else:
            try:
                data["Lizenzen zugewiesen"]
            except:
                data["Lizenzen zugewiesen"] = {}
            finally:
                print("==============================================")
                print(pupil)
                print("----------------------------------------------")
                msg = EmailMessage()
                msg["Subject"] = "E-Book-Lizenzen für " + pupil
                msg["From"] = ebook_config.EMAIL_SENDER_ADDRESS
                msg["To"] = data["E-Mail"]
                msg["Cc"] = ebook_config.EMAIL_SENDER_ADDRESS
                text = "Liebe(r) " + data["Erziehungsberechtigte/r"] + "," + "\n"
                text += "\n"
                text += (
                    'mit dieser E-Mail bekommen Sie E-Book-Lizenzen für Ihr Kind "'
                    + pupil
                    + '".\n'
                )
                text += "\n"
                publishers = []
                for lic in data["Lizenzen"]:
                    if lic not in list(
                        data["Lizenzen zugewiesen"]
                    ):  # just look at licenses that have not been sent yet
                        publisher = license_data[lic]["Verlag"]
                        if license_data[lic]["vergebeneLizenzen"] < len(
                            license_data[lic]["Lizenzschluessel"]
                        ):  # licenses are available
                            numberNewLicenses += 1
                            if (
                                not publisher in publishers
                            ):  # just send installation instructions of publishers, from which licenses are sent
                                publishers.append(publisher)
                            data["Lizenzen zugewiesen"][lic] = {}
                            data["Lizenzen zugewiesen"][lic][
                                "Lizenzschluessel"
                            ] = license_data[lic]["Lizenzschluessel"][
                                license_data[lic]["vergebeneLizenzen"]
                            ]
                            license_data[lic]["vergebeneLizenzen"] += 1
                            text += (
                                "- "
                                + lic
                                + ": "
                                + license_data[lic]["Buchbezeichnung"]
                                + "\n"
                            )
                            text += (
                                "  Lizenzschlüssel: "
                                + data["Lizenzen zugewiesen"][lic]["Lizenzschluessel"]
                            )
                            text += "\n"
                        else:
                            print("There are not enough licenses for " + lic + " !")
                            text += (
                                "- "
                                + lic
                                + ": "
                                + license_data[lic]["Buchbezeichnung"]
                                + "\n"
                            )
                            text += "  Lizenzschlüssel fehlt noch - wird in einer separaten E-Mail verschickt, sobald er uns vorliegt."
                            text += "\n"

                text += "\n\nUnten finden Sie Installationshinweise der verschiedenen Verlage, im Anhang Nutzungsbedingungen.\n"
                text += "\n"
                text += "Viele Grüße,\n"
                text += "Vorname Nachname"
                text += "\n\n"
                for publisher in publishers:
                    text += (
                        "*** "
                        + publisher
                        + " ***********************************************\n"
                    )
                    for zeile in installation_info[publisher]["Installation"]:
                        text += zeile + "\n"
                    text += "\n\n"

                msg.set_content(text)

                for publisher in publishers:
                    ## Attachments
                    # https://pythoncircle.com/post/719/sending-email-with-attachments-using-python-built-in-email-module/
                    for attachment_filename in installation_info[publisher]["Dateien"]:
                        mime_type, _ = mimetypes.guess_type(attachment_filename)
                        mime_type, mime_subtype = mime_type.split("/", 1)
                        with open(attachment_filename, "rb") as ap:
                            msg.add_attachment(
                                ap.read(),
                                maintype=mime_type,
                                subtype=mime_subtype,
                                filename=attachment_filename,
                            )

                if numberNewLicenses > 0:
                    if dry_run:
                        print(msg)
                    else:
                        s = smtplib.SMTP(
                            ebook_config.EMAIL_SERVER, port=ebook_config.EMAIL_PORT
                        )
                        s.starttls()
                        s.ehlo()
                        s.login(ebook_config.EMAIL_LOGIN, password)
                        s.send_message(msg)
                        s.quit()
                        print("Sent to " + msg["To"])


#######################################################################################
def main():
    order_data = ebook_functions.get_order_data_json(ebook_config.ORDER_DATA_JSON)
    license_data = get_json_data(ebook_config.EBOOK_LICENSES_JSON)
    installation_info = get_json_data(ebook_config.INSTALLATION_INSTRUCTIONS)
    send_licenses(order_data, license_data, installation_info)
    ebook_functions.dump_order_data(order_data, ebook_config.ORDER_DATA_JSON)

    # save updated license file
    json_string = json.dumps(license_data, indent=4)
    with open(ebook_config.EBOOK_LICENSES_JSON, "w") as f:
        print(json_string, file=f)


#######################################################################################
if __name__ == "__main__":
    main()
