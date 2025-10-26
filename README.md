# Project in Data Engineering ITMO 2025
<div id="header" align="left">
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3IzMGtmNm9menh0OGJzb3hxY2trZG44YTJ5cWViN3FjaTE2aHlsaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/WoRCBZFcLqGt2iANB1/giphy.gif" width="100"/><img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3BkMzgzNzlyOGZlc256YXc4YXNidmhydGhydGpicHphNTd2dW5tciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dyzew7Py7bnW9DiJJj/giphy.gif" width="350"/>
</div>

## О проекте
  Проект реализован в рамках дисциплины по Инжинирингу данных на языке Python. Его целью является знакомство с основами инжиниринга, c разработкой программ по обработке больших баз данных и визуализации полученных результатов.

## Датасет
  Обрабатывается набор данных о нарушениях правил дорожного движения в разных штатах Индии за 2023 и 2024 год.
  
Ссылка на веб-источник: https://www.kaggle.com/datasets/khushikyad001/indian-traffic-violation/data

Ссылка на сохранённый датасет: https://drive.google.com/file/d/1gJrXyvqIVSZCEjqhGhvisyMyxI0zBald/view?usp=drive_link


# Руководство по чтению датасета

## Требования
  - Conda >= 25.7.0
  - Python >= 3.12.3
  - Poetry >= 2.2.0
  - pip

## Установка Conda+Poetry, создание переменного окружения
  > [!IMPORTANT]
  > Для работы со скриптом, необходимо скачать и поместить в пустую папку 3 файла: environment.yml, pyproject.toml и poetry.lock, установить miniconda (убедитесь, что есть в PATH) и poetry. Выполнить шаги 2 и 7

1. Создать переменное окружение
```
cоnda env create -f environment.yml
```
2. Активировать переменное окружение
```
cоnda activate <название окружения из environment.yml>
```
3. Инициализировать Poetry
```
poetry init
```
4. Определить Poetry в виртуальное окружение Сonda
```
poetry config virtualenvs.create false
```
5. Добавить зависимости в проект
```
poetry add jupyterlab pandas matplotlib wget
```
6. Установить Poetry
```
poetry install
```
> [!TIP]
> При работе в VSCode необходимо выбрать переменное окружение через "Python: Select Interpreter"

7. Активировать скрипт
```
python3 data_loader.py
```
  Результат работы скрипта:
![Скриншот с результатом команды raw_data.head(10)](images/image_data_10rows.png)

# Приведение типов данных и сохранение датасета в формате .parquet.

> [!TIP]
> Для удобства предварительного анализа данных из датасета и совершенствования кода были созданы файл-ноутбук .ipynb и data_loader_test.py в папке "tests". Для работы с ноутбуком необходимо установить kernel

При работе с базой данных важно, чтобы данные не попадали в репозиторий на github. Решение этой задачи было реализовано в tests/data_loader_test.py и перенесено в основной файл с кодом data_loader.py.

## Анализ типов данных
Исследование данных проводилось с целью выявления ошибочных данных, пустых значений (NaN) и типов данных в файле data_loader_test.py, решение перенесено в основной файл data_processing.py.
Была создана копия (маска), в которой на основании анализа проведены замена данных и изменение типов.
У выбранного датасета 33 признака. Данные до обработки выводятся таблицей при помощи команды:
```
print(raw_data.info())
```
![Скриншот с результатом команды raw_data.info()](images/data_before.jpg)

## Приведение типов данных и исправление значений
Были проведены следующие действия:
1. Определение количества пустых значений, уникальных значений и их перечисление
2. Исправление ошибок, например, изменение категории NaN на "not_required" для сохранения логики
3. Объединение признаков для оптимизации памяти (например, признак DateTime) и удаление исходных
4. Замена типа данных с помощью команды:
```
<переменная>["<название признака>"].astype("<новый тип данных>")
```
Таким образом, в процессе обработки было уменьшено использование памяти:
![Скриншот с результатом команды proc_data.info()](images/data_after.jpg)

## Сохранение датасета в формате .parquet

> [!TIP]
> Для работы с Parquet необходимо установить библиотеку pyarrow

В файле-исполнителе программы - main_project.py - вызываются функции по загрузке и обработке данных, предварительно указываются пути и происходит проверка наличия файлов .parquet и .csv.
Сохранение обработанных данных производится командой:
```
proc_data.to_parquet(parquet_path, index=False)
```
Этот файл будет использоваться при дальнейшей работе и анализе.

---
## Работа с публичным API
Данный подпроект подробно описан во вложенном [README.md](./api_example/README.md) в папке api_example.

---
## EDA
Разведочный анализ данных и выводы по нему представлены в папке notebooks в файле [EDA.ipynb](./notebooks/EDA.ipynb).

---
## SQL

> [!TIP]
> В poetry необходимо установить библиотеки sqlalchemy, asyncpg, python-dotenv, psycopg2

На данном этапе работы было произведено подключение к базе данных access (SQLite), с использованием файла .db, считывание из неё учетных данных, подключение к базе данных homeworks (PostgreSQL), и запись в неё первых 100 строк из файла .parquet.
Код по подключению и записи строк представлен в файле [write_to_db.py](./write_to_db.py).


---
## Визуализация

> [!TIP]
> В poetry необходимо установить библиотеку plotly

Данный этап работы связан с грамотной визуализацией разведочного анализа данных в файле в папке notebooks [EDA.ipynb](./notebooks/EDA.ipynb).
В качестве палитры была выбрана палитра "PuBuGn", и для каждого вида графиков были прописаны параметры отображения.

Основными критериями работы являлись:
- Удержание единого кастомного стиля
- Добавление динамических графиков
- Включение сетки графиков (несколько графиков в одном)


  > [!IMPORTANT]
  > Github не отображает графики plotly из-за наличия элементов JavaScript. Один из работающих способов просмотра этих графиков - сохранение каждого графика plotly в файл .html с последующим открытием этих файлов

  Ссылки на интерактивные графики:
  - [age_geography.html](./notebooks/age_geography.html)
  - [temporal_patterns.html](./notebooks/temporal_patterns.html)
  - [violation_types.html](./notebooks/violation_types.html)
