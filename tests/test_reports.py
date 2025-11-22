from io import StringIO

import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def sample_transactions_for_3_months():
    """Фикстура с тестовыми данными."""
    return pd.DataFrame(
        [
            {"Дата операции": "15.03.2025", "Категория": "Еда", "Сумма": 300},
            {"Дата операции": "10.04.2025", "Категория": "Еда", "Сумма": 120},
            {"Дата операции": "05.05.2025", "Категория": "Еда", "Сумма": 80},
            {"Дата операции": "20.05.2025", "Категория": "Еда", "Сумма": 95},
            {"Дата операции": "10.01.2025", "Категория": "Еда", "Сумма": 200},
            {"Дата операции": "14.02.2025", "Категория": "Еда", "Сумма": 130},
            {"Дата операции": "03.03.2025", "Категория": "Еда", "Сумма": 110},
            {"Дата операции": "28.02.2025", "Категория": "Транспорт", "Сумма": 60},
        ]
    )


@pytest.mark.parametrize(
    "invalid_date",
    ["2025/01/01", "01-01-2025", "not-a-date", ""],
)
def test_spending_by_category_invalid_date(
    sample_transactions_for_3_months, invalid_date
):
    """Тест: некорректный формат даты вызывает ValueError."""
    with pytest.raises(
        ValueError, match="Date must be in 'YYYY-MM-DD' or 'YYYY.MM.DD HH:MM:SS' format"
    ):
        spending_by_category(sample_transactions_for_3_months, "Еда", invalid_date)


def test_spending_by_category_missing_column(sample_transactions_for_3_months):
    """Тест: отсутствие столбца 'Дата операции' вызывает KeyError."""
    df = sample_transactions_for_3_months.drop(columns=["Дата операции"])
    with pytest.raises(
        KeyError, match="Column 'Дата операции' not found in transactions"
    ):
        spending_by_category(df, "Еда", "2025-06-01")


def test_spending_by_category_empty_df():
    """Тест: пустой DataFrame возвращает пустой JSON."""
    empty_df = pd.DataFrame()
    result = spending_by_category(empty_df, "Еда", "2025-06-01")
    assert result == "[]"


def test_spending_by_category_case_insensitive():
    """Тест: фильтрация по категории без учёта регистра."""
    df = pd.DataFrame(
        {
            "Дата операции": ["10.05.2025", "15.04.2025"],
            "Категория": ["ЕДА", "еда"],
            "Сумма": [100, 200],
        }
    )
    result = spending_by_category(df, "Еда", "2025-06-01")
    df_result = pd.read_json(StringIO(result))
    assert len(df_result) == 2


def test_spending_by_category_invalid_dates():
    """Тест: строки с невалидными датами удаляются."""
    df = pd.DataFrame(
        {
            "Дата операции": ["10.05.2025", "invalid-date", "01.04.2025"],
            "Категория": ["Еда", "Еда", "Еда"],
            "Сумма": [100, 200, 150],
        }
    )
    result = spending_by_category(df, "Еда", "2025-06-01")
    df_result = pd.read_json(StringIO(result))
    assert len(df_result) == 2
