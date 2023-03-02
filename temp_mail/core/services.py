import requests
from typing import NamedTuple, Dict
from .exceptions import APIException, UserDataException
from django.conf import settings
import random


class DomainAndLogin(NamedTuple):
    domain: str
    login: str


class Message(NamedTuple):
    id: str
    fromUserMail: str
    subject: str
    date: str
    body: str
    textBody: str
    htmlBody: str


class ResponseData(NamedTuple):
    status: int
    data: Dict
    user_data: Dict


def main_service(request) -> DomainAndLogin:
    """Сервис вывода основной страницы"""
    data = _get_domain_and_login(request)

    if not data.login or not data.domain:
        domain = random.choice(settings.DOMAINS)
        login = ''.join([random.choice(settings.CHARS) for i in range(20)])

        request.session['domain'] = domain
        request.session['login'] = login
        return DomainAndLogin(domain=domain, login=login)
    return data


def get_list_messages_service(request) -> ResponseData:
    """Сервис по получению сообщений пользователя по сессии"""
    data = _get_domain_and_login(request)

    if not data.login or not data.domain:
        raise UserDataException('Ошибка получение данных пользователя')
    try:
        messages = _get_messages(data)
    except APIException:
        raise UserDataException('Ошибка получения данных из api')
    return ResponseData(status=200, data=messages, user_data=data)


def get_one_message_service(request, id) -> ResponseData:
    """Сервис по получению одного сообщения по сессии"""
    data = _get_domain_and_login(request)
    if not data.login or not data.domain:
        raise UserDataException('Ошибка получения данных пользователя')

    try:
        message = _get_one_message(data, id)
    except APIException:
        raise UserDataException('Ошибка получения данных из API')
    return ResponseData(status=200, data=message, user_data=data)


def _get_domain_and_login(request) -> DomainAndLogin:
    """Получаем данные пользователя"""
    domain = request.session.get('domain')
    login = request.session.get('login')
    return DomainAndLogin(domain=domain, login=login)


def _get_messages(user_data: DomainAndLogin) -> list[Message]:
    """Получение списка сообщений"""
    url = f'{settings.API_SEC_MAIL_URL}?action=getMessages&login={user_data.login}&domain={user_data.domain}'
    try:
        messages = requests.get(url).json()
    except Exception:
        raise APIException('Ошибка API')
    return messages


def _get_one_message(user_data: DomainAndLogin, id: int) -> Message:
    """Получение одного сообщения"""
    url = f'{settings.API_SEC_MAIL_URL}?action=readMessage&login={user_data.login}&domain={user_data.domain}&id={id}'
    try:
        message = requests.get(url).json()
    except APIException:
        raise APIException('Ошибка API')
    return Message(id=message['id'],
                   fromUserMail=message['from'],
                   subject=message['subject'],
                   date=message['date'],
                   body=message['body'],
                   textBody=message['textBody'],
                   htmlBody=message['htmlBody'])
