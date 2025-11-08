#tests/test_utils.py
from unittest.mock import patch
from src.utils import get_greeting, range_of_date
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


def test_range_of_date(range_testing):
    """Test for range_of_date"""
    result = range_of_date(range_testing)
    string_date_start = result[0].strftime("%Y.%m.%d %H:%M:%S")
    string_date_end = result[1].strftime("%Y.%m.%d %H:%M:%S")
    assert f"{string_date_start}, {string_date_end}" == "2021.04.01 00:00:00, 2021.04.10 10:00:00"

    invalid_input = "2021.04.10"
    assert range_of_date(invalid_input) == "Неверный формат даты"