from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Check DB."

    def handle(self, *args, **options):
        db_conn = connections['default']
        try:
            print(f'connections: {db_conn.settings_dict}')
            c = db_conn.cursor()
        except OperationalError:
            print('NOT CONNECTED')
        else:
            print('CONNECTED OK!')
        print("Done")
