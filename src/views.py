# src/views.py
import json
from typing import Dict

from src.utils import (datetime_handler, fetch_exchange_rates,
                       fetch_stock_price, get_greeting, range_of_date,
                       range_of_transactions,
                       read_transactions_from_excel_file,
                       short_information_about_cards,
                       top_five_transactions_per_card, user_settings_reader)


def main_view(user_input: str) -> Dict[str, str | float] | str:
    """Function for creating json-response for a bank service"""
    dates = range_of_date(user_input)
    total_transactions = read_transactions_from_excel_file()
    user_choice = range_of_transactions(total_transactions, dates)
    # получение топ 5 транзакций
    top_5 = top_five_transactions_per_card(user_choice)
    cards = short_information_about_cards(user_choice)
    currency_rates = fetch_exchange_rates()
    # получение данных по акциям
    list_of_stocks = user_settings_reader()["user_stocks"]
    stock_prices = []
    for symbol in list_of_stocks:
        response = fetch_stock_price(symbol)
        price = response["price"]

        modified_format_of_data = {"stock": symbol, "price": price}

        stock_prices.append(modified_format_of_data)

    result = {
        "greeting": get_greeting(),
        "cards": cards,
        "top_transactions": top_5,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    json_response = json.dumps(
        result, ensure_ascii=False, indent=4, default=datetime_handler
    )

    return json_response
