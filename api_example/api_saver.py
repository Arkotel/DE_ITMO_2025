import pandas as pd
import os

m_dir = os.path.dirname(os.path.abspath(__file__))
API_DATA = os.path.join(m_dir, "api_data")
API_IMAGES = os.path.join(m_dir, "api_images")
OUTPUT_FILENAME = os.path.join(API_DATA, "disney_characters.csv")


def api_to_csv(data: list[dict]) -> pd.DataFrame | None:
    """Сохраняет данные о персонажах в CSV файл"""
    if not data:
        print("Ошибка. Данные отсутствуют")
        return None

    # Создаем папку если ее нет
    os.makedirs(API_DATA, exist_ok=True)

    api_dataset = pd.DataFrame(data)

    if "_id" in api_dataset.columns:
        api_dataset["_id"] = api_dataset["_id"].astype("int16")

    if "name" in api_dataset.columns:
        api_dataset["name"] = api_dataset["name"].astype("category")

    api_dataset.to_csv(OUTPUT_FILENAME, index=False)
    print(f"Данные сохранены в {OUTPUT_FILENAME}")

    return api_dataset
