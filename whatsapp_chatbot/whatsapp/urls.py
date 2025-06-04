from django.urls import path
from . import views

urlpatterns = [
    # path('webhook/', views.webhook, name='webhook'),
    path('chat/', views.web_chat, name='web_chat'),
    path('messages/', views.get_messages, name='get_messages'),
]