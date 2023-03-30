import psycopg2
import sys
import os
import random
import dotenv


dotenv.load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST_EXTERNAL'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn



# create customers table and add customers to it
def create_task_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tasks")
    cur.execute("CREATE TABLE tasks (tasks_name varchar(255), deadline varchar(255), is_important varchar(255), is_urgent varchar(255))")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_task_table()