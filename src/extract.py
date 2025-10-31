import os
import pandas as pd
import requests


def ensure_data_dir():
    """Создает папки data/raw если их нет"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(project_root, "data", "raw")
    os.makedirs(data_path, exist_ok=True)
    return data_path


def download_csv_from_GD(FILE_ID, filename="dataset.csv"):
    """Скачивает файл с Google Drive"""
    data_path = ensure_data_dir()
    file_url = f"https://drive.google.com/uc?id={FILE_ID}"

    response = requests.get(file_url)
    file_path = os.path.join(data_path, filename)

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


def load_data(file_path, sep=";"):
    """Загружает данные из csv файла"""
    raw_data = pd.read_csv(file_path, sep=sep)
    return raw_data


def get_data_path():
    """Возвращает путь к папке data/raw"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, "data", "raw")
