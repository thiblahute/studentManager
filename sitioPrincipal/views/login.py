# -*- coding: <UTF-8> -*-1

from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

class LoginForm(forms.Form):
    usario = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget = forms.PasswordInput())

def log(request):
    if request.user.is_authenticated():
        return redirect('/menu',
                        permanent=True)
    form = LoginForm()
    try:
        username = request.POST['usario']
        password = request.POST['contrasena']
        user = authenticate(username=username, password=password)
    except:
        return render_to_response('login.html',
                                  {'form': form,
                                   'title': "Conection"})
    if user is not None:
        if user.is_active:
            login(request, user)

            return redirect('/menu',
                            permanent=True)
        else:
            return render_to_response('login.html',
                                     {'form': form,
                                      'title': 'Conection',
                                      'username' : username+" esta inactivo"})
    else:
        return render_to_response('login.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'title': 'Conection',
                                  'form': form,
                                  'username' : username + " y su contrasena no corresponden"})
def logOut(request):
    logout(request)
    return redirect('/login',
                    permanent=True)
