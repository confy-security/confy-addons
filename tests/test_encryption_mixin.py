import pytest

from confy_addons.core.mixins import EncryptionMixin


def test_raise_on_delete_attr():
    """Test that deleting an attribute raises AttributeError."""
    mixin = EncryptionMixin()
    with pytest.raises(AttributeError) as exc_info:
        del mixin.some_attribute
    assert str(exc_info.value) == 'Attribute deletion is not allowed for security reasons'
