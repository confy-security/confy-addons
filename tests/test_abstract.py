"""Tests for abstract base class for encryption handlers."""

import pytest

from confy_addons.core.abstract import AESEncryptionABC


class ConcreteAESEncryption(AESEncryptionABC):
    """Concrete implementation of AESEncryptionABC for testing purposes."""

    @staticmethod
    def encrypt(plaintext: str) -> str:
        return plaintext[::-1]

    @staticmethod
    def decrypt(ciphertext: str) -> str:
        return ciphertext[::-1]


def test_cannot_instantiate_abstract_class():
    """Test that AESEncryptionABC cannot be instantiated directly."""
    with pytest.raises(TypeError):
        AESEncryptionABC()


def test_concrete_class_can_be_instantiated():
    """Test that a concrete implementation can be instantiated."""
    cipher = ConcreteAESEncryption()
    assert isinstance(cipher, AESEncryptionABC)
    assert cipher is not None


def test_encrypt_method_exists():
    """Test that encrypt method is defined in abstract class."""
    assert hasattr(AESEncryptionABC, 'encrypt')
    assert callable(getattr(AESEncryptionABC, 'encrypt'))


def test_decrypt_method_exists():
    """Test that decrypt method is defined in abstract class."""
    assert hasattr(AESEncryptionABC, 'decrypt')
    assert callable(getattr(AESEncryptionABC, 'decrypt'))


def test_encrypt_returns_string():
    """Test that encrypt method returns a string."""
    cipher = ConcreteAESEncryption()
    result = cipher.encrypt('hello')
    assert isinstance(result, str)


def test_decrypt_returns_string():
    """Test that decrypt method returns a string."""
    cipher = ConcreteAESEncryption()
    result = cipher.decrypt('olleh')
    assert isinstance(result, str)


def test_encrypt_with_empty_string():
    """Test encrypt method with empty string."""
    cipher = ConcreteAESEncryption()
    result = cipher.encrypt('')
    assert not result


def test_decrypt_with_empty_string():
    """Test decrypt method with empty string."""
    cipher = ConcreteAESEncryption()
    result = cipher.decrypt('')
    assert not result


def test_encrypt_decrypt_roundtrip():
    """Test that encrypt followed by decrypt returns original text."""
    cipher = ConcreteAESEncryption()
    original_text = 'Hello, World!'
    encrypted = cipher.encrypt(original_text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == original_text


def test_encrypt_with_special_characters():
    """Test encrypt method with special characters."""
    cipher = ConcreteAESEncryption()
    text = '!@#$%^&*()'
    encrypted = cipher.encrypt(text)
    assert isinstance(encrypted, str)
    assert len(encrypted) == len(text)


def test_encrypt_with_unicode_characters():
    """Test encrypt method with unicode characters."""
    cipher = ConcreteAESEncryption()
    text = 'Olá, 世界! 🌍'
    encrypted = cipher.encrypt(text)
    assert isinstance(encrypted, str)


def test_decrypt_with_unicode_characters():
    """Test decrypt method with unicode characters."""
    cipher = ConcreteAESEncryption()
    text = 'Olá, 世界! 🌍'
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text


def test_encrypt_with_multiline_text():
    """Test encrypt method with multiline text."""
    cipher = ConcreteAESEncryption()
    text = 'Line 1\nLine 2\nLine 3'
    encrypted = cipher.encrypt(text)
    assert isinstance(encrypted, str)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text


def test_concrete_implementation_is_subclass():
    """Test that concrete implementation is a subclass of ABC."""
    assert issubclass(ConcreteAESEncryption, AESEncryptionABC)


def test_abstract_methods_are_marked():
    """Test that methods are marked as abstract."""
    abstract_methods = AESEncryptionABC.__abstractmethods__
    assert 'encrypt' in abstract_methods
    assert 'decrypt' in abstract_methods
    assert len(abstract_methods) == 2
