from django.contrib import admin
from django.urls import path, include
from .views import * 
from django.contrib.auth.views import logout

urlpatterns = [
    path('', index, name='index'),
    #----------#
    path('chat/', chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name='message-list'),
    #----------#
    path('logout/', logout, name='logout'),
    path('register/', register_view, name='register'),
    
]
