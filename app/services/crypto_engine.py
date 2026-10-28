import hashlib
import hmac


class CryptoEngine:
    """Utilities for validating flags without embedding answer strings."""

    @staticmethod
    def hash_flag(flag: str) -> str:
        """Return the SHA-256 digest of a normalized flag."""
        return hashlib.sha256(flag.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def verify_flag(submitted: str, expected_hash: str) -> bool:
        """Compare a submitted flag with its stored SHA-256 digest."""
        if not submitted or not expected_hash:
            return False
        actual_hash = CryptoEngine.hash_flag(submitted)
        return hmac.compare_digest(actual_hash, expected_hash.strip().lower())
