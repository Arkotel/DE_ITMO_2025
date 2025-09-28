import pandas as pd
from data_loader import load_data, get_data_path, check_file_exists
from data_processing import conv_data

FILE_ID = "1gJrXyvqIVSZCEjqhGhvisyMyxI0zBald"  # ID файла на Google Drive

# --- Пути к файлам ---
data_path = get_data_path()
parquet_path = data_path / "proc_data.parquet"
csv_path = data_path / "dataset.csv"

# Проверяем наличие .parquet файла
if check_file_exists("proc_data.parquet"):
    print("Найден файл .parquet")
    proc_data = pd.read_parquet(parquet_path)
    print("\nОбработанные данные:")
    print(proc_data.info())

else:
    print("Файл .parquet не найден")

    # Проверяем наличие CSV файла
    if check_file_exists("dataset.csv"):
        print("Найден dataset.csv")
        raw_data = load_data(FILE_ID)
    else:
        print("Файл dataset.csv не найден")
        raw_data = load_data(FILE_ID)

    # --- Обработка данных ---
    proc_data = conv_data(raw_data)

    # --- Сохранение обработанных данных в Parquet ---
    proc_data.to_parquet(parquet_path, index=False)
    print(f"Обработанные данные сохранены в: {parquet_path}")
