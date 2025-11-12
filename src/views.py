#src/views.py
import pprint

from src.utils import (get_greeting, range_of_date, read_transactions_from_excel_file,
                       range_of_transactions, top_five_transactions_per_card, short_information_about_cards)
from typing import Dict


def main_view(user_input: str) -> Dict[str, str|float] | str:
    """Function for creating json-response for a bank service"""
    dates = range_of_date(user_input)
    total_transactions = read_transactions_from_excel_file()
    user_choice = range_of_transactions(total_transactions, dates)
    # получение топ 5 транзакций
    top_5 = top_five_transactions_per_card(user_choice)
    cards = short_information_about_cards(user_choice)

    result = {

        "greeting": get_greeting(),
        "cards": cards,
        "top_transactions": top_5,
        "currency_rates": None,
        "stock_prices": None

    }

    return result

if __name__ == "__main__":
    r = main_view("2020.04.30 10:00:00")
    pprint.pprint(r)