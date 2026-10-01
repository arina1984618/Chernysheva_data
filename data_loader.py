import gdown
import pandas as pd


def load_data():
    """Скачивает датасет с Google Drive и выводит первые 10 строк."""
    url = "https://drive.google.com/uc?id=1iOyw7Rz_kGZGv8rAWYI_BTcNWe-8wEDT"
    output = "heart_disease.csv"
    gdown.download(url, output, quiet=False)

    df = pd.read_csv(output)
    print(df.head(10))
    return df


if __name__ == '__main__':
    load_data()
