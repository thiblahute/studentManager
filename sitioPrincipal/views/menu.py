#!/usr/bin/env python
#
#       menu.py
#
# Copyright (C) 2010 Thibault Saunier <tsaunier@gnome.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import sitioPrincipal.models as models

@login_required
def menu(request):
    user = request.user
    profe = models.Profesor.objects.filter(user=user)
    if profe:
        profe=profe[0]
        return render_to_response('menu.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'title': 'Menu principal',
                                  'nombreUsario': profe.nombre +
                                  " "+ profe.apelido, 'rut' : user.username})

    alumno = models.Alumno.objects.filter(user=user)[0]
    ano = alumno.promocion.ano.ano
    carrera = alumno.carrera.nombre
    return render_to_response('menu.html',
                              { 'logged' : request.user.is_authenticated(),
                                'title': 'Menu principal',
                                'nombreUsario': alumno.nombre +' '+ alumno.apelido,
                                'rut' : user.username,
                                'ano': ano,
                                'alumno' : True,
                                'carrera': carrera})
