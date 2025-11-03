"""Module defines string prefixes used for different types of messages and keys.

This file is licensed under the GNU GPL-3.0 license.
See the LICENSE file at the root of this repository for full details.
"""

from typing import Final

SYSTEM_PREFIX: Final[str] = 'system-message:'
KEY_EXCHANGE_PREFIX: Final[str] = 'key-exchange:'
AES_KEY_PREFIX: Final[str] = 'aes-key:'
AES_PREFIX: Final[str] = 'enc:'
SYSTEM_ERROR_PREFIX: Final[str] = 'system-error:'
