from confy_addons.http_messages import (
    DETAIL_RECIPIENT_IS_ALREADY_CHATTING,
    DETAIL_USERNAME_NOT_AVAILABLE,
    MESSAGE_AVAILABLE_RECIPIENT,
    MESSAGE_USERNAME_AVAILABLE,
)


def test_detail_username_not_available():
    assert DETAIL_USERNAME_NOT_AVAILABLE == 'Este nome de usuário não está disponível'


def test_message_username_available():
    assert MESSAGE_USERNAME_AVAILABLE == 'O nome de usuário está disponível'


def test_detail_recipient_is_already_chatting():
    assert DETAIL_RECIPIENT_IS_ALREADY_CHATTING == 'Destinatário já está em uma conversa ativa'


def test_message_available_recipient():
    assert MESSAGE_AVAILABLE_RECIPIENT == 'Destinatário disponível para conexão'
