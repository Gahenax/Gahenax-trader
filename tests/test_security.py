import unittest
from unittest.mock import patch
from scripts.testnet_probe import request

class SecurityTests(unittest.TestCase):
    def test_write_endpoint_blocked(self):
        for endpoint in ['/api/v3/order','/api/v3/order/test','/api/v3/withdraw']:
            with self.assertRaises(ValueError):
                request(endpoint)
    def test_missing_credentials_fail_closed(self):
        with patch.dict('os.environ', {'TESTNET_API_KEY':'', 'TESTNET_API_SECRET':''}):
            with self.assertRaises(ValueError):
                request('/api/v3/account', signed=True)

if __name__ == '__main__':
    unittest.main()
