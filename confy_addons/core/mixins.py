"""Mixin classes for encryption handlers."""


class EncryptionMixin:
    """Mixin class for encryption handlers.

    This mixin provides a common interface for encryption handler classes,
    allowing them to be identified as encryption-related classes.

    """

    def __delattr__(self, _):
        """Prevent deletion of attributes to enhance security.

        Raises:
            AttributeError: Always raised to prevent attribute deletion.

        """
        raise AttributeError('Attribute deletion is not allowed for security reasons')
