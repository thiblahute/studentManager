#!/usr/bin/env python
#
#       malla.py
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
import os.path

import sitioPrincipal.models as models

def malla(request):
    username = os.path.basename(request.path)
    alumno = models.Alumno.objects.filter(user=models.User.objects.filter(username=username)[0])[0]
    ramos_aprobados = []
    ramos_no_aprobados = []
    ramos_dar = []
    for ramo in models.Ramo.objects.all():
        estudiantes = [estudiante.user for estudiante in ramo.estudiantes.all()]
        if alumno.user in estudiantes:
            ramos_aprobados.append(ramo.nombre)
        else:
            try:
                estudiantes_parent = [estudiante.user for estudiante in ramo.parent.estudiantes.all()]
            except:
                if ramo.parent is None:
                    ramos_dar.append(ramo.nombre)
                else:
                    ramos_no_aprobados.append(ramo.nombre)
                estudiantes_parent = []
            if alumno.user in estudiantes_parent:
                ramos_dar.append(ramo.nombre)
            else:
                ramos_no_aprobados.append(ramo.nombre)
    return render_to_response('malla.html',
                             {'logged' : request.user.is_authenticated(),
                              'aprobados' : ramos_aprobados,
                              'dar' : ramos_dar,
                              'no_aprobados' : ramos_no_aprobados,
                              'nombre' : alumno.nombre +' '+alumno.apelido})
