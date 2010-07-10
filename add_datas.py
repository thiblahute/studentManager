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
ano.ano = 2010
ano.save()

promocion = models.Promocion()
promocion.ano = ano
promocion.save()

profeUser = models.User()
profeUser.username = "5"
profeUser.set_password("test")
profeUser.save()
profe = models.Profesor()
profe.apelido = "Un profe"
profe.nombre = "sor"
profe.user = profeUser
profe.user_id = profeUser.id
profe.save()


carreraInformatica = models.Carrera()
carreraInformatica.nombre = "Informatica"
carreraInformatica.jefeCarrera = profe
carreraInformatica.save()

introIng = models.Ramo()
introIng.nombre = "Introduction ingénioria"
introIng.save()

fisGraf1 = models.Ramo()
fisGraf1.nombre = "Fis graf 1"
fisGraf1.save()

fisGraf2 = models.Ramo()
fisGraf2.nombre = "Fis graf 2"
fisGraf2.parent = fisGraf1
fisGraf2.save()

IA = models.Ramo()
IA.nombre = "Iteligencia de software"
IA.save()

tm = models.Ramo()
tm.nombre = "Tecnologia multimedia"
tm.profesor = profe
tm.save()

stat = models.Ramo()
stat.nombre = "Estatistica"
stat.save()
