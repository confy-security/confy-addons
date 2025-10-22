import base64
import binascii
import os

import pytest

from confy_addons import AESEncryption
from confy_addons.core.constants import AES_IV_SIZE
from confy_addons.core.exceptions import DecryptionError, EncryptionError

AES_KEY_LEN = 32  # 256 bits


def test_aes_key_generation_length():
    aes = AESEncryption()
    assert len(aes.key) == AES_KEY_LEN


def test_aes_key_uniqueness():
    aes1 = AESEncryption()
    aes2 = AESEncryption()
    assert aes1.key != aes2.key


def test_aes_encrypt_decrypt_cycle():
    aes = AESEncryption()
    original_data = 'This is a test message for AES encryption and decryption.'
    encrypted_data = aes.encrypt(original_data)
    decrypted_data = aes.decrypt(encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_different_cipher_texts():
    aes = AESEncryption()
    data = 'Same message for encryption.'
    encrypted_data1 = aes.encrypt(data)
    encrypted_data2 = aes.encrypt(data)
    assert encrypted_data1 != encrypted_data2


def test_aes_encrypt_empty_string():
    aes = AESEncryption()
    original_data = ''
    encrypted_data = aes.encrypt(original_data)
    decrypted_data = aes.decrypt(encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_large_data():
    aes = AESEncryption()
    original_data = 'A' * 10**6  # 1 MB of data
    encrypted_data = aes.encrypt(original_data)
    decrypted_data = aes.decrypt(encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_non_ascii_data():
    aes = AESEncryption()
    original_data = '这是一条用于AES加密和解密的测试消息。'
    encrypted_data = aes.encrypt(original_data)
    decrypted_data = aes.decrypt(encrypted_data)
    assert original_data == decrypted_data


def test_repr_aes_encryption():
    aes = AESEncryption()
    repr_str = repr(aes)
    assert 'AESEncryption' in repr_str
    assert 'key=<hidden>' in repr_str
    assert 'object at' in repr_str


def test_aes_key_type():
    aes = AESEncryption()
    assert isinstance(aes.key, bytes)


def test_aes_key_very_large_length_raises():
    with pytest.raises(ValueError, match='AES key must be 32 bytes'):
        AESEncryption(key=os.urandom(64))  # 512 bits


def test_aes__key():
    key = os.urandom(32)
    aes = AESEncryption(key=key)
    assert aes._key == key


def test_aes_key_size():
    key_size = AESEncryption().key_size
    assert key_size == 32  # noqa
    assert isinstance(key_size, int)


def test_aes_init_invalid_key_type_raises():
    with pytest.raises(TypeError, match='AES key must be bytes or bytearray'):
        AESEncryption(key='not-bytes')


def test_aes_encrypt_invalid_plaintext_type_raises():
    aes = AESEncryption()
    with pytest.raises(TypeError, match='plaintext must be a str'):
        aes.encrypt(b'not-a-str')


def test_aes_encrypt_raises_encryption_error_on_cipher_failure(monkeypatch):
    aes = AESEncryption()

    class DummyEncryptor:
        @staticmethod
        def update(data):
            raise RuntimeError('encryptor failure')

        @staticmethod
        def finalize():
            return b''

    class DummyCipher:
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def encryptor():
            return DummyEncryptor()

    # substitui Cipher usado no módulo para acionar o except geral
    monkeypatch.setattr('confy_addons.encryption.aes.Cipher', DummyCipher)

    with pytest.raises(EncryptionError, match='Error occurred during encryption'):
        aes.encrypt('test')


def test_aes_decrypt_invalid_b64_type_raises():
    aes = AESEncryption()
    with pytest.raises(TypeError, match='b64_ciphertext must be a base64-encoded str'):
        aes.decrypt(b'not-a-str')


def test_aes_decrypt_raises_on_base64_decode_error(monkeypatch):
    aes = AESEncryption()

    def fake_b64decode(_):
        raise binascii.Error('invalid base64')

    # força base64.b64decode a lançar dentro do módulo alvo
    monkeypatch.setattr('confy_addons.encryption.aes.base64.b64decode', fake_b64decode)

    with pytest.raises(ValueError, match='Invalid base64 encrypted data'):
        aes.decrypt('this-is-not-base64')


def test_aes_decrypt_data_too_short_raises():
    aes = AESEncryption()
    # cria dados decodificados com tamanho menor que o IV esperado
    short = b'\x00' * (AES_IV_SIZE - 1)
    b64 = base64.b64encode(short).decode('ascii')

    with pytest.raises(
        ValueError, match='Encrypted data is too short to contain an IV and ciphertext'
    ):
        aes.decrypt(b64)


def test_aes_decrypt_raises_decryption_error_on_cipher_failure(monkeypatch):
    aes = AESEncryption()

    # creates valid payload (IV + at least one byte of ciphertext) to pass initial validations
    fake_payload = b'\x00' * AES_IV_SIZE + b'\x01'
    b64 = base64.b64encode(fake_payload).decode('ascii')

    class DummyDecryptor:
        @staticmethod
        def update(data):
            raise RuntimeError('decryptor failure')

        @staticmethod
        def finalize():
            return b''

    class DummyCipher:
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def decryptor():
            return DummyDecryptor()

    # substitui Cipher usado no módulo para acionar o except geral dentro de decrypt()
    monkeypatch.setattr('confy_addons.encryption.aes.Cipher', DummyCipher)

    with pytest.raises(DecryptionError, match='Decryption failed'):
        aes.decrypt(b64)
