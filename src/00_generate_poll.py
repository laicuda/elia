"""
This module reads data regarding available ebook licences from a CSV file
and stores it as text in a text file. This text file can be used to easily
set up the poll to order ebook licenses in the web portal.
"""


import ebook_config
import ebook_functions

#######################################################################################
def dump_available_ebooks(available_books, filename_txt):
    """function to dump list of available ebooks in a text file
    (one line per ebook)

    keyword arguments:
    available_books - dictionary of available ebooks as obtained from ebook_functions.get_available_books
    filename_txt - name of the TXT file to save infos to
    """
    text = ""
    for id, lic in available_books.items():
        text += lic["ID"]
        text += " - "
        text += lic["Buchbezeichnung"]
        text += " ("
        text += lic["Verlag"]
        text += "; "
        text += str("{:.2f}".format(int(lic["Preis"]) / 100)).replace(".", ",")
        text += " €)\n"

    with open(filename_txt, "w") as f:
        f.write(text)


#######################################################################################
def main():
    available_books = ebook_functions.get_available_books(
        ebook_config.AVAILABLE_EBOOK_LIST_CSV
    )
    dump_available_ebooks(available_books, ebook_config.AVAILABLE_EBOOK_LIST_TXT)


#######################################################################################
if __name__ == "__main__":
    main()
