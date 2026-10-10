import os
import gdown
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Целочисленные категориальные признаки
INT_COLS = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal", "num", "target_binary"]

# Вещественные (непрерывные) признаки
FLOAT_COLS = ["age", "trestbps", "chol", "thalach", "oldpeak"]


def load_data() -> pd.DataFrame:
    """Скачивает датасет с Google Drive и читает его в DataFrame."""
    url = "https://drive.google.com/uc?id=1iOyw7Rz_kGZGv8rAWYI_BTcNWe-8wEDT"
    output = "heart_disease.csv"

    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

    return pd.read_csv(output)


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """Приводит типы столбцов датасета к правильным."""
    df = df.copy()

    # Считаем NaN до приведения типов
    nan_before = df.isna().sum()

    for col in INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in FLOAT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # Считаем NaN после и находим «появившиеся»
    nan_after = df.isna().sum()
    new_nans = nan_after - nan_before
    new_nans = new_nans[new_nans > 0]

    if not new_nans.empty:
        logger.info("New NaN introduced by casting:\n%s", new_nans)
    else:
        logger.info("No new NaN values introduced by type casting.")

    return df


def save_parquet(df: pd.DataFrame, path: str = "heart_disease.parquet") -> None:
    """Сохраняет DataFrame в формат .parquet."""
    df.to_parquet(path, index=False)
    logger.info("Saved to %s", path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    df = load_data()
    df = cast_types(df)
    print(df.head(10))
    print(df.dtypes)
    save_parquet(df)
