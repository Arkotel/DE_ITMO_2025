from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_url = os.getenv("DB_URL")
db_port = os.getenv("DB_PORT")
db_root_base = os.getenv("DB_ROOT_BASE")

assert db_url

data = pd.read_parquet(r"notebooks/data/dataset.parquet")

new_column_names = {col: col.lower() for col in data.columns}
data.rename(columns=new_column_names, inplace=True)
# print(data.info())

part_of_data = data.head(100)
print(part_of_data.shape)

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_root_base}",  # noqa
    pool_recycle=3600,
    # echo=True,
)

with engine.begin() as conn:
    part_of_data.to_sql(
        name="kosagova",
        con=conn,
        schema="public",
        if_exists="replace",
        index=False,
    )

inspector = inspect(engine)
tables = inspector.get_table_names(schema="public")
if "kosagova" in tables:
    print("Таблица найдена")
else:
    print("Таблица не найдена")


with engine.begin() as conn:
    query = """
    SELECT k.violation_id, k.driver_gender, k.previous_violations
    FROM public.kosagova AS k
    LIMIT 100
    """
    rows = conn.execute(text(query)).all()

print(rows)
