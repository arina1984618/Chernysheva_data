import os
import gdown
import pandas as pd


def load_data():
    """Скачивает датасет с Google Drive и выводит первые 10 строк."""
    url = "https://drive.google.com/uc?id=1ohdg9wPXyRJ9rOEz6TwYtRnfX4qfkrhz"
    output = "heart_disease.csv"
    
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    df = pd.read_csv(output)
    print(df.head(10))
    return df


if __name__ == '__main__':
    load_data()
