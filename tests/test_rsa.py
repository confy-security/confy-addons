from cryptography.hazmat.primitives.asymmetric import rsa

from confy_addons.encryption import (
    deserialize_public_key,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_encrypt,
    serialize_public_key,
)


def test_rsa_keypair_generation_not_is_none():
    private_key, public_key = generate_rsa_keypair()
    assert private_key is not None
    assert public_key is not None


def test_rsa_keypair_types():
    private_key, public_key = generate_rsa_keypair()
    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert isinstance(public_key, rsa.RSAPublicKey)


def test_rsa_keypair_key_size():
    EXPECTED_KEY_SIZE = 4096
    private_key, public_key = generate_rsa_keypair()
    assert private_key.key_size == EXPECTED_KEY_SIZE
    assert public_key.key_size == EXPECTED_KEY_SIZE


def test_rsa_keypair_public_exponent():
    EXPECTED_PUBLIC_EXPONENT = 65537
    private_key, public_key = generate_rsa_keypair()
    assert private_key.public_key().public_numbers().e == EXPECTED_PUBLIC_EXPONENT
    assert public_key.public_numbers().e == EXPECTED_PUBLIC_EXPONENT


def test_serialize_public_key_not_empty():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    assert serialized_key


def test_serialize_public_key_type():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    assert isinstance(serialized_key, str)


def test_serialize_public_key_length():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    assert len(serialized_key) > 200  # Arbitrary length check # noqa


def test_serialize_different_keys():
    _, public_key1 = generate_rsa_keypair()
    _, public_key2 = generate_rsa_keypair()
    serialized_key1 = serialize_public_key(public_key1)
    serialized_key2 = serialize_public_key(public_key2)
    assert serialized_key1 != serialized_key2


def test_deserialize_public_key_type():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    deserialized_key = deserialize_public_key(serialized_key)
    assert isinstance(deserialized_key, rsa.RSAPublicKey)


def test_deserialize_public_key_equivalence():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    deserialized_key = deserialize_public_key(serialized_key)
    assert public_key.public_numbers() == deserialized_key.public_numbers()


def test_serialize_deserialize_cycle():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    deserialized_key = deserialize_public_key(serialized_key)
    re_serialized_key = serialize_public_key(deserialized_key)
    assert serialized_key == re_serialized_key


def test_deserialize_serialized_cycle():
    _, public_key = generate_rsa_keypair()
    serialized_key = serialize_public_key(public_key)
    deserialized_key = deserialize_public_key(serialized_key)
    re_deserialized_key = deserialize_public_key(serialize_public_key(deserialized_key))
    assert deserialized_key.public_numbers() == re_deserialized_key.public_numbers()


def test_rsa_encrypt_decrypt_cycle():
    private_key, public_key = generate_rsa_keypair()
    original_data = b'This is a test message for RSA encryption and decryption.'
    encrypted_data = rsa_encrypt(public_key, original_data)
    decrypted_data = rsa_decrypt(private_key, encrypted_data)
    assert original_data == decrypted_data


def test_rsa_encrypt_different_ciphertexts():
    _, public_key = generate_rsa_keypair()
    data = b'Same message for encryption.'
    encrypted_data1 = rsa_encrypt(public_key, data)
    encrypted_data2 = rsa_encrypt(public_key, data)
    assert encrypted_data1 != encrypted_data2
