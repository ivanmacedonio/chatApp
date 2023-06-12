from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import * 
from .forms import * 
from .serializers import *

def index(request): #funciona como un login
    if request.user.is_authenticated:
        return redirect('chat')
    if request.method == 'GET': 
        return render(request, 'chat/index.html', {})
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
        else:
            return HttpResponse({'error': 'Usuario no encontrado!'})
        return redirect('chat')

def message_list(request, sender = None, receiver = None): #lista los mensajes o crea uno nuevo, es la sala de chat de 2 personas, es el chat en si 
    if request.method == 'GET': 
        messages = Message.objects.filter(sender_id = sender, receiver_id = receiver, is_read=False) #_id es el identificador que usa el ORM para apuntar a columnas de la tabla 
        message_serializer = MessageSerializer(messages, many=True, context = {'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(message_serializer.data, safe=False) #con save=false, django puede retornar objetos json sin necesidad de que sean diccionarios unicamente 
    
    elif request.method == 'POST': 
        data = JSONParser().parse(request) #parse hace que se pueda almacenar la informacion de request en json sin necesidad de que se envie un formulario en json por post
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request,user)
                return redirect('chat')
    else:
        form = SignUpForm()
        template = 'chat/register.html'
        context = {'form':form}
        return render(request, template, context)

def chat_view(request): #lista los usuarios para chatear
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})

 #-----------------#

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


    

