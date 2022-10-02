"""This module generates a JSON file, that contains an entry for
   each available ebook. It contains placeholders to which licences from
   the publishers can be inserted and afterwards be sent.
"""

import ebook_config
import ebook_functions
import json

#######################################################################################
def main():
    available_books = ebook_functions.get_available_books(
        ebook_config.AVAILABLE_EBOOK_LIST_CSV
    )

    ebook_licenses = {}
    for id, book_data in available_books.items():
        ebook_licenses[id] = {}
        ebook_licenses[id]["Buchbezeichnung"] = book_data["Buchbezeichnung"]
        ebook_licenses[id]["Verlag"] = book_data["Verlag"]
        ebook_licenses[id]["vergebeneLizenzen"] = 0
        ebook_licenses[id]["Lizenzschluessel"] = []

    json_string = json.dumps(ebook_licenses, indent=4)
    with open(ebook_config.EBOOK_LICENSES_JSON, "w") as f:
        print(json_string, file=f)


#######################################################################################
if __name__ == "__main__":
    main()
