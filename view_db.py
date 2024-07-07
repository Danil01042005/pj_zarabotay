import pandas as pd
import psycopg2

# Подключаемся к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname='postgres',  # Замените на имя вашей базы данных
    user='postgres',  # Замените на ваше имя пользователя
    password='postgres',  # Замените на ваш пароль
    host='localhost',  # Замените на хост вашей базы данных
    port='5432'  # Замените на порт вашей базы данных, если он отличается
)

# Читаем данные из таблицы в DataFrame
df = pd.read_sql_query('SELECT * FROM vacancies', conn)

# Печатаем DataFrame
print(df)

# Закрываем соединение
conn.close()
