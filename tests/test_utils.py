#tests/test_utils.py
from unittest.mock import patch
import pandas as pd
from src.utils import (get_greeting, range_of_date, read_transactions_from_excel_file,
                       range_of_transactions, top_five_transactions_per_card, short_information_about_cards)
import pytest
from datetime import datetime


@pytest.mark.parametrize("hour, expected_greeting", [
    (10, 'Доброе утро'),
    (12, 'Добрый день'),
    (19, 'Добрый вечер'),
    (00, 'Доброй ночи')
]
                         )
def test_get_greeting(hour: int, expected_greeting: str) -> None:
    """Test for get_greeting function"""
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, hour, 0, 0)
        result = get_greeting()
        assert result == expected_greeting


def test_range_of_date(range_testing) -> None:
    """Test for range_of_date"""
    result = range_of_date(range_testing)
    string_date_start = result[0].strftime("%Y.%m.%d %H:%M:%S")
    string_date_end = result[1].strftime("%Y.%m.%d %H:%M:%S")
    assert f"{string_date_start}, {string_date_end}" == "2021.04.01 00:00:00, 2021.04.10 10:00:00"

    invalid_input = "2021.04.10"
    assert range_of_date(invalid_input) == "Неверный формат даты"


def test_read_transactions_from_excel_file(read_excel_testing) -> None:
    """Test for read_transactions_from_excel_file (standard)"""
    example_df = pd.DataFrame(read_excel_testing)

    with patch('src.utils.pd.read_excel') as mock_pandas:
        mock_pandas.return_value = example_df
        result = read_transactions_from_excel_file()

    assert result[0] == {'MCC': 5411.0,
                         'Дата операции': '31.12.2021 16:44:00',
                         'Сумма операции': -160.89
                         }
@patch('pandas.read_excel', side_effect=FileNotFoundError("Некорректный путь"))
def test_invalid_path(mock_read_excel) -> None:
    """Test for read_transactions_from_excel_file (invalid file path)"""
    with pytest.raises(FileNotFoundError):
        pd.read_excel('missing.xlsx')


def test_range_of_transactions(list_of_transactions) -> None:
    """Test for range_of_transactions"""
    list_excel = read_transactions_from_excel_file()
    band = range_of_date('2021.03.01 10:00:00')
    assert range_of_transactions(list_excel, band) == []
    band_2 = range_of_date('2021.04.01 10:00:00')
    assert range_of_transactions(list_excel, band_2) == list_of_transactions


def test_top_5_transactions_per_card(data_for_top_5_function) -> None:
    """Test for top_5_transactions function"""
    list_excel = read_transactions_from_excel_file()
    band = range_of_date('2020.04.30 10:00:00')
    tr = range_of_transactions(list_excel, band)
    result = top_five_transactions_per_card(tr)

    assert any(item['Сумма операции'] == data_for_top_5_function for item in result)


import pytest


@pytest.mark.parametrize(
            "test_data,expected",
            [
                (
                        # Входные данные: список транзакций
                        [
                            {
                                'Номер карты': '*7197',
                                'Сумма платежа': -278.22,
                                'Другое поле': 'игнорируется'
                            },
                            {
                                'Номер карты': '*7197',
                                'Сумма платежа': -266.32,
                                'Другое поле': 'игнорируется'
                            },
                            {
                                'Номер карты': '*4556',
                                'Сумма платежа': -250.00,
                                'Другое поле': 'игнорируется'
                            },
                            {
                                'Номер карты': None,  # превратится в «Номер карты неизвестен»
                                'Сумма платежа': -340.00,
                                'Другое поле': 'игнорируется'
                            }
                        ],
                        # Ожидаемый результат (после группировки и расчёта кэшбэка)
                        [
                            {
                                'Номер карты': '*7197',
                                'Сумма платежа': -544.54,
                                'Кэшбэк': 5.45
                            },
                            {
                                'Номер карты': '*4556',
                                'Сумма платежа': -250.00,
                                'Кэшбэк': 2.50
                            },
                            {
                                'Номер карты': 'Номер карты неизвестен',
                                'Сумма платежа': -340.00,
                                'Кэшбэк': 3.40
                            }
                        ]
                )
            ]
)
def test_short_information_about_cards_positive(test_data, expected):
    """Testing short_information_about_cards_positive function with correct input"""

    result = short_information_about_cards(test_data)

    assert isinstance(result, list)
    assert len(result) == len(expected)

    result_sorted = sorted(result, key=lambda x: x['Номер карты'])
    expected_sorted = sorted(expected, key=lambda x: x['Номер карты'])

    for i in range(len(result_sorted)):
        assert result_sorted[i]['Номер карты'] == expected_sorted[i]['Номер карты'], \
            f"Не совпадает Номер карты на позиции {i}"
        assert abs(result_sorted[i]['Сумма платежа'] - expected_sorted[i]['Сумма платежа']) < 0.01, \
            f"Не совпадает Сумма платежа на позиции {i}"
        assert abs(result_sorted[i]['Кэшбэк'] - expected_sorted[i]['Кэшбэк']) < 0.01, \
            f"Не совпадает Кэшбэк на позиции {i}"


def test_short_information_about_cards_key_error(invalid_data_for_summing_transactions):
    """Testing short_information_about_cards_positive function with invalid input"""

    result = short_information_about_cards(invalid_data_for_summing_transactions)

    assert isinstance(result, str)
    assert result == "Отсутствует поле 'Номер карты'"









