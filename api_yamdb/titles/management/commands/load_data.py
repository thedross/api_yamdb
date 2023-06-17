import csv
import os
from typing import Any, Optional

from django.apps import apps
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import .csv files into database from ./static/data folder.'

    def handle(self, *args, **options):
        APP_NAMES = (
            ('users', ('users, ')),
            ('titles', ('genre', 'category', 'titles', 'review', 'comments', 'genre_title')),
        )


    