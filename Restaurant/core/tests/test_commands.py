# Prueba para garantizar que la BD este disponible

from unittest.mock import patch #biblioteca de objetos simulados

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Prueba para la dispononibilidad de la base de datos"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True  #comport que realize Django lo anulara y remplaza por obj simulad

            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting from db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
