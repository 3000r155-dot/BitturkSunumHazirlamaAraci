import hashlib
import hmac


_SALT = bytes.fromhex("4f5b00047efef9297afaf5fa1bec2875")
_PASSWORD_HASH = bytes.fromhex("6f990c37112eca408032c5c40da59b72de43a6dafad8cbb4ea53e2dcb18e6e04")
_ITERATIONS = 600_000


def verify_password(password):
    if not isinstance(password, str):
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        _SALT,
        _ITERATIONS,
    )
    return hmac.compare_digest(candidate, _PASSWORD_HASH)
