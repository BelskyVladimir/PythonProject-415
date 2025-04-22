import os
import pandas as pd
from glob import glob
import configparser
from database_connection import DatabaseConnection

try:
    # Создание переменной (необходимо для исключения ошибок в блоке finally).
    dt = False
    # Загрузка параметров, необходимых для подключения к базе данных, из файла config.ini.
    path = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config.read(path + '/config.ini')
    # Данные для подключения к базе данных.
    DATABASE = config['Database']['DATABASE']
    USER = config['Database']['USER']
    PASSWORD = config['Database']['PASSWORD']
    HOST = config['Database']['HOST']
    PORT = config['Database']['PORT']

    # Создание подключения к базе данных.
    dt = DatabaseConnection(HOST, PORT, DATABASE, USER, PASSWORD)

    # Создание таблицы в базе для загрузки данных, если ее нет.
    query_create = '''
        create table if not exists sales (
            id serial primary key,
            doc_id varchar(30),
            item varchar,
            category varchar(50),
            amount int,
            price numeric,
            discount numeric
        )
    '''
    dt.create(query_create)

    # Составление списка файлов, выгруженных в папку data.
    path += '/data/'
    if os.path.exists(path):
        filelist = glob(f'{path}*_*.csv')
    else:
        raise FileNotFoundError ('No Such File Or Directory.')

    # Чтение файлов из списка и построчная загрузка их содержимого в базу данных.
    for f in filelist:
        print(f)
        df = pd.read_csv(f)
        for index, row in df.iterrows():
            query_insert = '''
                    insert into sales (doc_id, item, category, amount, price, discount)
                    values(%s, %s, %s, %s, %s, %s)
            '''
            dt.post(query_insert, list(dict(row).values())[1:])

except Exception as err:
    print('except Exception as err')
    print(err)

finally:
    # Отключение базы данных.
    if isinstance(dt, DatabaseConnection):
        dt.exit()