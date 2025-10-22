"""AES encryption implementation using the cryptography library.

This module provides an AES encryption handler that implements the
AESEncryptionABC abstract base class. It supports AES encryption and
decryption in CFB mode with 256-bit keys.
"""

import base64
import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from confy_addons.core.abstract import AESEncryptionABC
from confy_addons.core.mixins import EncryptionMixin


class AESEncryption(EncryptionMixin, AESEncryptionABC):
    """AES symmetric encryption handler.

    This class provides AES encryption and decryption operations in CFB mode
    with 256-bit keys. It can generate a random key or use a provided key.

    Attributes:
        key: The AES encryption key (32 bytes).
        key_size: The size of the AES key in bytes (always 32 for AES-256).

    """

    def __init__(self, key: Optional[bytes] = None):
        """Initialize AESEncryption with a key.

        Creates an AES encryption handler with either a provided key or a newly
        generated random key.

        Args:
            key: An optional 32-byte AES key. If None, a random key is generated.

        Raises:
            ValueError: If the provided key is not 32 bytes long.

        """
        self._key_size = 32  # 256 bits

        if key is None:
            self._key = os.urandom(self._key_size)
        else:
            if len(key) != self._key_size:
                raise ValueError(
                    f'AES key must be {self._key_size} bytes long ({self._key_size * 8} bits)'
                )
            self._key = key

    def __repr__(self):
        """Return a string representation of the AESEncryption instance.

        Returns:
            str: A detailed string representation including module, class name,
                key, and memory address.

        """
        class_name = type(self).__name__
        return f"""{self.__module__}.{class_name}(key={self._key!r}) object at {hex(id(self))}"""

    def encrypt(self, plaintext: str) -> str:
        """Encrypts text using AES in CFB mode.

        Encrypts the provided plaintext using AES-256 in CFB mode with a
        randomly generated initialization vector. Returns the result as a
        base64-encoded string.

        Args:
            plaintext: The text string to encrypt.

        Returns:
            str: The base64-encoded encrypted data (IV + ciphertext).

        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, b64_ciphertext: str) -> str:
        """Decrypts base64-encoded AES encrypted data.

        Decrypts the provided base64-encoded encrypted data using AES-256
        in CFB mode. The encrypted data must be in the format produced by
        the encrypt method (IV + ciphertext).

        Args:
            b64_ciphertext: The base64-encoded encrypted data.

        Returns:
            str: The decrypted plaintext as a string.

        """
        data = base64.b64decode(b64_ciphertext)
        iv, ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        return (decryptor.update(ciphertext) + decryptor.finalize()).decode()

    @property
    def key(self) -> bytes:
        """Returns the AES encryption key.

        Returns:
            bytes: The 32-byte AES key.

        """
        return self._key

    @property
    def key_size(self) -> int:
        """Returns the size of the AES key in bytes.

        Returns:
            int: The key size in bytes (always 32 for AES-256).

        """
        return self._key_size
