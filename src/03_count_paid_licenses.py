"""This module considers all orders and counts the number of ordered and 
   the number of ordered and paid instances of each available ebook.
   
   It generates a CSV file with the information.
"""


import ebook_config
import ebook_functions
import csv


#######################################################################################
def count_licenses(available_books, order_data):
    # init both counters for all books with zero
    for book in available_books:
        available_books[book]["Anzahl (bestellt)"] = 0
        available_books[book]["Anzahl (bezahlt)"] = 0

    # count!
    for pupil, data in order_data.items():
        try:
            if data["bezahlt"] == True:
                for lic in data["Lizenzen"]:
                    available_books[lic]["Anzahl (bestellt)"] += 1
                    available_books[lic]["Anzahl (bezahlt)"] += 1
        except:  # TODO: Use True/False rather than True/Exept
            print("License not paid for " + pupil + "...")
            for lic in data["Lizenzen"]:
                available_books[lic]["Anzahl (bestellt)"] += 1


#######################################################################################
def dump_ordered_licenses_csv(ordered_licenses, filename):
    # obtain fieldnames from first entry
    fieldnames = ordered_licenses[list(ordered_licenses)[0]]
    # dump data to csv
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, delimiter=";", extrasaction="ignore"
        )
        writer.writeheader()
        for id, value in ordered_licenses.items():
            writer.writerow(value)


#######################################################################################
def main():
    available_books = ebook_functions.get_available_books(
        ebook_config.AVAILABLE_EBOOK_LIST_CSV
    )
    order_data = ebook_functions.get_order_data_json(ebook_config.ORDER_DATA_JSON)
    count_licenses(available_books, order_data)
    dump_ordered_licenses_csv(available_books, ebook_config.PAID_AND_ORDERED_EBOOKS_CSV)


#######################################################################################
if __name__ == "__main__":
    main()
