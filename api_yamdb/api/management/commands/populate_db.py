import csv

# from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

BASE_PATH = './static/data/'

MAPPING = [
    {
        'table_csv': 'users',
        'model': User,
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
        # отказались от явного описания M2M модели и её привязки через
        # through, поэтому, надо тепрь получать авто-генерирумую связей
        # модель вот так
        'model': Title.genre.through,
        # альтернатива:
        # django_apps.get_model('reviews.title_genre',
        #                        require_ready=True),
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


class Command(BaseCommand):
    help = "Импортирует тестовые данные из CSV"

    def handle(self, *args, **options):
        for item in MAPPING:
            model = item['model']
            table = item['table_csv']

            self.stdout.write(
                self.style.SQL_TABLE(f'Importing: {table}')
            )

            with open(BASE_PATH + f'{table}.csv', encoding='utf8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    result_row = {}
                    for field_name in row.keys():
                        result_row[field_name] = row[field_name]

                    instance = model(**result_row)
                    instance.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Все таблицы, {len(MAPPING)}шт. залиты в базу'))
