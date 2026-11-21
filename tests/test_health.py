import json
import unittest
from unittest.mock import Mock
from scripts.health_server import Handler

class HealthSourceTests(unittest.TestCase):
    def test_health_handler_is_read_only(self):
        # Check that only GET is explicitly implemented by the handler.
        self.assertTrue(callable(getattr(Handler, 'do_GET', None)))
        self.assertFalse(hasattr(Handler, 'do_POST'))

if __name__ == '__main__':
    unittest.main()
