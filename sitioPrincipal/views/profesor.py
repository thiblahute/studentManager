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

import datetime
now = datetime.datetime.now()

import sitioPrincipal.models as models

class AnoWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%i" % obj.ano

class CarreraWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % obj.nombre

class RamoWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % obj.nombre

class ProfeWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % obj.nombre+" "+obj.apelido

class AsignaturaWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % str(obj.ano.ano)+' '+obj.ramo.nombre

class StudentWidget(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s" % obj.nombre+' '+obj.apelido

class AddStudentAsignatura(forms.Form):
    alumno = StudentWidget(models.Alumno.objects.filter(estado = 'activo'))
    ano = models.Ano.objects.filter(ano = now.year)[0]
    asignatura = AsignaturaWidget(models.Asignatura.objects.filter(ano=ano))

class AddPromocionForm(forms.Form):
    ano = forms.CharField(max_length=4)

class AddRamoForm(forms.Form):
    nombre = forms.CharField()
    descripcion = forms.CharField()
    profesor = ProfeWidget(models.Profesor.objects.all())

class AddAsignaturaForm(forms.Form):
    seccion = forms.IntegerField()
    periodos = forms.IntegerField()
    ano = AnoWidget(models.Ano.objects.all())
    carrera = CarreraWidget(models.Carrera.objects.all())
    ramo = RamoWidget(models.Ramo.objects.all())
    profesor = ProfeWidget(models.Profesor.objects.all())

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
    ano = AnoWidget(models.Ano.objects.all())
    carrera = CarreraWidget(models.Carrera.objects.all())


class AsignaturaPromocionForm(forms.Form):

    asignatura = AsignaturaWidget(models.Asignatura.objects.all())
    promocion = AnoWidget(models.Ano.objects.all())

@login_required
def addAsignatura(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    form = AddAsignaturaForm()
    try:
       seccion = request.POST['seccion']
       periodos = request.POST['periodos']
       ano = request.POST['ano']
       carrera = request.POST['carrera']
       ramo = request.POST['ramo']
       profesor = request.POST['profesor']
    except:
        return render_to_response('addAsignatura.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'form': form,
                                  'title': "Agregar asignatura"})

    anoObj = models.Ano.objects.filter(ano=ano)[0]
    carreraObj = models.Carrera.objects.filter(id=carrera)[0]
    ramoObj = models.Ramo.objects.filter(nombre=ramo)[0]
    profesorObj = models.Profesor.objects.filter(id=profesor)[0]
    asignatura = models.Asignatura()
    asignatura.ano = anoObj
    asignatura.ramo = ramoObj
    asignatura.carrera = carreraObj
    asignatura.seccion = seccion
    asignatura.periodo = periodos
    asignatura.profesor = profesorObj
    asignatura.save()
    return redirect('/menu',
                    permanent=True)
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
                                  'title': 'Agregar ramo',
                                  'form': form})
    profesorObj = models.Profesor.objects.filter(user = models.User.objects.filter(id = profesor)[0])[0]
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
                                  'title': 'Agregar promocion',
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
                                  'title': 'Agregar estudiante',
                                  'form': form})

    anoObj = models.Ano.objects.filter(ano=ano)[0]

    promocion = models.Promocion.objects.filter(ano=anoObj)
    if not promocion:
        promocion = models.Promocion()
        promocion.ano = anoObj
        promocion.save()
    else:
        promocion = promocion[0]

    carreraObj = models.Carrera.objects.filter(id = carrera)[0]
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
    alumno.estado = 'activo'
    alumno.save()
    try:
        user.save()
    except:
        models.User.deleete(user)
        html = "<html><body>" + rut +" no a estado agragado</body></html>"
        return HttpResponse(html)


    return redirect("/viewStudents", permanent=True)

@login_required
def addAlumnoAsignatura(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    form = AddStudentAsignatura()
    try:
        alumno = request.POST['alumno']
        asignatura = request.POST['asignatura']
    except:
        return render_to_response('addAlumnoAsignatura.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'form': form,
                                  'title': 'Agregar alumnos en asignatura'})
    asignaturaObj = models.Asignatura.objects.filter(id=asignatura)[0]
    alumnoObj = models.Alumno.objects.filter(id=alumno)[0]
    if alumnoObj not in asignaturaObj.alumnos.all():

        p = models.AsignAlumno()
        p.asignatura=asignaturaObj
        p.alumno=alumnoObj
        p.save()
        added = alumnoObj.nombre+" agragado a "+asignaturaObj.ramo.nombre
    else:
        added = alumnoObj.nombre+" estaba ya inscrita en "+asignaturaObj.ramo.nombre
    return render_to_response('addAlumnoAsignatura.html',
                             {'logged' : request.user.is_authenticated(),
                              'form': form,
                              'added': added,
                              'title': 'Agregar alumnos en asignatura'})


@login_required
def viewStudents(request):
    if not models.Profesor.objects.filter(user=request.user):
        return redirect('/menu',
                        permanent=True)
    form = AsignaturaPromocionForm()
    alumnos = []
    try:
       promocion = request.POST['promocion']
       asignatura = request.POST['asignatura']
    except:
        for alumno in models.Alumno.objects.all():
            alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])

        return render_to_response('viewStudents.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'alumnos': alumnos,
                                  'title': 'Ver alumnos',
                                  'form': form})
    if promocion != "":
        ano = models.Ano.objects.filter(ano=promocion)[0]
        promocion = models.Promocion.objects.filter(ano=promocion)[0]

    if asignatura != "":
        asignatura = models.Asignatura.objects.filter(id=asignatura)[0]
        for alumno in asignatura.alumnos.all():
            if promocion == "":
                alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])
            else:
                if alumno.promocion == promocion:
                    alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])
    else:
        for alumno in models.Alumno.objects.all():
            if promocion == "":
                alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])
            else:
                print "%s, %s" %(alumno.promocion.ano.ano, promocion.ano.ano)
                if alumno.promocion.ano.ano == promocion.ano.ano:
                    alumnos.append([alumno.user.username, alumno.nombre, alumno.apelido, alumno.promocion.ano.ano])
                print alumnos

    return render_to_response('viewStudents.html',
                             {'logged' : request.user.is_authenticated(),
                              'title': 'Agregar alumnos',
                              'alumnos': alumnos,
                              'form': form})
