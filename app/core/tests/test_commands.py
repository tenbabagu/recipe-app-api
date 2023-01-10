"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('django.db.connection.ensure_connection')
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_ensure_connection):
        """Test waiting for database if database ready"""
        patched_ensure_connection.return_value = True

        call_command('wait_for_db')

        patched_ensure_connection.assert_called_once()

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_ensure_connection):
        """Test waiting for database when getting OperationalError"""
        patched_ensure_connection.side_effect = [
            Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_ensure_connection.call_count, 6)
        patched_ensure_connection.assert_called()
