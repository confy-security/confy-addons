"""Module defining custom exceptions for encryption and decryption errors.

This module provides specific exception classes to handle errors that may
occur during encryption and decryption processes.
"""


class EncryptionError(Exception):
    pass


class DecryptionError(Exception):
    pass
