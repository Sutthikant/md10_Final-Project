import discord
from dotenv import load_dotenv
import os
import openai
import logging
from logging.handlers import RotatingFileHandler
import psycopg2

# create logger
def init_logging(logger):
    # logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    handler_rot_file = RotatingFileHandler(filename='discord-bot.log', encoding='utf-8', mode='a')
    handler_rot_file.setLevel(logging.DEBUG)
    handler_rot_file.setFormatter(log_formatter)

    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.DEBUG)
    handler_console.setFormatter(log_formatter)

    logger.addHandler(handler_rot_file)
    logger.addHandler(handler_console)

    return logger


logger = init_logging(logging.root)

def classify_intent(prompt):
    model_engine = "text-davinci-002"  # or any other OpenAI model that suits your use case

    # define the prompt to use for classification
    prompt = (f"Please classify the following user input into one of the following categories: "
              f"1. cheap\n2. expensive\n\n"
              f"User Input: {prompt}\nCategory:")

    # send prompt to OpenAI's API for classification
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # retrieve the predicted intent code from the response
    predicted_intent = response.choices[0].text.strip().lower()

    # return the predicted intent code
    return predicted_intent

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST_EXTERNAL'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

def add_tasks(taskname, deadline, is_important, is_urgent):

    logging.info(f"taskname: {taskname}, deadline: {deadline}, is_important: {is_important}, is_Urgent: {is_urgent}")

    conn = get_db_connection()
    cur = conn.cursor()
    logging.info('Connected.')
    logging.info('Reading data...')
    cur.execute("INSERT INTO tasks VALUES (%s, %s, %s, %s)", (taskname, deadline, is_important, is_urgent))
    conn.commit()
    cur.close()

def delete_tasks(taskname):

    logging.info(f"taskname: {taskname}")

    conn = get_db_connection()
    cur = conn.cursor()
    logging.info('Connected.')
    logging.info('Reading data...')
    cur.execute("DELETE FROM tasks WHERE tasks_name = %s", (taskname,))
    conn.commit()
    cur.close()

def list_all_tasks(all_tasks):

    logging.info(f"list all task")

    conn = get_db_connection()
    cur = conn.cursor()
    logging.info('Connected.')
    logging.info('Reading data...')
    cur.execute("SELECT * FROM tasks")
    all_task = cur.fetchall()
    logging.info(f"{all_task}")
    for task in all_task:
        all_tasks.append(task)
    conn.commit()
    cur.close()
    logging.info('Finished.')

class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            result = message.content.split(" ")
            logging.info(message.content)
            logging.info(result)

            if result[1] == 'add' :
                taskname = result[2] 
                deadline = result[3]
                is_important = result[4]
                is_urgent = result[5]
                add_tasks(taskname, deadline, is_important, is_urgent)
                await message.channel.send('Add task successfully!!!')
            elif result[1] == 'delete' :
                taskname = result[2]
                delete_tasks(taskname)
                await message.channel.send('Delete task successfully!!!')
            elif result[1] == 'list' :
                all_tasks = []
                list_all_tasks(all_tasks)
                count = 0
                sentence = "list of all tasks\n\n"
                logging.info(all_tasks)
                for task in all_tasks:
                    print(1)
                    count += 1
                    line = f"{count}. task_name: {task[0]}, deadline: {task[1]}, {task[2]} {task[3]}\n\n"
                    sentence += line
                    logging.info(line)
                await message.channel.send(f'{sentence}')

            else:
                await message.channel.send('Sorry, I do not understand you')

load_dotenv()

openai.api_key = os.getenv('OPEN_API_KEY')
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_BOT_TOKEN'))


