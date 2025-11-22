# src/utils.py
import json
import logging
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import Timestamp

# --- Настройка логгера ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаём handler для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создаём формат логов
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Добавляем handler к логгеру
if not logger.handlers:
    logger.addHandler(console_handler)

load_dotenv()
file_path = os.getenv("EXCEL_FILE_PATH")
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
user_settings_json = os.getenv("USER_SETTINGS_PATH")


def get_greeting() -> str:
    """Get greeting depends on time when user ran the program

    Returns: str
    """
    logger.info("Вызов функции get_greeting")
    try:
        current_time = datetime.now()
        logger.debug(f"Текущее время: {current_time}")

        if 6 <= current_time.hour < 12:
            greeting = "Доброе утро"
        elif 12 <= current_time.hour < 18:
            greeting = "Добрый день"
        elif 18 <= current_time.hour < 24:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        logger.info(f"Приветствие определено: {greeting}")
        return greeting
    except Exception as e:
        logger.error(f"Ошибка в get_greeting: {e}")
        raise


def range_of_date(input_date: str) -> tuple[datetime, datetime] | str:
    """Function create month range of dates based on the input date

    Args: str (users choice of date)
    Returns: tuple (range of dates)
    """
    logger.info(f"Вызов функции range_of_date с датой: {input_date}")
    try:
        current_date = datetime.strptime(input_date, "%Y.%m.%d %H:%M:%S")
        beginning_of_month_date = current_date.replace(
            day=1, hour=0, minute=0, second=0
        )
        logger.debug(f"Диапазон дат: с {beginning_of_month_date} по {current_date}")
        return beginning_of_month_date, current_date
    except ValueError as e:
        logger.error(f"Неверный формат даты: {input_date} — {e}")
        return "Неверный формат даты"


def read_transactions_from_excel_file() -> List[Dict[str, str | float]] | str:
    """Function reads an Excel file which contains data of transactions

    Returns: List[Dict[str, str|float]] (The list of transactions)
    """
    logger.info("Вызов функции read_transactions_from_excel_file")
    try:
        if not file_path:
            error_msg = "Путь к файлу Excel не задан в переменных окружения"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        if not os.path.exists(file_path):
            error_msg = f"Файл не найден: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        df = pd.read_excel(file_path)
        list_of_transactions = df.to_dict(orient="records")
        logger.info(
            f"Успешно загружено {len(list_of_transactions)} транзакций из {file_path}"
        )
        return list_of_transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {e}")
        raise


def range_of_transactions(
    transactions: List[Dict[str, str | float]],
    range_of_dates: tuple[datetime, datetime],
) -> List[Dict[str, str | float]]:
    """Function create a list of transactions within users range

    Args: List[Dict[str, str|float]] (input transactions)
          tuple[datetime,datetime] (range_of_dates)

    Returns: List[Dict[str, str|float]] (a list of transactions within users range)
    """
    logger.info("Вызов функции range_of_transactions")
    try:
        df = pd.DataFrame(transactions)
        df["Дата операции"] = pd.to_datetime(
            df["Дата операции"], format="%d.%m.%Y %H:%M:%S"
        )
        filtered_df = df[
            df["Дата операции"].between(
                range_of_dates[0], range_of_dates[1], inclusive="both"
            )
        ]
        users_df = filtered_df.to_dict(orient="records")
        logger.info(f"Отфильтровано {len(users_df)} транзакций по диапазону дат")
        return users_df
    except Exception as e:
        logger.error(f"Ошибка в range_of_transactions: {e}")
        raise


def top_five_transactions_per_card(
    filtered_range_of_transactions: List[Dict[str, str | float]],
) -> List[Dict[str, str | float]] | str:
    """Function create a list of top 5 transactions within users range

    Returns: List[Dict[str, str|float]] (top 5 transactions)
             str (if there is an KeyError exception)
    """
    logger.info("Вызов функции top_five_transactions_per_card")
    try:
        df = pd.DataFrame(filtered_range_of_transactions)
        df["Сумма операции"] = df["Сумма операции"].abs()
        top_5_transactions = df.nlargest(5, "Сумма операции")
        result = top_5_transactions.to_dict(orient="records")
        logger.info(f"Найдено топ-5 транзакций: {len(result)} записей")
        return result
    except KeyError as e:
        logger.error(f"Отсутствует ожидаемый столбец: {e}")
        return "Некорректная дата операции"
    except Exception as e:
        logger.error(f"Ошибка в top_five_transactions_per_card: {e}")
        raise


def short_information_about_cards(
    filtered_range_of_transactions: List[Dict[str, str | float]],
) -> List[Dict[str, str | float]] | str:
    """Function generates short information about card

    Returns: List[Dict[str, str|float]] (last 4 digits, total expenses and cashback)
             str (if there is an KeyError exception)
    """
    logger.info("Вызов функции short_information_about_cards")
    try:
        df = pd.DataFrame(filtered_range_of_transactions)
        df.fillna({"Номер карты": "Номер карты неизвестен"}, inplace=True)
        grouped_df = (
            df.groupby("Номер карты")
            .agg({"Сумма платежа": lambda x: x[x < 0].sum()})
            .reset_index()
        )
        grouped_df["Сумма платежа"] = grouped_df["Сумма платежа"].round(2)
        grouped_df["Кэшбэк"] = (grouped_df["Сумма платежа"].abs() * 0.01).round(2)
        result = grouped_df.to_dict(orient="records")
        logger.info(f"Сформирована сводка по {len(result)} картам")
        return result
    except KeyError as e:
        logger.error(f"Отсутствует ожидаемый столбец: {e}")
        return "Отсутствует поле 'Номер карты'"
    except Exception as e:
        logger.error(f"Ошибка в short_information_about_cards: {e}")
        raise


BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def fetch_exchange_rates() -> Dict[str, float]:
    """Function for getting current exchange rates

    Returns: Dict[str, float] (USD and EUR exchange rates)
    """
    logger.info("Вызов функции fetch_exchange_rates")
    try:
        if not API_KEY:
            error_msg = "API ключ для курсов валют не задан"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        params = {"base": "RUB", "symbols": "USD,EUR", "apikey": API_KEY}
        logger.debug(f"Запрос к API: {BASE_URL} с параметрами {params}")
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            logger.error(
                f"Ошибка API курсов валют: {response.status_code} — {response.text[:200]}"
            )
            raise RuntimeError(
                f"Ошибка при получении данных: {response.status_code}. Ответ сервера: {response.text[:100]}..."
            )

        rates = response.json().get("rates", {})
        if not rates:
            logger.warning("Ответ API не содержит данных о курсах")
            return {}

        rates_in_rub = {
            "USD": round(1 / rates["USD"], 2),
            "EUR": round(1 / rates["EUR"], 2),
        }
        logger.info(f"Получены курсы валют: {rates_in_rub}")
        return rates_in_rub
    except requests.Timeout:
        logger.error("Таймаут при запросе к API курсов валют")
        raise TimeoutError("Таймаут при запросе к API курсов валют")
    except requests.ConnectionError as e:
        logger.error(f"Ошибка подключения к API курсов валют: {e}")
        raise ConnectionError("Ошибка подключения к API курсов валют")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в fetch_exchange_rates: {e}")
        raise


def datetime_handler(obj):
    """Custom JSON serializer for datetime objects"""
    logger.debug(f"Сериализация объекта: {obj} типа {type(obj)}")
    if isinstance(obj, (Timestamp, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


DEFAULT_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
DEFAULT_BASE_URL = "https://api.twelvedata.com/price"
DEFAULT_TIMEOUT = 10


def fetch_stock_price(
    symbol: str,
    api_key: str = None,
    base_url: str = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Fetch current stock price for a given symbol.

    Returns: {"symbol": str, "price": float}
    """
    logger.info(f"Вызов fetch_stock_price с символом: {symbol}")
    if not symbol:
        logger.error("Stock symbol is required.")
        raise ValueError("Stock symbol is required.")

    api_key = api_key or DEFAULT_API_KEY
    base_url = base_url or DEFAULT_BASE_URL

    try:
        if not api_key:
            error_msg = "API key not set. Please configure TWELVE_DATA_API_KEY."
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        if not symbol:
            error_msg = "Stock symbol is required."
            logger.error(error_msg)
            raise ValueError(error_msg)

        params = {"symbol": symbol.strip().upper(), "apikey": api_key}
        logger.debug(f"Запрос к API акций: {base_url} с параметрами {params}")
        response = requests.get(base_url, params=params, timeout=timeout)

        if response.status_code != 200:
            error_msg = f"API request failed with status {response.status_code}: {response.text[:200]}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

        data = response.json()
        if "price" not in data:
            error_msg = f"Invalid response: missing 'price'. Got: {data}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        price = float(data["price"])
        result = {"symbol": symbol.upper(), "price": round(price, 2)}
        logger.info(f"Получена цена акции: {result}")
        return result

    except requests.Timeout as e:
        logger.error(f"Таймаут при запросе акций {symbol}: {e}")
        raise TimeoutError(f"Request timed out fetching {symbol}: {e}") from e
    except requests.ConnectionError as e:
        logger.error(f"Ошибка подключения при запросе акций {symbol}: {e}")
        raise ConnectionError(f"Connection failed for {symbol}: {e}") from e
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Ошибка обработки данных акций {symbol}: {e}")
        raise RuntimeError(f"Error processing transaction data: {e}") from e


def user_settings_reader() -> Dict[str, str]:
    """Function reads a json file which contains number of user stocks

    Returns: Dict[str, str] (The list of stocks)
    """
    logger.info(f"Вызов user_settings_reader, путь к файлу: {user_settings_json}")
    try:
        if not user_settings_json:
            error_msg = "Путь к user_settings.json не задан в переменных окружения"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        if not os.path.exists(user_settings_json):
            error_msg = f"Config file not found: {user_settings_json}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(user_settings_json, encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            error_msg = f"Expected dict, got {type(data).__name__}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Конфигурация успешно загружена: {list(data.keys())}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в конфигурации: {e}")
        raise ValueError(f"Invalid JSON in config file: {e}") from e
    except Exception as e:
        logger.error(f"Неизвестная ошибка при чтении конфигурации: {e}")
        raise
