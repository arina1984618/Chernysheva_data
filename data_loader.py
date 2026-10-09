import os
import gdown
import pandas as pd


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

    # Целочисленные категориальные признаки
    int_cols = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal", "num", "target_binary"]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    # Вещественные признаки
    float_cols = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].astype("float64")

    return df


def save_parquet(df: pd.DataFrame, path: str = "heart_disease.parquet") -> None:
    """Сохраняет DataFrame в формат .parquet."""
    df.to_parquet(path, index=False)
    print(f"Saved to {path}")


if __name__ == '__main__':
    df = load_data()
    df = cast_types(df)
    print(df.head(10))
    print(df.dtypes)
    save_parquet(df)
