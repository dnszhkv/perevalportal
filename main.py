import psycopg2
from decouple import config

# Получаем данные для подключения к базе данных из переменных окружения
dbname = config('FSTR_DB_NAME')
user = config('FSTR_DB_USER')
password = config('FSTR_DB_PASS')
host = config('FSTR_DB_HOST')
port = config('FSTR_DB_PORT')

# Создание базы данных
try:
    # создаю подключение к базе данных
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=dbname,
    )

    conn.autocommit = True

    # удаляю таблицы, если они существуют
    with conn.cursor() as cursor:
        cursor.execute(
            'DROP TABLE IF EXISTS "public"."pereval_perevaladded", "public"."pereval_perevalimages",'
            '"public"."pereval_coords", "public"."pereval_users", "public"."pereval_perevalareas", '
            '"public"."pereval_spractivitiestypes", "public"."pereval_perevaladdedimages" CASCADE;')

    # создаю таблицы
    with conn.cursor() as cursor:
        # таблица users
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."pereval_users" (
                    "id" serial PRIMARY KEY,
                    "email" text UNIQUE NOT NULL,
                    "phone" text,
                    "fam" text,
                    "name" text,
                    "otc" text
                );
            """)

        # таблица coords
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."pereval_coords" (
                    "id" serial PRIMARY KEY,
                    "latitude" double precision,
                    "longitude" double precision,
                    "height" integer
                );
            """)

        # таблица pereval_images
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."pereval_perevalimages" (
                    "id" serial PRIMARY KEY,
                    "date_added" timestamp,
                    "img" bytea,
                    "title" text
                );
            """)

        # таблица pereval_added
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."pereval_perevaladded" (
                    "id" serial PRIMARY KEY,
                    "date_added" timestamp,
                    "beautyTitle" text,
                    "title" text,
                    "other_titles" text,
                    "connect" text,
                    "add_time" timestamp,
                    "raw_data" json,
                    "coord_id" integer REFERENCES "public"."pereval_coords"("id"),
                    "level_winter" text,
                    "level_summer" text,
                    "level_autumn" text,
                    "level_spring" text,
                    "user_id" integer REFERENCES "public"."pereval_users"("id")
                );
            """)

        # таблица связи pereval_images и pereval_added
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."pereval_perevaladdedimages" (
                    "pereval_added_id" integer REFERENCES "public"."pereval_perevaladded"("id"),
                    "image_id" integer REFERENCES "public"."pereval_perevalimages"("id"),
                    PRIMARY KEY ("pereval_added_id", "image_id")
                );
            """)

        # таблица pereval_areas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "public"."pereval_perevalareas" (
                "id" serial PRIMARY KEY,
                "id_parent" integer,
                "title" text
            );
        """)

        # таблица spr_activities_types
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "public"."pereval_spractivitiestypes" (
                "id" serial PRIMARY KEY,
                "title" text
            );
        """)

except Exception as ex:
    print('[INFO] Error while working with PostgresSQL', ex)
finally:
    if conn:
        conn.close()
        print('[INFO] PostgresSQL connection is closed')
