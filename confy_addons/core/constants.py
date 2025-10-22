"""Module defines constants used throughout the Confy encryption system."""

import logging
from typing import Final

DEFAULT_RSA_KEY_SIZE: Final[int] = 4096
RSA_PUBLIC_EXPONENT: Final[int] = 65537
AES_KEY_SIZE: Final[int] = 32  # 256 bits
AES_IV_SIZE: Final[int] = 16  # 128 bits
LOGGER_LEVEL: Final[int] = logging.INFO
