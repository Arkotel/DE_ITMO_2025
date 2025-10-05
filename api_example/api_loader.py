import requests
from tqdm import tqdm
import time
import os

url = "https://disneyapi.dev"
API_URL = "https://api.disneyapi.dev/character"

m_dir = os.path.dirname(os.path.abspath(__file__))
API_DATA = os.path.join(m_dir, "api_data")
API_IMAGES = os.path.join(m_dir, "api_images")


def ensure_api_dir():
    """Создаем папки, если они не существуют"""
    print("Папки для хранения данных API созданы")
    os.makedirs(API_DATA, exist_ok=True)
    os.makedirs(API_IMAGES, exist_ok=True)


def cleanup_api_dir():
    """Очищаем папки перед новым запуском"""
    for folder in [API_DATA, API_IMAGES]:
        if os.path.exists(folder):  # Если папка существует
            for filename in os.listdir(folder):  # Смотрим все файлы в папке
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):  # Если это файл (а не папка)
                    os.remove(file_path)  # Удаляем файл
                    print(f"Удалили: {filename}")
    print("Папки пусты. Загружаем данные")


def download_image(image_url: str, character_name: str) -> str:
    """Скачиваем изображение персонажа и сохраняем в api_images"""

    if not image_url:
        return None

    try:
        # Создаем имя файла и определяем расширение
        img_name = character_name.replace(" ", "_")
        if ".png" in image_url.lower():
            extension = ".png"
        else:
            extension = ".jpg"

        filename = f"{img_name}{extension}"
        filepath = os.path.join(API_IMAGES, filename)

        # Скачиваем изображение
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath
        else:
            return None

    except Exception as e:
        print(f"Ошибка при скачивании изображения {character_name}: {e}")
        return None


def download_api(count: int) -> list[dict]:
    """Загружаем указанное количество персонажей из API"""

    ensure_api_dir()

    if count <= 0:
        return []

    items = []
    per_page = 50
    all_pages = (count + per_page - 1) // per_page
    print(f"\nЗагружаем {count} персонажей")

    # Загружаем данные по страницам с прогресс-баром
    for page in tqdm(range(1, all_pages + 1), desc="Загрузка"):
        items_remaining = count - len(items)
        current_per_page = min(per_page, items_remaining)

        if current_per_page <= 0:
            break

        try:
            # Делаем запрос к API с параметрами страницы
            response = requests.get(
                API_URL,
                params={"page": page, "pageSize": current_per_page},
                headers={"Content-Type": "application/json"},
                timeout=20,
            )

            if response.status_code == 200:
                data = response.json()
                characters = data.get("data", [])

                # Если персонажей нет, или если загрузили достаточно - выходим
                if not characters or len(items) >= count:
                    break
                # Добавляем персонажей в общий список
                items.extend(characters)

            else:
                print(f"\nОшибка API: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"\nОшибка соединения: {e}")
            break

        time.sleep(0.5)

    result = items[:count]
    print(f" Из базы загружено {len(result)} персонажей (запрошено {count})")
    return result
