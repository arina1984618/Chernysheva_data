import os
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

API_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_crypto_data(vs_currency: str = "usd", per_page: int = 20) -> list:
    """Запрашивает данные о криптовалютах из CoinGecko API.

    Args:
        vs_currency: валюта для цен (по умолчанию USD).
        per_page: количество монет (по умолчанию 20).

    Returns:
        Список словарей с данными от API.
    """
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def to_dataframe(data: list) -> pd.DataFrame:
    """Преобразует ответ API в pandas DataFrame."""
    df = pd.DataFrame(data)

    # Оставляем нужные столбцы
    df = df[[
        "id", "symbol", "name", "current_price", "market_cap",
        "market_cap_rank", "total_volume", "high_24h", "low_24h",
        "price_change_24h", "price_change_percentage_24h",
        "circulating_supply", "ath", "atl",
    ]]

    # Приведение типов
    numeric_cols = [
        "current_price", "market_cap", "total_volume", "high_24h",
        "low_24h", "price_change_24h", "price_change_percentage_24h",
        "circulating_supply", "ath", "atl",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def save_parquet(df: pd.DataFrame, path: str = "crypto.parquet") -> None:
    """Сохраняет DataFrame в .parquet."""
    df.to_parquet(path, index=False)
    logger.info("Saved to %s", path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    data = fetch_crypto_data()
    df = to_dataframe(data)

    print(df.head(20))
    print(df.dtypes)

    save_parquet(df)
