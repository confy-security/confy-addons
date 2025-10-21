import os

import pytest

from confy_addons import AESEncryption

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


def test_aes_encrypt_different_ciphertexts():
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
    assert 'key=' in repr_str
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
