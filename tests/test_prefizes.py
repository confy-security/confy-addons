from confy_addons.prefixes import AES_KEY_PREFIX, AES_PREFIX, KEY_EXCHANGE_PREFIX, SYSTEM_PREFIX


def test_system_prefix():
    assert SYSTEM_PREFIX == 'system-message:'


def test_key_exchange_prefix():
    assert KEY_EXCHANGE_PREFIX == 'key-exchange:'


def test_aes_key_prefix():
    assert AES_KEY_PREFIX == 'aes-key:'


def test_aes_prefix():
    assert AES_PREFIX == 'enc:'
