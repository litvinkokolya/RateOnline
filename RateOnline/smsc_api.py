import requests


def get_token():
    '''
    Получение токена авторизации
    '''
    try:
        response = requests.post(
            'https://online.sigmasms.ru/api/login',
            json=dict(
                username='Lomka',
                password='200412'
            )
        )

        if response and response.status_code == 200:
            return response.json().get('token')

    except Exception as e:
        raise e


def send_sms(token, phone, random_number, name_user):
    '''
    Отправка одного сообщения
    :param token: токен авторизации
    :return: id сообщения
    '''
    try:
        response = requests.post(
            'https://online.sigmasms.ru/api/sendings',
            headers=dict(Authorization=token),
            json=dict(
                recipient=phone,
                type='flashcall',
                payload=dict(
                    # убедитесь, что имя отправителя добавлено в ЛК в разделе Компоненты(https://online.sigmasms.ru/#/components)
                    sender='B-Media',
                    text=random_number
                )
            )
        )

        if response and response.status_code == 200:
            return response.json().get('id')

    except Exception as e:
        raise e


def check_status(token, message_id):
    '''
    Проверка статуса сообщения
    :param token: токен авторизации
    :param message_id: id отправленного сообщения
    :return: статус отправки сообщения
    '''
    response = requests.get(
        'https://online.sigmasms.ru/api/sendings/' + message_id,
        headers=dict(Authorization=token)
    )

    if response and response.status_code == 200:
        return response.json().get('state', {}).get('status')
