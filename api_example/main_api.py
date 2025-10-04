import pandas as pd
import os
from api_user_input import get_character_count
from api_loader import download_api
from api_loader import download_image
from api_loader import cleanup_api_dir
from api_saver import api_to_csv


def main():

    print(
        "! Данный код выполняет выгрузку данных API в csv, "
        "а также выгрузку изображений."
    )
    print(
        "! Для избежания перегруза памяти компьютера, "
        "максимальное количество запрашиваемых данных - 10"
    )
    print(
        "! Данное число можно изменить в файле api_user_input.py "
        "на усмотрение пользователя."
    )

    try:
        count = get_character_count()

        if count <= 0:
            print(f"Будет загружено: {count} персонажей")
            return

        cleanup_api_dir()

        api_dataset_raw = download_api(count)
        if not api_dataset_raw:
            print("Не удалось загрузить данные")
            return

        downloaded_images = 0
        total_count = len(api_dataset_raw)

        for i, character in enumerate(api_dataset_raw, 1):
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

        print(f"\n{downloaded_images} из {total_count} изображений скачано")  # noqa

        print("Типы данных до обработки")
        raw_df = pd.DataFrame(api_dataset_raw)
        for column in raw_df.columns:
            dtype = raw_df[column].dtype
            print(f"  {column}: {dtype}")
        print(raw_df.head())

        print("Данные после обработки")
        api_dataset = api_to_csv(api_dataset_raw)
        for column in api_dataset.columns:
            dtype = api_dataset[column].dtype
            print(f"  {column}: {dtype}")
        print(api_dataset.head())

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
