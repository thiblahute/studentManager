#!/usr/bin/env python
#
#       dbtest.py
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

import unittest
import sitioPrincipal.models as models

class dbTestCase(unittest.TestCase):
    def setUp(self):
        self.ano = models.Ano()
        self.promocion = models.Promocion()
        self.carreraInformatica = models.Carrera()
        self.estudiante1User = models.User()
        self.estudiante1 = models.Alumno()

    def addAno(self):
        self.ano.ano = '2010'
        self.ano.save()
        self.failUnless(isinstance(self.ano, models.Ano))

    def addPromocion(self):
        self.promocion.ano = self.ano
        self.promocion.save()
        self.failUnless(isinstance(self.promocion, models.Promocion))

    def addCarrera(self):
        self.carrera.nombre = "Carrera informatica"
        self.carrera.save()
        self.failUnless(isinstance(self.carrera, models.Carrera))

    def agregarEstudiantes(self):
        self.estudiante1User.username = "estudiante1"
        self.estudiante1User.set_password("estudiante1")
        self.estudiante1User.save()
        self.estudiante1.apelido = "Vargas"
        self.estudiante1.nombre = "david"
        self.estudiante1.promocion = self.promocion
        self.estudiante1.user = self.davidUser
        self.estudiante1.user_id = self.davidUser.id
        self.estudiante1.carrera = self.carreraInformatica
        self.estudiante1.save()
        self.failUnless(isinstance(self.estudiante1, models.Alumno))
