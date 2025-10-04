"""Запрашиваем у пользователя количество персонажей для загрузки"""


def get_character_count() -> int:

    while True:
        try:
            count = int(input("Сколько персонажей Вы хотите загрузить?: "))

            if count <= 0:
                print("Ошибка. Число должно быть больше 0")
                return 0
            elif count > 10:
                print("Ошибка. Макс. число персонажей для загрузки - 10")
                return 0
            else:
                # Если число в допустимом диапазоне
                return count

        except ValueError:
            print("Ошибка. Введите целое число")
            return 0
