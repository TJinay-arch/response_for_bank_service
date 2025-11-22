from unittest.mock import patch

from src.views import main_view


def test_main_view_success():
    """Test that main_view returns correct JSON structure with mocked data."""
    with patch("src.views.get_greeting", return_value="Доброе утро"), patch(
        "src.views.range_of_date", return_value=("2025-01-01", "2025-01-31")
    ), patch("src.views.read_transactions_from_excel_file") as mock_read, patch(
        "src.views.range_of_transactions"
    ) as mock_range, patch(
        "src.views.top_five_transactions_per_card"
    ) as mock_top5, patch(
        "src.views.short_information_about_cards"
    ) as mock_cards, patch(
        "src.views.fetch_exchange_rates", return_value={"USD": 75.0, "EUR": 85.0}
    ), patch(
        "src.views.user_settings_reader", return_value={"user_stocks": ["AAPL"]}
    ), patch(
        "src.views.fetch_stock_price", return_value={"price": 150.25}
    ):

        # Mock transaction data flow
        mock_read.return_value = [{"Дата операции": "2025-01-15"}]
        mock_range.return_value = [{"Дата операции": "2025-01-15"}]
        mock_top5.return_value = [{"amount": 1000}]
        mock_cards.return_value = [{"last_digits": "1234", "total_spent": 5000}]

        result = main_view("2025-01-15")

        assert isinstance(result, str)  # JSON string
        assert "Доброе утро" in result
        assert "USD" in result
        assert "AAPL" in result
        assert "150.25" in result


def test_main_view_empty_transactions():
    """Test main_view handles empty transaction list gracefully."""
    with patch("src.views.get_greeting", return_value="Добрый день"), patch(
        "src.views.range_of_date", return_value=("2025-01-01", "2025-01-31")
    ), patch("src.views.read_transactions_from_excel_file", return_value=[]), patch(
        "src.views.range_of_transactions", return_value=[]
    ), patch(
        "src.views.top_five_transactions_per_card", return_value=[]
    ), patch(
        "src.views.short_information_about_cards", return_value=[]
    ), patch(
        "src.views.fetch_exchange_rates", return_value={}
    ), patch(
        "src.views.user_settings_reader", return_value={"user_stocks": []}
    ), patch(
        "src.views.fetch_stock_price", return_value={"price": 0}
    ):

        result = main_view("2025-01-10")

        assert isinstance(result, str)
        assert "Добрый день" in result
        assert '"cards": []' in result
        assert '"top_transactions": []' in result
        assert '"currency_rates": {}' in result
        assert '"stock_prices": []' in result
