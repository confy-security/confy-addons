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
[![GitHub License](https://img.shields.io/github/license/confy-security/confy-addons?color=blue)](/LICENSE)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=confy-security%2Fconfy-addons&label=repository%20visits&countColor=%231182c3&style=flat)](https://github.com/confy-security/confy-addons)
  
</div>

---

<details><summary>➡️ Click here for English version</summary><br>

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

### Role of each function

#### `aes_decrypt`

The `aes_decrypt` function is responsible for decrypting data that was encrypted using the AES algorithm. It receives as input the encrypted base64-encoded data and the AES key, and returns the original data.

```python
def aes_decrypt(key: bytes, b64_ciphertext: str):
    data = base64.b64decode(b64_ciphertext)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
```

#### `aes_encrypt`

The `aes_encrypt` function is responsible for encrypting data using the AES algorithm. It takes the original data and the AES key as input and returns the encrypted data.

```python
def aes_encrypt(key: bytes, plaintext: str):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()
```

#### `deserialize_public_key`

The `deserialize_public_key` function is responsible for decoding an RSA public key that has been encoded in base64. It receives the public key in base64 format as input and returns the public key object.

```python
def deserialize_public_key(b64_key):
    key_bytes = base64.b64decode(b64_key.encode())
    return serialization.load_pem_public_key(key_bytes)
```

#### `generate_aes_key`

The `generate_aes_key` function generates a random 32-byte (256-bit) AES key for use in symmetric encryption.

```python
def generate_aes_key():
    return os.urandom(32)
```

#### `generate_rsa_keypair`

The `generate_rsa_keypair` function generates an RSA key pair (public and private) for use in asymmetric encryption.

```python
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    return private_key, private_key.public_key()
```

#### `rsa_decrypt`

The `rsa_decrypt` function is responsible for decrypting data that was encrypted using the RSA algorithm. It receives the encrypted data and the RSA private key as input, and returns the original data.

```python
def rsa_decrypt(private_key, encrypted_data: bytes):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
```

#### `rsa_encrypt`

The `rsa_encrypt` function is responsible for encrypting data using the RSA algorithm. It takes the original data and the RSA public key as input and returns the encrypted data.

```python
def rsa_encrypt(public_key, data: bytes):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
```

#### `serialize_public_key`

The `serialize_public_key` function is responsible for encoding an RSA public key in base64 format. It receives the public key object as input and returns the base64-encoded key.

```python
def serialize_public_key(public_key):
    return base64.b64encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    ).decode()
```

### Usage example

```python
from confy_addons.encryption import (
    aes_decrypt,
    aes_encrypt,
    deserialize_public_key,
    generate_aes_key,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_encrypt,
    serialize_public_key,
)

# Generating RSA key pair
pk, pub_key = generate_rsa_keypair()

# Encoding public key to base64
pub_b64 = serialize_public_key(pub_key)

# Decoding public key from base64
decoded_pub_key = deserialize_public_key(pub_b64)

# Generating random AES key
aes_key = generate_aes_key()

# Encrypting AES key with RSA keys
encrypted_aes_key = rsa_encrypt(decoded_pub_key, aes_key)

# Decrypting AES key with RSA private key
rsa_decrypt(pk, encrypted_aes_key)

# Encrypting message with AES key
aes_encrypted_msg = aes_encrypt(aes_key, "Secret message")

# Decrypting message with AES key
decrypted_msg = aes_decrypt(aes_key, aes_encrypted_msg)

print(decrypted_msg) # Output: Secret message
```

## 📜 License

Confy Addons is open source software licensed under the [GPL-3.0](https://github.com/confy-security/confy-addons/blob/main/LICENSE) license.

</details>

Pacote Python que fornece as funções de criptografia simétrica e assimétrica para os aplicativos clientes do sistema Confy de comunicação criptografada, assim como os prefixos que identificam as mensagens e chaves de criptografia enviadas pelos aplicativos durante o processo de *handshake*. O pacote também inclui funções de encode e decode da chave RSA pública para `base64`, para fins de envio pela rede.

Saiba mais sobre o projeto em [github.com/confy-security](https://github.com/confy-security)

Feito com dedicação por estudantes do Brasil 🇧🇷.

## ⚡ Utilizando

### Instale o pacote

Instale o pacote com o gerenciador de pacotes usado no seu projeto.

Por exemplo, com pip:

```shell
pip install confy-addons
```

Ou com Poetry:

```shell
poetry add confy-addons
```

### Papel de cada função

#### `aes_decrypt`

A função `aes_decrypt` é responsável por descriptografar dados que foram criptografados usando o algoritmo AES. Ela recebe como entrada os dados criptografados codificados em base64 e a chave AES, e retorna os dados originais.

```python
def aes_decrypt(key: bytes, b64_ciphertext: str):
    data = base64.b64decode(b64_ciphertext)
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()
```

#### `aes_encrypt`

A função `aes_encrypt` é responsável por criptografar dados usando o algoritmo AES. Ela recebe como entrada os dados originais e a chave AES, e retorna os dados criptografados.

```python
def aes_encrypt(key: bytes, plaintext: str):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()
```

#### `deserialize_public_key`

A função `deserialize_public_key` é responsável por decodificar uma chave pública RSA que foi codificada em base64. Ela recebe como entrada a chave pública em formato base64 e retorna o objeto da chave pública.

```python
def deserialize_public_key(b64_key):
    key_bytes = base64.b64decode(b64_key.encode())
    return serialization.load_pem_public_key(key_bytes)
```

#### `generate_aes_key`

A função `generate_aes_key` é responsável por gerar uma chave AES aleatória de 32 bytes (256 bits) para uso na criptografia simétrica.

```python
def generate_aes_key():
    return os.urandom(32)
```

#### `generate_rsa_keypair`

A função `generate_rsa_keypair` é responsável por gerar um par de chaves RSA (pública e privada) para uso na criptografia assimétrica.

```python
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    return private_key, private_key.public_key()
```

#### `rsa_decrypt`

A função `rsa_decrypt` é responsável por descriptografar dados que foram criptografados usando o algoritmo RSA. Ela recebe como entrada os dados criptografados e a chave privada RSA, e retorna os dados originais.

```python
def rsa_decrypt(private_key, encrypted_data: bytes):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
```

#### `rsa_encrypt`

A função `rsa_encrypt` é responsável por criptografar dados usando o algoritmo RSA. Ela recebe como entrada os dados originais e a chave pública RSA, e retorna os dados criptografados.

```python
def rsa_encrypt(public_key, data: bytes):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
```

#### `serialize_public_key`

A função `serialize_public_key` é responsável por codificar uma chave pública RSA em formato base64. Ela recebe como entrada o objeto da chave pública e retorna a chave codificada em base64.

```python
def serialize_public_key(public_key):
    return base64.b64encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    ).decode()
```

### Exemplo de uso

```python
from confy_addons.encryption import (
    aes_decrypt,
    aes_encrypt,
    deserialize_public_key,
    generate_aes_key,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_encrypt,
    serialize_public_key,
)

# Gerando par de chaves RSA
pk, pub_key = generate_rsa_keypair()

# Codificando chave pública para base64
pub_b64 = serialize_public_key(pub_key)

# Decodificando chave pública de base64
decoded_pub_key = deserialize_public_key(pub_b64)

# Gerando chave AES aleatória
aes_key = generate_aes_key()

# Criptografando chave AES com chaves RSA
encrypted_aes_key = rsa_encrypt(decoded_pub_key, aes_key)

# Descriptografando chave AES com chave privada RSA
rsa_decrypt(pk, encrypted_aes_key)

# Criptografando mensagem com chave AES
aes_encrypted_msg = aes_encrypt(aes_key, "Mensagem secreta")

# Descriptografando mensagem com chave AES
decrypted_msg = aes_decrypt(aes_key, aes_encrypted_msg)

print(decrypted_msg)  # Output: Mensagem secreta
```

## 📜 Licença

Confy Addons é um software de código aberto licenciado sob a Licença [GPL-3.0](https://github.com/confy-security/confy-addons/blob/main/LICENSE).
