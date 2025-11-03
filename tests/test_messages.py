from confy_addons.messages import (
    NOT_CONNECT_YOURSELF,
    RECIPIENT_CONNECTED,
    RECIPIENT_NOT_CONNECTED,
    RECIPIENT_NOT_CONNECTED_2,
    THE_OTHER_USER_LOGGED_OUT,
    THIS_ID_ALREADY_IN_USE,
)


def test_the_other_user_logged_out():
    assert THE_OTHER_USER_LOGGED_OUT == 'O outro usuário se desconectou'


def test_not_connect_yourself():
    assert NOT_CONNECT_YOURSELF == 'Você não pode se conectar com você mesmo'


def test_this_id_already_in_use():
    assert THIS_ID_ALREADY_IN_USE == 'Já há um usuário conectado com o ID que você solicitou'


def test_recipient_not_connected():
    assert RECIPIENT_NOT_CONNECTED == (
        'O destinatário ainda não está conectado. Você será notificado quando ele estiver online.'
    )


def test_recipient_connected():
    assert RECIPIENT_CONNECTED == 'O usuário destinatário agora está conectado.'


def test_recipient_not_connected_2():
    assert RECIPIENT_NOT_CONNECTED_2 == 'O outro usuário ainda não está conectado.'
