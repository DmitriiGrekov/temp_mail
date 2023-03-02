from django.urls import path, include
from .views import main, get_messages, get_one_message

urlpatterns = [
    path('', main),
    path('getMessages/', get_messages),
    path('getMessage/<int:id>/', get_one_message)
]
