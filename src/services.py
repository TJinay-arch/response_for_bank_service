import json
import logging
from typing import Dict, List

# Настройка логгера
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def user_finder(
    user_input: str, transactions: List[Dict[str, str | float]]
) -> Dict[str, str | float] | str:
    """Function return a set of transactions based on the users input

    Args:
        user_input (str): The search term to look for in 'Описание' or 'Категория'.
        transactions (List[Dict[str, Union[str, float]]]): List of transaction records.

    Returns:
        str: JSON-formatted string of matching transactions, or empty list as JSON if no matches.
    """
    logger.info(f"Starting search for user input: '{user_input}'")

    if not user_input or not isinstance(user_input, str):
        logger.error("Invalid user_input: must be a non-empty string.")
        raise ValueError("user_input must be a non-empty string.")

    if not isinstance(transactions, list):
        logger.error("Invalid transactions: must be a list of dictionaries.")
        raise TypeError("transactions must be a list of dictionaries.")

    list_of_data = []
    logger.debug(f"Searching through {len(transactions)} transactions")

    for item in transactions:
        description = item.get("Описание", "")
        category = item.get("Категория", "")

        if user_input in str(description):
            list_of_data.append(item)
            logger.debug(f"Match found in 'Описание': {description}")
        elif isinstance(category, str) and user_input in category:
            list_of_data.append(item)
            logger.debug(f"Match found in 'Категория': {category}")

    logger.info(f"Search completed. Found {len(list_of_data)} matching transactions.")
    response = json.dumps(list_of_data, indent=4, ensure_ascii=False)
    return response
