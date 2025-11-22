import logging
from datetime import datetime
from typing import Optional

import pandas as pd

# Настройка логгера
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
        )
    )
    logger.addHandler(handler)


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> str:
    """
    Возвращает JSON-строку с транзакциями по категории за последние 3 месяца.

    Args:
        transactions (pd.DataFrame): DataFrame с транзакциями. Должен содержать 'Категория' и 'Дата операции'.
        category (str): Категория для фильтрации.
        date (Optional[str]): Дата в формате 'YYYY.MM.DD HH:MM:SS'. Если None — используется текущая дата.

    Returns:
        str: JSON-строка с отфильтрованными транзакциями.
    """
    logger.info(f"Вызов spending_by_category с категорией='{category}', дата='{date}'")

    if transactions.empty:
        logger.info("DataFrame пуст, возвращаем пустой список")
        return "[]"

    # Парсинг даты
    if date is None:
        reference_date = datetime.today()
        logger.debug(f"Дата не указана, используем текущую дату: {reference_date}")
    else:
        try:
            # Поддержка форматов: YYYY-MM-DD и YYYY.MM.DD HH:MM:SS
            if "-" in date:
                reference_date = datetime.strptime(date, "%Y-%m-%d")
            else:
                reference_date = datetime.strptime(date, "%Y.%m.%d %H:%M:%S")
            logger.debug(f"Парсинг даты успешен: {reference_date}")
        except ValueError as e:
            error_msg = "Date must be in 'YYYY-MM-DD' or 'YYYY.MM.DD HH:MM:SS' format"
            logger.error(f"{error_msg}: {e}")
            raise ValueError(error_msg) from e

    reference_date = datetime.combine(reference_date.date(), datetime.min.time())

    # Проверка на наличие столбца
    if "Дата операции" not in transactions.columns:
        logger.error("Отсутствует столбец 'Дата операции'")
        raise KeyError("Column 'Дата операции' not found in transactions")

    # Копирование и парсинг дат
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], dayfirst=True, errors="coerce"
    )
    df.dropna(subset=["Дата операции"], inplace=True)
    df["Дата операции"] = df["Дата операции"].dt.normalize()

    # Фильтрация по дате (последние 3 месяца)
    start_date = reference_date - pd.DateOffset(months=3)
    filtered = df[
        (df["Дата операции"] >= start_date)
        & (df["Дата операции"] <= reference_date)
        & (df["Категория"].str.lower() == category.lower())
    ]

    result = filtered.to_json(orient="records", date_format="iso")
    logger.info(f"Найдено {len(filtered)} транзакций по категории '{category}'")
    return result
