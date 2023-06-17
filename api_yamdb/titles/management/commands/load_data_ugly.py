import csv
import os

from django.apps import apps
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import .csv files into database from ./static/data folder.'

    def handle(self, *args, **options):
        APP_NAMES = (
            ('users', ('users', )),
            ('titles', ('genre', 'category', 'titles', 'genre_title', 'review', 'comments', )),
        )
        CSV_FOLDER = './static/data/'

        if not os.path.exists(CSV_FOLDER):
            raise CommandError(f'{CSV_FOLDER} does not exist.')

        files_to_upload = os.listdir(CSV_FOLDER)

        for app, file_names in APP_NAMES:
            print(app)
            for file in file_names:
                print(file)
                if (file + '.csv') in files_to_upload:
                    csv_path = os.path.join(CSV_FOLDER, (file + '.csv'))

                    model = os.path.splitext(file)[0].rstrip('s')

                    if app == 'users':
                        model = 'CustomUser'

                    if model == 'genre_title':
                        model = 'title_genre'
                    
                    print(app, model)

                    Model = apps.get_model(app, model)

                    model_fields = [field.name for field in Model._meta.fields]
                    

                    with open(csv_path, newline='') as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        field_names = next(reader)

                        for field_name in field_names:
                            field_name.removesuffix('_id')
                            """
                            if field_name not in model_fields:
                                raise CommandError(
                                    f"{field_name} field does not exists in {model}"
                                )
                            """

                        for row in reader:
                            try:
                                obj = Model()
                                for field, value in enumerate(row):
                                    set_field = field_names[field].removesuffix('_id')
                                    if Model._meta.get_field(field_names[field]).is_relation:
                                        set_field = set_field + '_id'
                                    setattr(obj, set_field, value)
                                obj.save()
                            except Exception as error:
                                raise CommandError(
                                    f'({error}, {obj}, {set_field}, {value})'
                                )
