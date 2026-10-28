import unittest

from app.services.crypto_engine import CryptoEngine


class TestCryptoEngine(unittest.TestCase):
    def test_hash_normalizes_outer_whitespace(self):
        expected_hash = CryptoEngine.hash_flag("OFFHA{sample_flag}")
        self.assertTrue(CryptoEngine.verify_flag("  OFFHA{sample_flag}  ", expected_hash))

    def test_rejects_wrong_flag(self):
        expected_hash = CryptoEngine.hash_flag("OFFHA{sample_flag}")
        self.assertFalse(CryptoEngine.verify_flag("OFFHA{wrong_flag}", expected_hash))

    def test_rejects_missing_values(self):
        self.assertFalse(CryptoEngine.verify_flag("", ""))
        self.assertFalse(CryptoEngine.verify_flag("OFFHA{sample_flag}", ""))


if __name__ == "__main__":
    unittest.main()
