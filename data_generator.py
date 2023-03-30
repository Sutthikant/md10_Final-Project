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

def generate_task():
    tasks = []
    names = ['do', 'finish', 'go', 'read']
    last_names = ['homework', 'assignment', 'shopping', 'book']

    # generate 100 customers with random names
    for i in range(100):
        name = names[i % 4] + ' ' + last_names[i % 4]
        tasks.append((i, name))

    return tasks


# create customers table and add customers to it
def create_task_table():
    tasks = generate_task()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tasks")
    cur.execute("CREATE TABLE tasks (tasks_id int, tasks_name varchar(255))")
    for task in tasks:
        cur.execute("INSERT INTO tasks VALUES (%s, %s)", task)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_task_table()