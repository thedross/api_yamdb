import csv
import os

from django.apps import apps
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    """
    """

    help = 'Import .csv files into database from ./static/data folder.'

    def handle(self, *args, **options):
        APP_NAMES = (
            ('users', ('users, ')),
            ('titles', ('genre', 'category', 'titles', 'review', 'comments')),
        )
        CSV_FOLDER = './static/data/'

        if not os.path.exists(CSV_FOLDER):
            raise CommandError(f'{CSV_FOLDER} does not exist.')

        files_to_upload = os.listdir(CSV_FOLDER)

        for app, file_names in APP_NAMES:
            for file in files_to_upload:
                if os.path.splitext(file)[0] in file_names:
                    csv_path = os.path.join(CSV_FOLDER, file)

                    model = os.path.splitext(file)[0].rstrip('s')

                    if app == 'users':
                        model = 'CustomUser'

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
                                    set_field = field_names[field]
                                    if Model._meta.get_field(field_names[field]).is_relation:
                                        set_field = field_names[field] + '_id'
                                    setattr(obj, set_field, value)
                                obj.save()
                            except Exception as error:
                                raise CommandError(error)
