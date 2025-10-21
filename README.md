<h1 align="center">
  <a href="https://github.com/confy-security/confy-addons" target="_blank" rel="noopener noreferrer">
    <picture>
      <img width="80" src="https://github.com/confy-security/assets/blob/main/img/confy-app-icon.png?raw=true">
    </picture>
  </a>
  <br>
  Confy Addons
</h1>

<p align="center">Componentes adicionais de aplicativos clientes Confy.</p>

<div align="center">

[![Test](https://github.com/confy-security/confy-addons/actions/workflows/test.yml/badge.svg)](https://github.com/confy-security/confy-addons/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/confy-security/confy-addons.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/confy-security/confy-addons)
[![PyPI - Version](https://img.shields.io/pypi/v/confy-addons?color=blue)](https://pypi.org/project/confy-addons/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/confy-addons)](https://pypi.org/project/confy-addons/)
[![GitHub License](https://img.shields.io/github/license/confy-security/confy-addons?color=blue)](/LICENSE)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=confy-security%2Fconfy-addons&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/confy-security/confy-addons)
  
</div>

---

A Python package that provides symmetric and asymmetric encryption functions for client applications of the Confy encrypted communication system, as well as prefixes that identify messages and encryption keys sent by applications during the handshake process. The package also includes functions to encode and decode the public RSA key to `base64` for sending over the network.

Learn more about the project at [github.com/confy-security](https://github.com/confy-security)

Made with dedication by students from Brazil 🇧🇷.

## ⚡ Using

### Install the package

Install the package with the package manager used in your project.

For example, with pip:

```shell
pip install confy-addons
```

Or with Poetry:

```shell
poetry add confy-addons
```

### Usage example

#### Import the necessary classes

```python
from confy_addons import (
    AESEncryption,
    RSAEncryption,
    RSAPublicEncryption,
    deserialize_public_key,
)
```

This imports all the encryption classes and utilities needed for RSA and AES operations.

#### Generate an RSA key pair

```python
rsa_handler = RSAEncryption()
private_key = rsa_handler.private_key
```

Creates a new RSA encryption handler that automatically generates a 4096-bit key pair. The private key is extracted for later decryption operations.

#### Serialize and share the public key

```python
pub_key_b64 = rsa_handler.base64_public_key
deserialized_pub_key = deserialize_public_key(pub_key_b64)
```

The public key is serialized to a base64-encoded PEM format, which can be safely transmitted over text-based protocols. The deserialized version is reconstructed from the encoded string for encryption operations.

#### Create an RSA public encryption handler

```python
rsa_public_handler = RSAPublicEncryption(key=deserialized_pub_key)
```

Initializes an RSA encryption handler using only the public key. This handler can encrypt data that only the holder of the private key can decrypt.

#### Generate and encrypt an AES key

```python
aes_handler = AESEncryption()
encrypted_aes_key = rsa_public_handler.encrypt(aes_handler.key)
```

Generates a random 256-bit AES key and encrypts it using RSA public key encryption. This allows secure transmission of the symmetric key to the recipient.

#### Decrypt the AES key with the RSA private key

```python
decrypted_aes_key = rsa_handler.decrypt(encrypted_aes_key)
aes_handler_decrypted = AESEncryption(key=decrypted_aes_key)
```

Decrypts the AES key using the RSA private key. A new AES handler is created with the decrypted key for symmetric encryption and decryption operations.

#### Encrypt and decrypt messages with AES

```python
secret_message = "Secret message"
encrypted_message = aes_handler.encrypt(secret_message)
decrypted_message = aes_handler_decrypted.decrypt(encrypted_message)
print(decrypted_message)
```

Encrypts a plaintext message using AES-256 in CFB mode and then decrypts it back to verify the process works correctly. The output will display the original secret message.

## Dependencies

Confy Addons relies only on [`cryptography`](https://cryptography.io/).

## License

Confy Addons is open source software licensed under the [GPL-3.0](https://github.com/confy-security/confy-addons/blob/main/LICENSE) license.
