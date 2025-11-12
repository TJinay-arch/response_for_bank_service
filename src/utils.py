#src/utils.py
import pprint
from datetime import datetime
from typing import List, Dict
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
file_path = os.getenv('EXCEL_FILE_PATH')

def get_greeting() -> str:
    """Get greeting depends on time when user ran the program

       Args: None

       Returns: str

       Raises: None
       """

    current_time = datetime.now()

    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def range_of_date(input_date: str) -> tuple[datetime, datetime] | str:
    """Function create month range of dates based on the input date

       Args: str (users choice of date)
       Returns: tuple (range of dates)
       """
    try:
        current_date = datetime.strptime(input_date, "%Y.%m.%d %H:%M:%S")
        beginning_of_month_date = current_date.replace(day=1, hour=0, minute=0, second=0)

        return beginning_of_month_date, current_date
    except ValueError:
        return "Неверный формат даты"



def read_transactions_from_excel_file() -> List[Dict[str, str|float]] | str:
    """Function reads an Excel file which contains data of transactions
       Args: None
       Returns: List[Dict[str, str|float]] (The list of transactions)
       """
    if not os.path.exists(file_path):
        raise FileNotFoundError("Некорректный путь")

    df = pd.read_excel(file_path)
    list_of_transactions = df.to_dict(orient='records')
    return list_of_transactions


def range_of_transactions(transactions:List[Dict[str, str|float]], range_of_dates: tuple[datetime,datetime]) -> List[Dict[str, str|float]]:
    """Function create a list of transactions within users range

       Args: List[Dict[str, str|float]] (input transactions)
             tuple[datetime,datetime] (range_of_dates)

       Returns: List[Dict[str, str|float]] (a list of transactions within users range)
       """
    df = pd.DataFrame(transactions)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")
    filtered_df = df[df['Дата операции'].between(range_of_dates[0], range_of_dates[1], inclusive='both')]
    users_df = filtered_df.to_dict(orient='records')

    return users_df


def top_five_transactions_per_card(filtered_range_of_transactions:List[Dict[str, str|float]]) -> List[Dict[str, str|float]] | str:
    """Function create a list of top 5 transactions within users range

       Args: List[Dict[str, str|float]] (input transactions)

       Returns: List[Dict[str, str|float]] (a list of transactions within users range)
                str (if there is an KeyError exception)
       """
    try:
        df = pd.DataFrame(filtered_range_of_transactions)
        df['Сумма операции'] = df['Сумма операции'].abs() # получаем абсолютные столбца "Сумма операции"
        top_5_transactions = df.nlargest(5, 'Сумма операции')
        return top_5_transactions.to_dict(orient='records')
    except KeyError:
        return "Некорректная дата операции"

def sum_negative(group):
    return group[group['Значение'] < 0]['Значение'].sum()

def short_information_about_cards(filtered_range_of_transactions:List[Dict[str, str|float]]) -> List[Dict[str, str|float]] | str:
    """Function generates short information about card

       Args: List[Dict[str, str|float]] (input transactions)

       Returns: List[Dict[str, str|float]] (a list of information about transactions within users range:
                last four digits, total expenses and cashback)

                str (if there is an KeyError exception)"""
    try:
        df = pd.DataFrame(filtered_range_of_transactions)
        df.fillna({'Номер карты': 'Номер карты неизвестен'}, inplace=True)
        grouped_df = df.groupby('Номер карты').agg({'Сумма платежа': lambda x: x[x < 0].sum()}).reset_index()
        grouped_df['Сумма платежа'] = grouped_df['Сумма платежа'].round(2)
        grouped_df['Кэшбэк'] = (grouped_df['Сумма платежа'].abs() * 0.01).round(2)

        return grouped_df.to_dict(orient='records')
    except KeyError:
        return "Отсутствует поле 'Номер карты'"

if __name__ == "__main__":
    greeting = get_greeting()
    print(greeting)
    a = input("Введите дату в формате YYYY-MM-DD HH:MM:SS\n")
    b = range_of_date(a)
    c = read_transactions_from_excel_file()
    result = range_of_transactions(c, b)
    #top_5 = top_five_transactions_per_card(result)
    cards = short_information_about_cards(result)
    pprint.pprint(result)
    pprint.pprint(cards)