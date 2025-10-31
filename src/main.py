from .extract import download_csv_from_GD, load_data
from .transform import conv_data
from .load import data_to_parquet, read_data_from_parquet, write_to_db
from .validate import (
    check_file_parquet_exists,
    check_file_csv_exists,
    val_csv,
    val_parquet,
)
from dotenv import load_dotenv
import os
import click

load_dotenv()

file_id = os.getenv("FILE_ID")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_url = os.getenv("DB_URL")
db_port = os.getenv("DB_PORT")
db_root_base = os.getenv("DB_ROOT_BASE")
db_table_name = os.getenv("DB_TABLE_NAME")

assert file_id, "FILE_ID не установлен в .env"
assert db_user, "DB_USER не установлен в .env"
assert db_password, "DB_PASSWORD не установлен в .env"
assert db_url, "DB_URL не установлен в .env"
assert db_port, "DB_PORT не установлен в .env"
assert db_root_base, "DB_ROOT_BASE не установлен в .env"
assert db_table_name, "DB_TABLE_NAME не установлен в .env"


@click.command()
@click.option("--csv-name", default="dataset", help="Название файла .csv")
@click.option("--parquet-name", default="dataset", help="Название файла .parquet")
@click.option("--no-write-db", is_flag=True, help="Не записывать в базу данных")
def etl_pipeline(csv_name, parquet_name, no_write_db):

    click.echo("\n- Начало ETL -\n")
    click.echo(f"CSV файл: {csv_name}.csv\n")
    click.echo(f"Parquet файл: {parquet_name}.parquet\n")
    click.echo(f"Запись в БД: {'НЕТ' if no_write_db else 'ДА'}\n")
    if not no_write_db:  # Если флаг --no-write-db НЕ установлен
        click.echo("Количество строк записи в БД: 100\n")

    project_root = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")

    for directory in [raw_dir, processed_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            click.echo(f"Создана директория: {directory}")

    csv_filename = f"{csv_name}.csv"
    parquet_filename = f"{parquet_name}.parquet"

    data = None

    if check_file_parquet_exists(processed_dir, parquet_filename):
        click.echo("Файл .parquet найден")
        try:
            parquet_path = os.path.join(processed_dir, parquet_filename)
            data = read_data_from_parquet(parquet_path)
            click.echo(f"Загружено {len(data)} строк из parquet")
        except Exception as e:
            click.echo(f"Ошибка загрузки parquet: {e}")
            data = None
    else:
        click.echo("Файл .parquet не найден")
        click.echo("\n- Проверяем наличие файла .csv -\n")

        csv_file_path = check_file_csv_exists(raw_dir, csv_filename)

        if not csv_file_path:
            click.echo("Файл .csv не найден. Скачиваем")
            try:
                csv_file_path = download_csv_from_GD(file_id, csv_filename)
                click.echo(f"Файл загружен: {csv_file_path}")
            except Exception as e:
                click.echo(f"Ошибка загрузки .csv: {e}")
                return
        else:
            click.echo(f"Файл .csv найден: {csv_file_path}")

        try:
            click.echo("Загружаем данные из .csv...")
            raw_data = load_data(csv_file_path, sep=";")
            click.echo(f"Загружено {len(raw_data)} строк из .csv")

            click.echo("\n---Валидация исходных данных---\n")
            csv_valid = val_csv(raw_data)
            if not csv_valid:
                click.echo("Ошибка: Валидация исходных данных не пройдена")
                return

            click.echo("\nПреобразование данных...")
            clean_data = conv_data(raw_data)

            click.echo("Сохранение в parquet...")
            parquet_path = data_to_parquet(clean_data, processed_dir, parquet_filename)
            click.echo(f"Данные сохранены: {parquet_path}")

            data = clean_data

        except Exception as e:
            click.echo(f"Ошибка обработки данных: {e}")
            return

    if data is not None:
        click.echo("\n---Валидация выходных данных---\n")
        valid = val_parquet(data)

        if not valid:
            click.echo("Ошибка: Валидация обработанных данных не пройдена")
            return

        if not no_write_db:
            click.echo("\nЗапись в базу данных")
            success = write_to_db(
                data,
                db_user,
                db_url,
                db_password,
                db_port,
                db_root_base,
                db_table_name,
                size=100,  # Используем размер по умолчанию из load.py
            )
            if success:
                click.echo("Данные успешно записаны в БД")
            else:
                click.echo("Возникли проблемы при записи в БД")
        else:
            click.echo("\nЗапись в БД не проводилась")

        # Итог
        click.echo("\nETL завершен\n")

    else:
        click.echo("Ошибка: Данные не были загружены или преобразованы")


if __name__ == "__main__":
    etl_pipeline()
