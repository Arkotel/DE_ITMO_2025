import os

count_max_str = os.environ.get("COUNT_MAX")
count_max = int(count_max_str)

"""Запрашиваем у пользователя количество персонажей для загрузки"""


def get_character_count() -> int:

    while True:
        try:
            count = int(input("\nСколько персонажей Вы хотите загрузить?: "))

            if count <= 0:
                print("Ошибка. Число должно быть больше 0")
                return 0
            elif count > count_max:
                print(
                    "Ошибка. Макс. число персонажей для загрузки - "
                    + str(count_max_str)
                )
                return 0
            else:
                # Если число в допустимом диапазоне
                return count

        except ValueError:
            print("Ошибка. Введите целое число")
            return 0
