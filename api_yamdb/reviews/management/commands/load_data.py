import csv
import os

from django.apps import apps
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import .csv files into database from ./static/data folder.'

    CSV_FOLDER = './static/data/'

    APP_FILES_TABLES = (
        ('users', ('users', ), ('customuser', )),
        (
            'reviews',
            (
                'genre',
                'category',
                'titles',
                'genre_title',
                'review',
                'comments'
            ),
            (
                'genre',
                'category',
                'title',
                'title_genre',
                'review',
                'comment'
            )
        )
    )

    def check_dir(self):
        """Проверяет наличие директории с .csv файлами."""
        if not os.path.exists(self.CSV_FOLDER):
            raise CommandError(f'{self.CSV_FOLDER} does not exist.')

    def check_files(self):
        """
        Проверяет соответствие APP_FILES_TABLES и актуального набора файлов.
        """
        to_upload = [
            file.removesuffix('.csv')
            for file
            in os.listdir(self.CSV_FOLDER)
        ]

        for app, files, models in self.APP_FILES_TABLES:
            for file in files:
                if file not in to_upload:
                    raise CommandError(f'{file} does not exist.')

    def check_fields(self, Model, fields):
        """
        Проверяет соответствие полей моделей из файлов и полей моделей в БД.
        """
        model_fields = [field.name for field in Model._meta.fields]
        for field in fields:
            if field not in model_fields:
                raise CommandError(
                    f"{field} field does not exists in {Model}"
                )

    def handle(self, *args, **options):
        self.check_dir()
        self.check_files()
        for app, files, models in self.APP_FILES_TABLES:
            for i, file in enumerate(files):
                csv_path = os.path.join(self.CSV_FOLDER, (file + '.csv'))
                Model = apps.get_model(app, models[i])

                with open(csv_path, newline='') as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    fields = [
                        field.removesuffix('_id')
                        for field
                        in next(reader)
                    ]
                    self.check_fields(Model, fields)
                    for row in reader:
                        try:
                            obj = Model()
                            for field, value in enumerate(row):
                                set_field = fields[field]
                                if Model._meta.get_field(
                                    set_field
                                ).is_relation:
                                    set_field = set_field + '_id'
                                setattr(obj, set_field, value)
                            obj.save()
                        except Exception as error:
                            raise CommandError(
                                f'({error}: {obj}, {set_field}, {value})'
                            )
