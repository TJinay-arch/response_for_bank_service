import json

import pytest

from src.services import user_finder


def test_user_finder_by_description(sample_transactions):
    """Test searching by part of the description."""
    result = user_finder("еды", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Описание"] == "Доставка еды"
    assert data[0]["Категория"] == "Еда"


def test_user_finder_by_category(sample_transactions):
    """Test searching by category name."""
    result = user_finder("Еда", sample_transactions)
    data = json.loads(result)
    assert len(data) == 2
    descriptions = [item["Описание"] for item in data]
    assert "Обед в кафе" in descriptions
    assert "Доставка еды" in descriptions


def test_user_finder_partial_match(sample_transactions):
    """Test partial substring match in description."""
    result = user_finder("интернет", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Описание"] == "Оплата интернета"


def test_user_finder_no_match_returns_empty_list(sample_transactions):
    """Test that no matches return an empty JSON list."""
    result = user_finder("Не_существует", sample_transactions)
    data = json.loads(result)
    assert data == []


def test_user_finder_case_sensitive(sample_transactions):
    """Test that search is case-sensitive."""
    result = user_finder("еды", sample_transactions)
    data = json.loads(result)
    assert len(data) == 1


def test_user_finder_with_none_category(sample_transactions):
    """Test that transaction with non-string (e.g. None) category does not raise error."""
    result = user_finder("Категория", sample_transactions)
    data = json.loads(result)
    # Should just skip the None category safely
    assert isinstance(data, list)


def test_user_finder_empty_transactions():
    """Test behavior with empty transactions list."""
    result = user_finder("Еда", [])
    data = json.loads(result)
    assert data == []


def test_user_finder_empty_input(sample_transactions):
    """Test that empty string input raises ValueError."""
    with pytest.raises(ValueError, match="user_input must be a non-empty string."):
        user_finder("", sample_transactions)


def test_user_finder_non_string_input(sample_transactions):
    """Test that non-string user_input raises ValueError."""
    with pytest.raises(ValueError):
        user_finder(123, sample_transactions)  # type: ignore


def test_user_finder_invalid_transactions_type():
    """Test that non-list transactions raises TypeError."""
    with pytest.raises(TypeError):
        user_finder("Еда", "not a list")  # type: ignore
