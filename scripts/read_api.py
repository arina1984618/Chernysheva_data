from pathlib import Path
import time
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

API_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_crypto_data(vs_currency: str = "usd", per_page: int = 20) -> list[dict]:
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

    # Простой retry при 429 (Too Many Requests)
    for attempt in range(3):
        response = requests.get(API_URL, params=params, timeout=30)
        if response.status_code == 429:
            logger.warning("CoinGecko вернул 429, попытка %d/3, ждём 5 сек", attempt + 1)
            time.sleep(5)
            continue
        response.raise_for_status()
        return response.json()

    # Если все попытки исчерпаны
    response.raise_for_status()
    return []


def to_dataframe(data: list) -> pd.DataFrame:
    """Преобразует ответ API в pandas DataFrame."""
    df = pd.DataFrame(data)

    # Оставляем нужные столбцы (reindex не упадёт, если чего-то нет)
    df = df.reindex(columns=[
        "id", "symbol", "name", "current_price", "market_cap",
        "market_cap_rank", "total_volume", "high_24h", "low_24h",
        "price_change_24h", "price_change_percentage_24h",
        "circulating_supply", "ath", "atl",
    ])

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


def save_parquet(df: pd.DataFrame, path: str = "data/crypto.parquet") -> None:
    """Сохраняет DataFrame в .parquet, создавая папку при необходимости."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    logger.info("Saved to %s", path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    data = fetch_crypto_data()
    if not data:
        logger.error("CoinGecko вернул пустой список")
        raise SystemExit(1)
    logger.info("Получено %d монет", len(data))

    df = to_dataframe(data)
    logger.info("\n%s", df.head(20))
    logger.info("\n%s", df.dtypes)

    save_parquet(df)
