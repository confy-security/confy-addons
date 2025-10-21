"""Module defines all the functions used by client applications
of the Confy encrypted communication system,
for generating cryptographic keys, encrypting and decrypting texts.

It uses RSA for asymmetric encryption and AES for symmetric encryption.

This file is licensed under the GNU GPL-3.0 license.
See the LICENSE file at the root of this repository for full details.
"""

import base64
import os
from typing import Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class RSAEncryption:
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

    def __init__(self, key_size: int = 4096, public_exponent: int = 65537):
        """Initialize RSAEncryption with a new key pair.

        Generates a new RSA key pair with the specified key size and public
        exponent. The private key is stored internally for decryption operations.

        Args:
            key_size: The size of the RSA key in bits. Defaults to 4096.
            public_exponent: The public exponent value. Defaults to 65537.

        """
        self._key_size = key_size
        self._public_exponent = public_exponent

        self._private_key = rsa.generate_private_key(
            public_exponent=self._public_exponent, key_size=self._key_size
        )

    def __repr__(self):
        """Return a string representation of the RSAEncryption instance.

        Returns:
            str: A detailed string representation including module, class name,
                parameters, and memory address.

        """
        class_name = type(self).__name__
        return f"""{self.__module__}.{class_name}(key_size={self._key_size!r},
                public_exponent={self._public_exponent!r}) object at {hex(id(self))}"""

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypts data using the private key.

        Decrypts the provided encrypted data using RSA with OAEP padding
        and SHA256 hashing algorithm.

        Args:
            encrypted_data: The encrypted bytes to decrypt.

        Returns:
            bytes: The decrypted data.

        """
        return self._private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

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
        return self.public_key.public_bytes(
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
        return base64.b64encode(self.serialized_public_key).decode()


class RSAPublicEncryption:
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

        """
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

        """
        return self._key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    @property
    def key(self) -> RSAPublicKey:
        """Returns the RSA public key.

        Returns:
            RSAPublicKey: The public key object used for encryption.

        """
        return self._key


class AESEncryption:
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


def deserialize_public_key(b64_key: str) -> PublicKeyTypes:
    """Deserializes a base64-encoded PEM string back to an RSA public key object.

    Decodes a base64-encoded PEM string and loads it as an RSA public key object
    that can be used for encryption operations.

    Args:
        b64_key (str): The base64-encoded PEM representation of the public key.

    Returns:
        PublicKeyTypes: The deserialized RSA public key object.

    """
    key_bytes = base64.b64decode(b64_key.encode())
    return serialization.load_pem_public_key(key_bytes)
