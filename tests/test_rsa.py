import pytest
from cryptography.hazmat.primitives.asymmetric import rsa as RSA

from confy_addons import (
    RSAEncryption,
    RSAPublicEncryption,
    deserialize_public_key,
)


def test_rsa_keypair_generation_not_is_none():
    rsa_encryption = RSAEncryption()
    assert rsa_encryption.private_key is not None
    assert rsa_encryption.public_key is not None


def test_rsa_keypair_types():
    rsa = RSAEncryption()
    private_key = rsa.private_key
    public_key = rsa.public_key
    assert isinstance(private_key, RSA.RSAPrivateKey)
    assert isinstance(public_key, RSA.RSAPublicKey)


def test_rsa_keypair_key_size():
    EXPECTED_KEY_SIZE = 4096
    rsa = RSAEncryption()
    private_key = rsa.private_key
    public_key = rsa.public_key
    assert private_key.key_size == EXPECTED_KEY_SIZE
    assert public_key.key_size == EXPECTED_KEY_SIZE


def test_rsa_keypair_public_exponent():
    EXPECTED_PUBLIC_EXPONENT = 65537
    rsa = RSAEncryption()
    private_key = rsa.private_key
    public_key = rsa.public_key
    assert private_key.public_key().public_numbers().e == EXPECTED_PUBLIC_EXPONENT
    assert public_key.public_numbers().e == EXPECTED_PUBLIC_EXPONENT


def test_serialize_public_key_not_empty():
    rsa = RSAEncryption()
    assert rsa.serialized_public_key


def test_serialize_public_key_type():
    rsa = RSAEncryption()
    assert isinstance(rsa.serialized_public_key, bytes)


def test_base64_public_key_type():
    rsa = RSAEncryption()
    assert isinstance(rsa.base64_public_key, str)


def test_serialize_different_keys():
    rsa1 = RSAEncryption()
    rsa2 = RSAEncryption()
    assert rsa1.serialized_public_key != rsa2.serialized_public_key


def test_deserialize_public_key_type():
    rsa = RSAEncryption()
    base64_key = rsa.base64_public_key
    deserialized_key = deserialize_public_key(base64_key)
    assert isinstance(deserialized_key, RSA.RSAPublicKey)


def test_deserialize_public_key_equivalence():
    rsa = RSAEncryption()
    original_public_key = rsa.public_key
    base64_key = rsa.base64_public_key
    deserialized_key = deserialize_public_key(base64_key)
    assert original_public_key.public_numbers() == deserialized_key.public_numbers()


def test_rsa_encrypt_decrypt_cycle():
    rsa = RSAEncryption()
    public_key = rsa.public_key
    rsa_pub = RSAPublicEncryption(public_key)
    data = b'Test message for RSA encryption.'
    encrypted_data = rsa_pub.encrypt(data)
    decrypted_data = rsa.decrypt(encrypted_data)
    assert decrypted_data == data


def test_rsa_encrypt_different_ciphertexts():
    rsa = RSAEncryption()
    public_key = rsa.public_key
    rsa_pub = RSAPublicEncryption(public_key)
    data = b'Test message for RSA encryption.'
    encrypted_data1 = rsa_pub.encrypt(data)
    encrypted_data2 = rsa_pub.encrypt(data)
    assert encrypted_data1 != encrypted_data2


def test_repr_rsa_encryption():
    rsa = RSAEncryption()
    repr_str = repr(rsa)
    assert 'RSAEncryption' in repr_str
    assert 'key_size' in repr_str
    assert 'public_exponent' in repr_str
    assert 'object at' in repr_str


def test_key_size():
    rsa = RSAEncryption()
    assert isinstance(rsa.key_size, int)


def test_repr_rsa_public_encryption():
    rsa = RSAEncryption()
    public_key = rsa.public_key
    rsa_pub = RSAPublicEncryption(public_key)
    repr_str = repr(rsa_pub)
    assert 'RSAPublicEncryption' in repr_str
    assert 'key=' in repr_str
    assert 'object at' in repr_str


def test_rsa_public_encryption_key_type():
    rsa = RSAEncryption()
    public_key = rsa.public_key
    rsa_pub = RSAPublicEncryption(public_key)
    assert isinstance(rsa_pub.key, RSA.RSAPublicKey)


def test_rsa_key_size_not_int():
    with pytest.raises(TypeError) as exc_info:
        RSAEncryption(key_size='not_a_key')
    assert str(exc_info.value) == 'key_size must be an integer'


def test_rsa_decrypt_encrypted_data_not_bytes():
    rsa = RSAEncryption()
    with pytest.raises(TypeError) as exc_info:
        rsa.decrypt('not_bytes')
    assert str(exc_info.value) == 'encrypted_data must be bytes'


def test_rsa_public_encrypt_key_not_rsa_public_key():
    with pytest.raises(TypeError) as exc_info:
        RSAPublicEncryption(key='not_a_public_key')
    assert str(exc_info.value) == 'key must be an instance of RSAPublicKey'


def test_rsa_public_encrypt_data_not_bytes():
    rsa = RSAEncryption()
    public_key = rsa.public_key
    rsa_pub = RSAPublicEncryption(public_key)
    with pytest.raises(TypeError) as exc_info:
        rsa_pub.encrypt('not_bytes')
    assert str(exc_info.value) == 'data must be bytes'
