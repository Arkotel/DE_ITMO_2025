import pandas as pd
import requests
from pathlib import Path


def get_data_path():
    """Возвращает путь к папке data"""
    return Path(__file__).parent.parent / "data"


def ensure_data_dir():
    """Создает папку data если её нет"""
    data_path = get_data_path()
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path


def download_csv(FILE_ID, filename="dataset.csv"):
    """Скачивает файл с Google Drive"""
    data_path = ensure_data_dir()
    file_url = f"https://drive.google.com/uc?id={FILE_ID}"

    response = requests.get(file_url)
    file_path = data_path / filename

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Датасет скачан в: {file_path}")
    return file_path


def check_file_exists(filename="dataset.csv"):
    """Проверяет существует ли файл"""
    data_path = get_data_path()
    file_path = data_path / filename
    return file_path.exists()


def load_data(FILE_ID, filename="dataset.csv"):
    """Загружает данные из csv файла"""
    data_path = get_data_path()
    file_path = data_path / filename

    # Если файла нет - скачиваем
    if not file_path.exists():
        print("Скачиваем файл...")
        file_path = download_csv(FILE_ID, filename)
    else:
        print(f"Файл найден: {file_path}")

    # Загружаем данные
    return pd.read_csv(file_path)
