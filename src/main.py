import json
import pprint

import pandas as pd

from src.reports import spending_by_category
from src.services import user_finder
from src.utils import read_transactions_from_excel_file
from src.views import main_view

if __name__ == "__main__":
    response = main_view("2021.04.30 10:00:00")
    print("Функциональность 1\n")
    pprint.pprint(json.loads(response))
    print("\n\n")

    transactions = read_transactions_from_excel_file()
    user_choice = "Колхоз"
    set_of_transactions = user_finder(user_choice, transactions)
    print("Функциональность 2\n")
    pprint.pprint(json.loads(set_of_transactions))
    print("\n\n")

    transactions_for_report = pd.DataFrame(transactions)
    category_report = "Супермаркеты"
    date_for_report = "2021.04.30 10:00:00"
    report = spending_by_category(
        transactions_for_report, category_report, date_for_report
    )
    print("Функциональность 3\n")
    pprint.pprint(json.loads(report))
