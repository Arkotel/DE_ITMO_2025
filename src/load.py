import pandas as pd
import os
from sqlalchemy import create_engine, inspect, text
import psycopg2


def data_to_parquet(clean_data, processed, filename):
    """Сохранение обработанных данных в .parquet"""
    file_path = os.path.join(processed, filename)
    clean_data.to_parquet(file_path, index=False)
    return file_path


def read_data_from_parquet(file_path):
    """Чтение данных из .parquet"""
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    else:
        raise FileNotFoundError("Ошибка чтения файла .parquet")


def write_to_db(
    clean_data, user, url, password, port, root_base, table_name, size=100
):  # noqa
    """Запись в базу данных"""
    print("\n---Загрузка в базу данных---\n")

    data_to_db = clean_data.head(size)

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{url}:{port}/{root_base}",
        pool_recycle=3600,
    )

    try:
        with engine.begin() as conn:
            data_to_db.to_sql(
                name=table_name,
                con=conn,
                schema="public",
                if_exists="replace",
                index=False,
            )
        print(
            f"\n{len(data_to_db)} строк успешно записаны в таблицу {table_name}\n"
        )  # noqa
    except Exception as e:
        print(f"Ошибка - {e}")
        return False

    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    f"ALTER TABLE public.{table_name} ADD PRIMARY KEY (violation_id)"
                )  # noqa
            )
        print("Ключ добавлен")

    except Exception as e:
        print(f"Ошибка - {e}")

    try:

        inspector = inspect(engine)
        tables = inspector.get_table_names(schema="public")
        if table_name in tables:
            print("Таблица найдена")

        else:
            print("Таблица не найдена")
            return False

    except Exception as e:
        print(f"Ошибка - {e}")
        return False

    return True
