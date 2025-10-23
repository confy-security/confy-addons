import binascii

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa as RSA

from confy_addons import (
    RSAEncryption,
    RSAPublicEncryption,
    deserialize_public_key,
)
from confy_addons.core.constants import DEFAULT_RSA_KEY_SIZE
from confy_addons.core.exceptions import (
    DecryptionError,
    EncryptionError,
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


def test_rsa_encrypt_different_cipher_texts():
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


def test_rsa_generate_key_failure_raises_runtime_error(monkeypatch):
    # força generate_private_key a falhar durante a inicialização
    def fake_generate_private_key(*args, **kwargs):
        raise ValueError('simulated failure')

    monkeypatch.setattr(
        'confy_addons.encryption.rsa.rsa.generate_private_key', fake_generate_private_key
    )

    with pytest.raises(RuntimeError, match='Failed to generate RSA key pair'):
        RSAEncryption()


def test_rsa_decrypt_raises_decryption_error_on_private_decrypt_failure():
    rsa = RSAEncryption()

    class DummyPrivateKey:
        @staticmethod
        def decrypt(encrypted_data, padding):
            raise ValueError('simulated decrypt failure')

    # substitui a chave privada do objeto por uma que falha ao descriptografar
    rsa._private_key = DummyPrivateKey()

    with pytest.raises(DecryptionError, match='RSA decryption failed'):
        rsa.decrypt(b'not-valid-ciphertext')


def test_rsa_public_encrypt_raises_encryption_error_on_internal_failure():
    rsa = RSAEncryption()
    rsa_pub = RSAPublicEncryption(rsa.public_key)

    class DummyKey:
        @staticmethod
        def encrypt(*args, **kwargs):
            raise RuntimeError('simulated encrypt failure')

    # substitui a chave interna para forçar falha durante encrypt()
    rsa_pub._key = DummyKey()

    with pytest.raises(EncryptionError, match='RSA encryption failed'):
        rsa_pub.encrypt(b'test data')


def test_deserialize_public_key_raises_on_load_failure(monkeypatch):
    rsa = RSAEncryption()
    b64_key = rsa.base64_public_key

    def fake_load_pem_public_key(_):
        raise ValueError('simulated load failure')

    monkeypatch.setattr(
        'confy_addons.encryption.rsa.serialization.load_pem_public_key', fake_load_pem_public_key
    )

    with pytest.raises(ValueError, match='Failed to load public key from PEM'):
        deserialize_public_key(b64_key)


def test_deserialize_public_key_raises_on_invalid_base64_decode(monkeypatch):
    def fake_b64decode(_, validate=True):
        raise binascii.Error('invalid base64')

    monkeypatch.setattr('confy_addons.encryption.rsa.base64.b64decode', fake_b64decode)

    with pytest.raises(ValueError, match='Invalid base64 public key'):
        deserialize_public_key('not-a-valid-base64')


def test_deserialize_public_key_raises_type_error_for_non_string_input():
    with pytest.raises(TypeError, match='b64_key must be a base64-encoded string'):
        deserialize_public_key(b'not-a-string')


def test_rsa_decrypt_raises_value_error_on_empty_input():
    rsa = RSAEncryption()
    with pytest.raises(ValueError, match='encrypted_data is empty'):
        rsa.decrypt(b'')


def test_rsa_init_raises_on_too_small_key_size():
    small_size = DEFAULT_RSA_KEY_SIZE - 1
    with pytest.raises(
        ValueError, match=f'key_size must be at least {DEFAULT_RSA_KEY_SIZE} bits for security'
    ):
        RSAEncryption(key_size=small_size)


def test_sign_type_error_for_non_bytes():
    rsa = RSAEncryption()
    with pytest.raises(TypeError, match='data must be bytes'):
        rsa.sign('not-bytes')  # tipo inválido


def test_sign_value_error_for_empty_data():
    rsa = RSAEncryption()
    with pytest.raises(ValueError, match='data is empty'):
        rsa.sign(b'')  # vazio


def test_sign_and_verify_success():
    rsa = RSAEncryption()
    data = b'message to sign'
    signature = rsa.sign(data)

    rsa_pub = RSAPublicEncryption(rsa.public_key)
    # verify não retorna nada se OK
    rsa_pub.verify(data, signature)


def test_rsa_sign_raises_runtime_error_on_internal_failure():
    rsa = RSAEncryption()

    class BadPrivateKey:
        @staticmethod
        def sign(*args, **kwargs):
            raise RuntimeError('simulated signing failure')

    rsa._private_key = BadPrivateKey()

    with pytest.raises(RuntimeError, match='RSA signing failed'):
        rsa.sign(b'data to sign')


def test_verify_raises_type_error_for_non_bytes_inputs():
    rsa = RSAEncryption()
    rsa_pub = RSAPublicEncryption(rsa.public_key)

    with pytest.raises(TypeError, match='data and signature must be bytes'):
        rsa_pub.verify('not-bytes', b'sig')

    with pytest.raises(TypeError, match='data and signature must be bytes'):
        rsa_pub.verify(b'data', 'not-bytes')


def test_rsa_public_verify_raises_signature_verification_error_on_unexpected_exception():
    rsa = RSAEncryption()
    rsa_pub = RSAPublicEncryption(rsa.public_key)

    class BadKey:
        @staticmethod
        def verify(*args, **kwargs):
            raise RuntimeError('internal failure')

    rsa_pub._key = BadKey()
    data = b'payload'
    signature = b'signature'

    with pytest.raises(Exception, match=r'Verification error:'):
        rsa_pub.verify(data, signature)
