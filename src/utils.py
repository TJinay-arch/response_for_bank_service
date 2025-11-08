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



def read_transactions_from_excel_file() -> List[Dict[str, str|float]]:
    """Function reads an Excel file which contains data of transactions
       Args: None
       Returns: List[Dict[str, str|float]] (The list of transactions)
       """

    df = pd.read_excel(file_path).head(3)
    list_of_transactions = df.to_dict(orient='records')
    return list_of_transactions


if __name__ == "__main__":
    pprint.pprint(read_transactions_from_excel_file())
