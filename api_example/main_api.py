import pandas as pd
import os
from api_user_input import get_character_count
from api_loader import download_api
from api_loader import download_image
from api_loader import cleanup_api_dir
from api_saver import api_to_csv, api_to_parquet

count_max_str = os.environ.get("COUNT_MAX")


def main():

    print(
        "! Данный код выполняет выгрузку данных API в csv, "
        "типизацию, сохранение в parquet, а также выгрузку изображений."
    )
    print(f"! Максимальное количество запрашиваемых данных - {count_max_str}")
    print("! Число можно изменить в environment.yml.")

    try:
        count = get_character_count()

        if count <= 0:
            print(f"Будет загружено: {count} персонажей")
            return

        cleanup_api_dir()

        raw_api_dataset = download_api(count)
        if not raw_api_dataset:
            print("Не удалось загрузить данные")
            return

        downloaded_images = 0
        total_count = len(raw_api_dataset)

        for i, character in enumerate(raw_api_dataset, 1):
            image_url = character.get("imageUrl")
            character_name = character.get("name", "Unknown")
            print(f"[{i}/{total_count}] {character_name}")

            if image_url:
                image_path = download_image(image_url, character_name)
                if image_path:
                    print(f"Успешно: {os.path.basename(image_path)}")
                    downloaded_images += 1
            else:
                print("Не удалось скачать")

        print(f"{downloaded_images} из {total_count} изображений скачано")  # noqa

        raw_api = api_to_csv(raw_api_dataset)
        print("Типы данных до обработки")
        raw_api = pd.DataFrame(raw_api_dataset)
        for column in raw_api.columns:
            dtype = raw_api[column].dtype
            print(f"  {column}: {dtype}")
        print(raw_api.head())

        api_dataset = api_to_parquet(raw_api_dataset)
        print("Данные после обработки")
        for column in api_dataset.columns:
            dtype = api_dataset[column].dtype
            print(f"  {column}: {dtype}")
        print(api_dataset.head())

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
