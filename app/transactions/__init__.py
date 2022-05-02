""" transactions module """
from csv import DictReader
import logging
from app.db.models import Transaction, TransactionTypeEnum

def open_and_parse_csv(filepath):
    """ utility function to open and parse a CSV """
    transaction_list = []
    log = logging.getLogger("misc_debug")

    with open(filepath, encoding="utf-8-sig" ) as file:
        csv_table = DictReader(file, dialect='excel')
        log.info("CSV: %s, Fieldnames: %s", filepath, csv_table.fieldnames)

        # TODO check CSV for proper headers
        csv_header = Transaction.csv_headers()
        for row in csv_table:
            amount = row[csv_header[0]]
            transaction_type = TransactionTypeEnum[row[csv_header[1]]]

            transaction_list.append(Transaction(amount, transaction_type))

    return transaction_list
    