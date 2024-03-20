
import csv
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")
django.setup()

# эти импорты должны идти после конфигурирования Django, иначе не заработает
from custom_auth.models import CustomUser  # noqa
from reviews.models import (Category, Comment, Genre, GenreTitle,  # noqa
                           Review, Title)

BASE_PATH = './static/data/'


MAPPING = [
    {
        'table_csv': 'users',
        'model': CustomUser,
    },
    {
        'table_csv': 'category',
        'model': Category,
    },
    {
        'table_csv': 'genre',
        'model': Genre,
    },
    {
        'table_csv': 'titles',
        'model': Title,
    },
    {
        'table_csv': 'genre_title',
        'model': GenreTitle,
    },
    {
        'table_csv': 'review',
        'model': Review,
    },
    {
        'table_csv': 'comments',
        'model': Comment,
    },
]


def import_csvs():
    for item in MAPPING:
        model = item['model']
        table = item['table_csv']

        print(f'Importing: {table}')

        with open(BASE_PATH + f'{table}.csv', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                result_row = {}
                for field_name in row.keys():
                    result_row[field_name] = row[field_name]

                instance = model(**result_row)
                instance.save()


import_csvs()
