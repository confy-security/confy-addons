"""RSA encryption handler with automatic key pair generation.

This module provides classes for RSA encryption and decryption using
the `cryptography` library. It includes functionality for generating RSA
key pairs, serializing public keys, and performing encryption and decryption
operations using RSA with OAEP padding.
"""

import base64
import binascii

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes

from confy_addons.core.constants import DEFAULT_RSA_KEY_SIZE, RSA_PUBLIC_EXPONENT
from confy_addons.core.exceptions import DecryptionError, EncryptionError
from confy_addons.core.mixins import EncryptionMixin


class RSAEncryption(EncryptionMixin):
    """RSA encryption handler with automatic key pair generation.

    This class generates and manages an RSA key pair for asymmetric encryption
    and decryption operations. It provides convenient access to both private
    and public keys, as well as serialized forms of the public key.

    Attributes:
        key_size: The size of the RSA key in bits.
        public_key: The RSA public key.
        private_key: The RSA private key.
        serialized_public_key: The public key in PEM format.
        base64_public_key: The public key in base64-encoded PEM format.

    """

    def __init__(self, key_size: int = DEFAULT_RSA_KEY_SIZE):
        """Initialize RSAEncryption with a new key pair.

        Generates a new RSA key pair with the specified key size and public
        exponent. The private key is stored internally for decryption operations.

        Args:
            key_size: The size of the RSA key in bits. Defaults to 4096.

        Raises:
            TypeError: If key_size is not an integer.
            ValueError: If key_size is less than the recommended minimum for security.
            RuntimeError: If key pair generation fails.

        """
        if not isinstance(key_size, int):
            raise TypeError('key_size must be an integer')
        if key_size < DEFAULT_RSA_KEY_SIZE:
            raise ValueError(f'key_size must be at least {DEFAULT_RSA_KEY_SIZE} bits for security')

        self._key_size = key_size
        self._public_exponent = RSA_PUBLIC_EXPONENT

        try:
            self._private_key = rsa.generate_private_key(
                public_exponent=self._public_exponent, key_size=self._key_size
            )
        except Exception as e:
            raise RuntimeError('Failed to generate RSA key pair') from e

    def __repr__(self):
        """Return a string representation of the RSAEncryption instance.

        Returns:
            str: A detailed string representation including module, class name,
                parameters, and memory address.

        """
        class_name = type(self).__name__
        return f"""{self.__module__}.{class_name}(key_size={self._key_size!r})
                object at {hex(id(self))}"""

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypts data using the private key.

        Decrypts the provided encrypted data using RSA with OAEP padding
        and SHA256 hashing algorithm.

        Args:
            encrypted_data: The encrypted bytes to decrypt.

        Returns:
            bytes: The decrypted data.

        Raises:
            TypeError: If encrypted_data is not bytes.
            ValueError: If encrypted_data is empty.
            DecryptionError: If decryption fails.

        """
        if not isinstance(encrypted_data, bytes):
            raise TypeError('encrypted_data must be bytes')
        if len(encrypted_data) == 0:
            raise ValueError('encrypted_data is empty')

        try:
            decrypted_data = self._private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return decrypted_data
        except Exception as e:
            raise DecryptionError('RSA decryption failed') from e

    @property
    def key_size(self) -> int:
        """Returns the size of the RSA key in bits.

        Returns:
            int: The key size in bits.

        """
        return self._key_size

    @property
    def public_key(self) -> RSAPublicKey:
        """Returns the RSA public key.

        Returns:
            RSAPublicKey: The public key object that can be shared with others
                for encryption operations.

        """
        return self._private_key.public_key()

    @property
    def private_key(self) -> RSAPrivateKey:
        """Returns the RSA private key.

        Returns:
            RSAPrivateKey: The private key object that should be kept secure
                and used for decryption operations.

        """
        return self._private_key

    @property
    def serialized_public_key(self) -> bytes:
        """Returns the public key in PEM format.

        Serializes the public key to PEM format with SubjectPublicKeyInfo
        structure, suitable for transmission or storage.

        Returns:
            bytes: The public key in PEM-encoded bytes.

        """
        return self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    @property
    def base64_public_key(self) -> str:
        """Returns the public key in base64-encoded PEM format.

        Provides the public key as a base64-encoded string, which is convenient
        for transmission over text-based protocols.

        Returns:
            str: The base64-encoded PEM representation of the public key.

        """
        serialized_public_key = self._private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return base64.b64encode(serialized_public_key).decode()


class RSAPublicEncryption(EncryptionMixin):
    """RSA encryption handler using a public key only.

    This class provides encryption operations using an existing RSA public key.
    It is intended for encrypting data that will be decrypted by the holder
    of the corresponding private key.

    Attributes:
        key: The RSA public key used for encryption.

    """

    def __init__(self, key: RSAPublicKey):
        """Initialize RSAPublicEncryption with a public key.

        Args:
            key: An RSA public key object to use for encryption operations.

        Raises:
            TypeError: If the provided key is not an instance of RSAPublicKey.

        """
        if not isinstance(key, RSAPublicKey):
            raise TypeError('key must be an instance of RSAPublicKey')

        self._key = key

    def __repr__(self):
        """Return a string representation of the RSAPublicEncryption instance.

        Returns:
            str: A detailed string representation including module, class name,
                key, and memory address.

        """
        class_name = type(self).__name__
        return f'{self.__module__}.{class_name}(key={self._key!r}) object at {hex(id(self))}'

    def encrypt(self, data: bytes) -> bytes:
        """Encrypts data using the public key.

        Encrypts the provided data using RSA with OAEP padding and SHA256
        hashing algorithm for secure encryption.

        Args:
            data: The bytes to encrypt.

        Returns:
            bytes: The encrypted data.

        Raises:
            TypeError: If the provided data is not bytes.
            EncryptionError: If encryption fails.

        """
        if not isinstance(data, bytes):
            raise TypeError('data must be bytes')
        try:
            return self._key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except Exception as e:
            raise EncryptionError('RSA encryption failed') from e

    @property
    def key(self) -> RSAPublicKey:
        """Returns the RSA public key.

        Returns:
            RSAPublicKey: The public key object used for encryption.

        """
        return self._key


def deserialize_public_key(b64_key: str) -> PublicKeyTypes:
    """Deserializes a base64-encoded PEM string back to an RSA public key object.

    Decodes a base64-encoded PEM string and loads it as an RSA public key object
    that can be used for encryption operations.

    Args:
        b64_key (str): The base64-encoded PEM representation of the public key.

    Returns:
        PublicKeyTypes: The deserialized RSA public key object.

    Raises:
        TypeError: If b64_key is not a string.
        ValueError: If the base64 decoding fails or the key cannot be loaded.

    """
    if not isinstance(b64_key, str):
        raise TypeError('b64_key must be a base64-encoded string')
    try:
        key_bytes = base64.b64decode(b64_key.encode('ascii'), validate=True)
    except (binascii.Error, ValueError) as e:
        raise ValueError('Invalid base64 public key') from e

    try:
        return serialization.load_pem_public_key(key_bytes)
    except Exception as e:
        raise ValueError('Failed to load public key from PEM') from e
