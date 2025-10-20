from confy_addons.encryption import aes_decrypt, aes_encrypt, generate_aes_key

AES_KEY_LEN = 32  # 256 bits


def test_aes_key_generation_length():
    key = generate_aes_key()
    assert len(key) == AES_KEY_LEN


def test_aes_key_uniqueness():
    key1 = generate_aes_key()
    key2 = generate_aes_key()
    assert key1 != key2


def test_aes_encrypt_decrypt_cycle():
    key = generate_aes_key()
    original_data = 'This is a test message for AES encryption and decryption.'
    encrypted_data = aes_encrypt(key, original_data)
    decrypted_data = aes_decrypt(key, encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_different_ciphertexts():
    key = generate_aes_key()
    data = 'Same message for encryption.'
    encrypted_data1 = aes_encrypt(key, data)
    encrypted_data2 = aes_encrypt(key, data)
    assert encrypted_data1 != encrypted_data2


def test_aes_encrypt_empty_string():
    key = generate_aes_key()
    original_data = ''
    encrypted_data = aes_encrypt(key, original_data)
    decrypted_data = aes_decrypt(key, encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_large_data():
    key = generate_aes_key()
    original_data = 'A' * 10**6  # 1 MB of data
    encrypted_data = aes_encrypt(key, original_data)
    decrypted_data = aes_decrypt(key, encrypted_data)
    assert original_data == decrypted_data


def test_aes_encrypt_non_ascii_data():
    key = generate_aes_key()
    original_data = '这是一条用于AES加密和解密的测试消息。'
    encrypted_data = aes_encrypt(key, original_data)
    decrypted_data = aes_decrypt(key, encrypted_data)
    assert original_data == decrypted_data
