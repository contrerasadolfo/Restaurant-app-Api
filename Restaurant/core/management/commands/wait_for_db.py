import time

# Prueba de conexion de la base de datos
from django.db import connections
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is avalible"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Cargando base de datos...'))
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Base de Datos no disponible, esperando 1 sg...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Base de Datos Disponible!!!'))
