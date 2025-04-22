import pandas as pd
import os, json
from glob import glob
import random as r
from datetime import datetime

# Настройка генератора случайных чисел.
r.seed(42)
# Определение текущей даты.
current_date = datetime.now().strftime('%Y-%m-%d')
# Определение пути до текущей папки.
path = os.path.dirname(__file__)

# Проверка наличия и очистки или создание директории data для выгрузки файлов.
if not os.path.exists(path + '/data/'):
    os.mkdir(path + '/data')
else:
    filelist = glob(f'{path}/data/*_*.csv')
    for f in filelist:
        os.remove(f)

# Задание количества магазинов и касс.
# Количество магазинов
NM = 10
# Максимальное количество касс.
NK = 7
# Генерация списка названия файлов, состоящих из номера магазина и номера кассы.
filenames = [f'{m}_{k}.csv' for m in range(1, NM+1) for k in range(1, r.randint(1, NK)+1)]

# Загрузка номенклатуры из файла.
with open(path + '/nomenclature.txt', 'r', encoding='UTF-8') as f:
    json_str = f.read()
    products = json.loads(json_str)

# Формирование данных о продажах по магазинам и кассам и выгрузка их в файлы.
for filename in filenames:
    # Создание префикса номера чека.
    doc = f'CH-{filename[:-4]}-{current_date}-'
    # Создание пустых списков.
    doc_id, item, category, amount, price, discount = [], [], [], [], [], []
    # Определение случайным образом количества записей в файле.
    number_of_records = r.randint(100, 150)
    # Задание начального номера чека.
    number_of_check = 1

    # Формирование списков со значениями признаков для каждой записи.
    for _ in range(number_of_records):
        # Определение значений категории, товара, цены, количества и скидки в текущей записи.
        category_rnd = list(products.keys())[r.randint(0, len(list(products.keys()))-1)]
        item_rnd = products[category_rnd][r.randint(0, len(products[category_rnd])-1)][0]
        price_rnd = products[category_rnd][r.randint(0, len(products[category_rnd])-1)][1]
        amount_rnd = r.randint(1, 5)
        discount_rnd = 0.05 if amount_rnd >= 5 else 0.03 if amount_rnd >= 3 else 0

        # Добавление значений в списки.
        doc_id.append(doc + '0' * (6 - len(str(number_of_check))) + str(number_of_check))
        category.append(category_rnd)
        item.append(item_rnd)
        price.append(price_rnd)
        amount.append(amount_rnd)
        discount.append(discount_rnd)
        # Случайный выбор оставить текущий номер чека или перейти к следующему.
        number_of_check += r.randint(0, 1)

    # Создание датафрейма из списков.
    df = pd.DataFrame({
        'doc_id':doc_id,
        'item':item,
        'category':category,
        'amount':amount,
        'price':price,
        'discount':discount
         })

    # Сохранение датафрейма в файл.
    df.to_csv(path + '/data/' + filename)




