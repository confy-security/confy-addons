"""Abstract base class for encryption handlers.

This module defines an abstract base class that specifies the interface
for encryption handlers. Any concrete encryption handler must implement
the methods defined in this abstract base class.
"""

from abc import ABC, abstractmethod


class AESEncryptionABC(ABC):
    """Abstract base class for encryption handlers.

    This class defines the interface for encryption handlers, requiring
    implementation of encryption and decryption methods.
    """

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """Encrypts the given plaintext string.

        Args:
            plaintext (str): The text to be encrypted.

        Returns:
            str: The encrypted text as a string.

        """
        pass  # pragma: no cover

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """Decrypts the given ciphertext string.

        Args:
            ciphertext (str): The text to be decrypted.

        Returns:
            str: The decrypted text as a string.

        """
        pass  # pragma: no cover
