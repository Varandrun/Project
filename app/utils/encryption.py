import os
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, key: str | None = None):
        if key is None:
            key = os.getenv("ENCRYPTION_KEY")
        if key is None:
            key = Fernet.generate_key().decode()
        if isinstance(key, str):
            key = key.encode()
        self._fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        if data is None:
            return None
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        if token is None:
            return None
        return self._fernet.decrypt(token.encode()).decode()
