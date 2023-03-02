from django.shortcuts import render
from django.http import JsonResponse
from .exceptions import UserDataException
import logging
from .services import (main_service,
                       get_list_messages_service,
                       get_one_message_service)


logger = logging.getLogger(__name__)


def main(request):
    """Обработчик основной страницы"""
    data = main_service(request)
    return render(request, 'core/index_list.html',
                  {'login': data.login, 'domain': data.domain})


def get_messages(request):
    """Получаем список сообщений"""
    try:
        messages = get_list_messages_service(request)
    except UserDataException as e:
        logger.error(e)
    return JsonResponse(messages.data, safe=False)


def get_one_message(request, id):
    """Получаем одно сообщение"""
    try:
        messages = get_one_message_service(request, id)
    except UserDataException as e:
        logger.error(e)
        return render(request, 'core/mail.html', {'error': e})
    return render(request, 'core/mail.html',
                  {'message': messages.data._asdict(),
                   'login': messages.user_data.login,
                   'domain': messages.user_data.domain})
