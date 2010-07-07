#!/usr/bin/env python
#
#       add_datas.py
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
# Boston, MA 02110-1307, USA.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

from sitioPrincipal import models

ano = models.Ano()
ano.ano = 2007
ano.save()

promocion = models.Promocion()
promocion.ano = ano
promocion.save()

mbrunoUser = models.User()
mbrunoUser.username = "5"
mbrunoUser.set_password("test")
mbrunoUser.save()
mbruno = models.Profesor()
mbruno.apelido = "Un profe"
mbruno.nombre = "sor"
mbruno.user = mbrunoUser
mbruno.user_id = mbrunoUser.id
mbruno.save()


carreraInformatica = models.Carrera()
carreraInformatica.nombre = "Informatica"
carreraInformatica.jefeCarrera = mbruno
carreraInformatica.save()


davidUser = models.User()
davidUser.username = "123.369.125-1"
davidUser.set_password("test")
davidUser.save()
david = models.Alumno()
david.apelido = "Vargas"
david.nombre = "david"
david.promocion = promocion
david.user = davidUser
david.user_id = davidUser.id
david.carrera = carreraInformatica
david.save()

testUser = models.User()
testUser.username = "23.037.160-1"
testUser.set_password("test")
testUser.save()
test = models.Profesor()
test.apelido = "test"
test.nombre = "Test"
test.user = testUser
test.user_id = testUser.id
test.save()

IA = models.Ramo()
IA.nombre = "Inteligencia Artificial"
IA.profesor = mbruno
IA.save()
IA.estudiantes.add(david)
IA.save()

stat = models.Ramo()
stat.nombre = "Estatistica"
stat.profesor = test
stat.save()
stat.estudiantes.add(david)
stat.save()
