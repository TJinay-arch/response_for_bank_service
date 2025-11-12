import pytest
from typing import List, Dict
from pandas import Timestamp
import numpy as np


@pytest.fixture
def range_testing() -> str:
    """Fixture for testing range_of_date function"""
    return "2021.04.10 10:00:00"

@pytest.fixture
def read_excel_testing() -> List[Dict[str, str|float]]:
    """Fixture for testing read_transactions_from_excel_file function"""
    return [{'MCC': 5411.0,
             'Дата операции': '31.12.2021 16:44:00',
             'Сумма операции': -160.89,
             },
            {'MCC': 5411.0,
             'Дата операции': '31.12.2021 16:42:04',
             'Сумма операции': -64.0,
             },
            {'MCC': 5411.0,
             'Дата операции': '31.12.2021 16:39:04',
             'Сумма операции': -118.12
             }
            ]



@pytest.fixture(params=[[{'MCC': 7999.0,
  'Бонусы (включая кэшбэк)': 11,
  'Валюта операции': 'RUB',
  'Валюта платежа': 'RUB',
  'Дата операции': Timestamp('2021-04-01 01:07:59'),
  'Дата платежа': '01.04.2021',
  'Категория': 'Развлечения',
  'Кэшбэк': 11.0,
  'Номер карты': '*4556',
  'Округление на инвесткопилку': 0,
  'Описание': 'Яндекс.Афиша',
  'Статус': 'OK',
  'Сумма операции': -1100.0,
  'Сумма операции с округлением': 1100.0,
  'Сумма платежа': -1100.0}]])
def list_of_transactions(request):
    return request.param


np = np.nan
@pytest.fixture(params=[24292.61, 24292.61, 2063.73, 1116.0, 709.8])
def data_for_top_5_function(request) -> List[float]:
    return request.param


@pytest.fixture
def invalid_data_for_summing_transactions() -> List[Dict[str, str|float]]:
    return [
        {
            'Неверный ключ': '*7197',
            'Сумма платежа': -278.22
        },
        {
            'Неверный ключ': '*4556',
            'Сумма платежа': -250.00
        }
    ]