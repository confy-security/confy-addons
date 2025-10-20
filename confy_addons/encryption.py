"""Module defines all the functions used by client applications
of the Confy encrypted communication system,
for generating cryptographic keys, encrypting and decrypting texts.

It uses RSA for asymmetric encryption and AES for symmetric encryption.

This file is licensed under the GNU GPL-3.0 license.
See the LICENSE file at the root of this repository for full details.
"""

import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# RSA functions


def generate_rsa_keypair() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """Generate a new RSA key pair for asymmetric encryption.

    Creates a 4096-bit RSA key pair with public exponent of 65537.
    The private key should be kept secure and the public key can be
    shared with other parties for encryption operations.

    Returns:
        tuple[RSAPrivateKey, RSAPublicKey]: A tuple containing the private key
        and corresponding public key.

    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    return private_key, private_key.public_key()


def serialize_public_key(public_key: RSAPublicKey) -> str:
    """Serialize an RSA public key to a base64-encoded PEM string.

    Converts an RSA public key object to PEM format and encodes it in base64
    for easy transmission or storage as a string.

    Args:
        public_key (RSAPublicKey): The RSA public key to serialize.

    Returns:
        str: The base64-encoded PEM representation of the public key.

    """
    return base64.b64encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    ).decode()


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


def rsa_encrypt(public_key: RSAPublicKey, data: bytes) -> bytes:
    """Encrypts data using RSA asymmetric encryption.

    Encrypts the provided data using the public key with OAEP padding
    and SHA256 hashing algorithm for secure encryption.

    Args:
        public_key (RSAPublicKey): The RSA public key to use for encryption.
        data (bytes): The bytes to encrypt.


    Returns:
        bytes: The encrypted data.

    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(private_key: RSAPrivateKey, encrypted_data: bytes) -> bytes:
    """Decrypts data using RSA asymmetric decryption.

    Decrypts the provided encrypted data using the private key with OAEP padding
    and SHA256 hashing algorithm.

    Args:
        private_key (RSAPrivateKey): The RSA private key to use for decryption.
        encrypted_data (bytes): The encrypted bytes to decrypt.

    Returns:
        bytes: The decrypted data.

    """
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# AES functions


def generate_aes_key() -> bytes:
    """Generate a random AES encryption key.

    Creates a cryptographically secure 256-bit (32-byte) random key suitable
    for AES symmetric encryption.

    Returns:
        bytes: A 32-byte random key for use with AES encryption functions.

    """
    return os.urandom(32)


def aes_encrypt(key: bytes, plaintext: str) -> str:
    """Encrypts text using AES symmetric encryption in CFB mode.

    Encrypts the provided plaintext using the AES key in CFB (Cipher Feedback)
    mode with a randomly generated initialization vector. Returns the result
    as a base64-encoded string combining the IV and ciphertext.

    Args:
        key (bytes): The AES encryption key (should be 32 bytes for AES-256).
        plaintext (str): The text string to encrypt.

    Returns:
        str: The base64-encoded encrypted data (IV + ciphertext).

    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()


def aes_decrypt(key: bytes, b64_ciphertext: str) -> str:
    """Decrypts base64-encoded AES encrypted data in CFB mode.

    Decrypts the provided base64-encoded encrypted data using the AES key
    in CFB mode. The encrypted data should be in the format produced by
    aes_encrypt (IV + ciphertext).

    Args:
        key (bytes): The AES decryption key (should be 32 bytes for AES-256).
        b64_ciphertext (str): The base64-encoded encrypted data (IV + ciphertext).

    Returns:
        str: _description_

    """
    data = base64.b64decode(b64_ciphertext)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
