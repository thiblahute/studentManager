# -*- coding: <UTF-8> -*-1

from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response


class LoginForm(forms.Form):
    usario = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget = forms.PasswordInput())

# Create your views here.
def Login (request):
    form = LoginForm() # An unbound form
    return render_to_response('login.html', {'form': form,})
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            pass # Return a 'disabled account' error message
    else:
        pass # Return an 'invalid login' error message.
