"""
This module defines all the functions used by client applications
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
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    return private_key, private_key.public_key()


def serialize_public_key(public_key: RSAPublicKey) -> str:
    return base64.b64encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    ).decode()


def deserialize_public_key(b64_key: str) -> PublicKeyTypes:
    key_bytes = base64.b64decode(b64_key.encode())
    return serialization.load_pem_public_key(key_bytes)


def rsa_encrypt(public_key: RSAPublicKey, data: bytes) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(private_key: RSAPrivateKey, encrypted_data: bytes) -> bytes:
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# AES
def generate_aes_key() -> bytes:
    return os.urandom(32)


def aes_encrypt(key: bytes, plaintext: str) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()


def aes_decrypt(key: bytes, b64_ciphertext: str) -> str:
    data = base64.b64decode(b64_ciphertext)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
