import logging
from logging.handlers import RotatingFileHandler
import os
import flask
import psycopg2
import matplotlib.pyplot as plt

from dotenv import load_dotenv

# create logger
def init_logging(logger):
    # logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    handler_rot_file = RotatingFileHandler(filename='web-app.log', encoding='utf-8', mode='a')
    handler_rot_file.setLevel(logging.DEBUG)
    handler_rot_file.setFormatter(log_formatter)

    logger.addHandler(handler_rot_file)

    # handler_console = logging.StreamHandler()
    # handler_console.setLevel(logging.DEBUG)
    # handler_console.setFormatter(log_formatter)

#    logger.addHandler(handler_console)

    return logger


# to run the app:
# python3 -m flask --app webapp run --debug -p 8888 -h 0.0.0.0

app = flask.Flask(__name__)

# main route
@app.route('/')
def index():
    return flask.render_template('main.html')

@app.route('/alltasks', methods=['GET'])
def alltasks():

    # connect to the PostgreSQL server
    logging.info('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST_EXTERNAL'),
                            database=os.getenv('POSTGRES_DB'),
                            user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'))

    logging.info('Connected.')

    # read products from database
    logging.info('Reading data...')
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    rows = cur.fetchall()

    # render products template
    html = flask.render_template('alltasks.html', tasks=rows)

    # close the communication with the PostgreSQL
    cur.close()
    conn.close()
    logging.info('Done.')

    return html

# @app.route('/customers', methods=['GET'])
# def customers():
#     return "Customers"

# def get_monthly_sales(conn):
#     sql = """
#     select 
# 	date_part('month',o.order_date) as month_num, 
# 	sum(oi.price) as total_cost, sum(oi.quantity) as total_qty
# from 
# 	orders o 
# 	inner join order_items oi on oi.order_id = o.order_id
# group by month_num
# order by month_num
#     """

#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()

#     monthly_sales = []
#     for row in rows:
#         monthly_sales.append({'month': row[0], 'total_cost': row[1], 'total_qty': row[2]})

#     cur.close()

#     return monthly_sales


# @app.route('/sales', methods=['GET'])
# def sales():

#     # connect to the PostgreSQL server
#     logging.info('Connecting to the PostgreSQL database...')
#     conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST_EXTERNAL'),
#                             database=os.getenv('POSTGRES_DB'),
#                             user=os.getenv('POSTGRES_USER'),
#                             password=os.getenv('POSTGRES_PASSWORD'))

#     logging.info('Connected.')

#     # read products from database
#     logging.info('Reading data...')
#     cur = conn.cursor()
#     cur.execute('select	o.order_date, c.customer_name, o.order_id from orders o	inner join customers c on c.customer_id = o.customer_id')
#     rows = cur.fetchall()

#     orders = []
#     for row in rows:
#         orders.append({'date': row[0], 'customer_name': row[1], 'order_id': row[2]})

#     cur.close()

#     for o in orders:
#         cur = conn.cursor()
#         cur.execute(f'select p.product_name, oi.price, oi.quantity from order_items oi inner join products p on p.product_id = oi.product_id where oi.order_id = {o["order_id"]}')
#         rows = cur.fetchall()
#         products = []
#         for row in rows:
#             products.append({'name': row[0], 'price': row[1], 'quantity': row[2]})

#         o['products'] = products
#         cur.close()

#     monthly_sales = get_monthly_sales(conn)

#     conn.close()

#     # plot monthly sales with matplotlib
#     fig, ax = plt.subplots()
#     ax.plot([x['month'] for x in monthly_sales], [x['total_cost'] for x in monthly_sales])
#     ax.set(xlabel='month', ylabel='Total Cost',
#         title='Monthly Sales')
#     ax.grid()

#     uniq = os.urandom(8).hex()
#     path = f"static/images/monthly-sales-{uniq}.png"
#     fig.savefig(path)

#     html = flask.render_template('sales.html', orders=orders, monthly_sales_image=path)
#     return html

if __name__ == '__main__':
    logger = init_logging(logging.root)
    logging.info('Program started')

    # read environment variables
    load_dotenv()

    app.run(debug=True, port=8888, host='0.0.0.0')