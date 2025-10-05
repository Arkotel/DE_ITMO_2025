import pandas as pd
import os

m_dir = os.path.dirname(os.path.abspath(__file__))
API_DATA = os.path.join(m_dir, "api_data")
API_IMAGES = os.path.join(m_dir, "api_images")
OUTPUT_CSV = os.path.join(API_DATA, "disney_characters.csv")
OUTPUT_PARQUET = os.path.join(API_DATA, "disney_characters.parquet")


def api_to_csv(data: list[dict]) -> pd.DataFrame | None:
    """Сохраняет данные о персонажах в CSV файл"""
    if not data:
        print("Ошибка. Данные отсутствуют")
        return None

    # Создаем папку если ее нет
    os.makedirs(API_DATA, exist_ok=True)

    raw_api_dataset = pd.DataFrame(data)
    raw_api_dataset.to_csv(OUTPUT_CSV, index=False)
    print(f"\nДанные сохранены в {OUTPUT_CSV}")

    return raw_api_dataset


def api_to_parquet(data: list[dict]) -> pd.DataFrame | None:
    """Сохраняет типизированные данные в Parquet"""
    if not data:
        print("Ошибка. Данные отсутствуют")
        return None

    os.makedirs(API_DATA, exist_ok=True)

    api_dataset = pd.DataFrame(data)

    if "_id" in api_dataset.columns:
        api_dataset["_id"] = api_dataset["_id"].astype("int16")

    if "name" in api_dataset.columns:
        api_dataset["name"] = api_dataset["name"].astype("category")

    api_dataset.to_parquet(OUTPUT_PARQUET, index=False)
    print(
        f"\nОбработанные данные сохранены в {os.path.basename(OUTPUT_PARQUET)}"
    )  # noqa

    return api_dataset
