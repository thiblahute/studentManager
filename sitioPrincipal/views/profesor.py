#!/usr/bin/env python
#
#       profesor.py
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
from django.shortcuts import render_to_response, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

import sitioPrincipal.models as models

class AddPromocionForm(forms.Form):
    ano = forms.CharField(max_length=4)

class AddRamoForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField()
    profesor = forms.CharField(widget=forms.Select(choices=[(profesor.user.username, profesor.nombre+" "+profesor.apelido) for profesor in models.Profesor.objects.all()]))

class AddStudentForm(forms.Form):
    rut = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget = forms.PasswordInput())
    apelido = forms.CharField(max_length=100)
    nombre = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=100)
    telefono_casa = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=100)
    direccion_casa = forms.CharField(max_length=100)
    estado = forms.CharField(max_length=100)
    ano = forms.CharField(widget=forms.Select(choices=[(ano.ano, ano.ano) for ano in models.Ano.objects.all()]))
    carrera = forms.CharField(widget=forms.Select(choices=[(carrera.nombre, carrera.nombre) for carrera in models.Carrera.objects.all()]))

class AsignaturaPromocionForm(forms.Form):
    asignatura = forms.CharField(widget=forms.Select(choices=[(ano.ano, ano.ano) for ano in models.Ano.objects.all()]))
    promocion = forms.CharField(widget=forms.Select(choices=[(promocion.ano.ano, promocion.ano.ano) for promocion in models.Promocion.objects.all()]))

@login_required
def addRamo(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    form = AddRamoForm()
    try:
       nombre = request.POST['nombre']
       descripcion = request.POST['descripcion']
       profesor = request.POST['profesor']
    except:
        return render_to_response('addRamo.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'form': form})
    profesorObj = models.Profesor.objects.filter(user = models.User.objects.filter(username = profesor)[0])[0]
    ramo = models.Ramo()
    ramo.profesor = profesorObj
    ramo.nombre = nombre
    ramo.descripcion = descripcion
    ramo.save()
    return redirect('/menu',
                    permanent=True)

@login_required
def addPromocion(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    form = AddPromocionForm()
    try:
        ano = request.POST['ano']
    except:
        return render_to_response('addPromocion.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'promocion': form})
    if not models.Ano.objects.filter(ano=ano):
        anoObj = models.Ano()
        anoObj.ano = ano
        anoObj.save()
    else:
        anoObj = models.Ano.objects.filter(ano=ano)[0]

    if not models.Promocion.objects.filter(ano=anoObj):
        promocionObj = models.Promocion()
        promocionObj.ano = anoObj
        promocionObj.save()

    return redirect('/menu',
                    permanent=True)

@login_required
def addStudent(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)

    form = AddStudentForm()
    try:
        rut = request.POST['rut']
        contrasena = request.POST['contrasena']
        apelido = request.POST['apelido']
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        telefono_casa = request.POST['telefono_casa']
        direccion = request.POST['direccion']
        direccion_casa = request.POST['direccion_casa']
        estado = request.POST['estado']
        ano = request.POST['ano']
        carrera = request.POST['carrera']
    except:
        return render_to_response('addStudent.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'form': form})

    anoObj = models.Ano.objects.filter(ano=ano)[0]

    promocion = models.Promocion.objects.filter(ano=anoObj)
    if not promocion:
        promocion = models.Promocion()
        promocion.ano = anoObj
        promocion.save()
    else:
        promocion = promocion[0]

    carreraObj = models.Carrera.objects.filter(nombre = carrera)[0]
    user = models.User()
    user.username = rut
    user.set_password(contrasena)
    try:
        user.save()
    except:
        html = "<html><body>" + rut +" ya esta en la base de dato </body></html>"
        return HttpResponse(html)
    alumno = models.Alumno()
    alumno.apelido = apelido
    alumno.nombre = nombre
    alumno.promocion = promocion
    alumno.user = user
    alumno.user_id = user.id
    alumno.carrera = carreraObj
    alumno.save()
    try:
        user.save()
    except:
        models.User.deleete(user)
        html = "<html><body>" + rut +" no a estado agragado</body></html>"
        return HttpResponse(html)


    return redirect("/viewStudents", permanent=True)

def viewStudents(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    alumnos = []
    for alumno in models.Alumno.objects.all():
        alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])

    return render_to_response('viewStudents.html',
                             {'logged' : request.user.is_authenticated(),
                              'alumnos': alumnos})
