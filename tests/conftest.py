import pytest
from typing import List, Dict


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