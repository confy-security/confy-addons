"""AES encryption implementation using the cryptography library.

This module provides an AES encryption handler that implements the
AESEncryptionABC abstract base class. It supports AES encryption and
decryption in CFB mode with 256-bit keys.
"""

import base64
import binascii
import logging
import secrets
from typing import Optional

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from confy_addons.core.abstract import AESEncryptionABC
from confy_addons.core.constants import AES_IV_SIZE, AES_KEY_SIZE, LOGGER_LEVEL
from confy_addons.core.exceptions import DecryptionError, EncryptionError
from confy_addons.core.mixins import EncryptionMixin

logging.basicConfig(level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)


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
            TypeError: If the provided key is not bytes or bytearray.

        """
        self._key_size = AES_KEY_SIZE

        if key is None:
            self._key = secrets.token_bytes(self._key_size)
        else:
            if not isinstance(key, (bytes, bytearray)):
                logger.error(f'Invalid key type: {type(key)}')
                raise TypeError('AES key must be bytes or bytearray')

            key_bytes = bytes(key)

            if len(key_bytes) != self._key_size:
                logger.error(f'Invalid key length: {len(key_bytes)}')
                raise ValueError(
                    f'AES key must be {self._key_size} bytes long ({self._key_size * 8} bits)'
                )
            self._key = key_bytes
            logger.debug('AES encryption initialized with provided key')

    def __repr__(self):
        """Return a string representation of the AESEncryption instance.

        Returns:
            str: A detailed string representation including module, class name,
                key, and memory address.

        """
        class_name = type(self).__name__
        return f"""{self.__module__}.{class_name}(key=<hidden>) object at {hex(id(self))}"""

    def encrypt(self, plaintext: str) -> str:
        """Encrypts text using AES in CFB mode.

        Encrypts the provided plaintext using AES-256 in CFB mode with a
        randomly generated initialization vector. Returns the result as a
        base64-encoded string.

        Args:
            plaintext: The text string to encrypt.

        Returns:
            str: The base64-encoded encrypted data (IV + ciphertext).

        Raises:
            EncryptionError: If an error occurs during encryption.
            TypeError: If the plaintext is not a string.

        """
        if not isinstance(plaintext, str):
            logger.error(f'Invalid plaintext type: {type(plaintext)}')
            raise TypeError('plaintext must be a str')

        try:
            iv = secrets.token_bytes(AES_IV_SIZE)
            cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv))
            encryptor = cipher.encryptor()
            ciphertext = (
                encryptor.update(plaintext.encode(encoding='utf-8')) + encryptor.finalize()
            )
            return base64.b64encode(iv + ciphertext).decode(encoding='ascii')
        except Exception as e:
            logger.error(f'Error occurred during encryption: {e}')
            raise EncryptionError('Error occurred during encryption') from e

    def decrypt(self, b64_ciphertext: str) -> str:
        """Decrypts base64-encoded AES encrypted data.

        Decrypts the provided base64-encoded encrypted data using AES-256
        in CFB mode. The encrypted data must be in the format produced by
        the encrypt method (IV + ciphertext).

        Args:
            b64_ciphertext: The base64-encoded encrypted data.

        Returns:
            str: The decrypted plaintext as a string.

        Raises:
            TypeError: If the b64_ciphertext is not a string.
            ValueError: If the base64 data is invalid or too short.
            DecryptionError: If an error occurs during decryption.

        """
        if not isinstance(b64_ciphertext, str):
            logger.error(f'Invalid b64_ciphertext type: {type(b64_ciphertext)}')
            raise TypeError('b64_ciphertext must be a base64-encoded str')

        try:
            data = base64.b64decode(b64_ciphertext)
        except (binascii.Error, ValueError, TypeError) as e:
            logger.error(f'Error occurred during base64 decoding: {e}')
            raise ValueError('Invalid base64 encrypted data') from e

        if len(data) < AES_IV_SIZE:
            logger.error(f'Invalid encrypted data length: {len(data)}')
            raise ValueError('Encrypted data is too short to contain an IV and ciphertext')

        iv, ciphertext = data[:AES_IV_SIZE], data[AES_IV_SIZE:]

        try:
            cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv))
            decryptor = cipher.decryptor()
            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext_bytes.decode('utf-8')
        except Exception as e:
            logger.error(f'Error occurred during decryption: {e}')
            raise DecryptionError('Decryption failed') from e

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
