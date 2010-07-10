from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')

class Ramo(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    descripcion = models.CharField(max_length=500)

    estudiantes = models.ManyToManyField(Persona, related_name='test')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

#mptt.register(Ramo)

class Profesor(Persona):
    apelido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    ramos = models.ManyToManyField(Ramo)
    #Relaciones
    jefeCarrera = models.ForeignKey('Profesor')

class Ano(models.Model):
    ano = models.IntegerField(primary_key=True)
    #Relaciones

class Promocion(models.Model):
    #Relaciones
    ano = models.ForeignKey(Ano)


class Alumno(Persona):
    apelido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    telefono_casa = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    direccion_casa = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    #Relaciones
    carrera = models.ForeignKey(Carrera)
    promocion = models.ForeignKey(Promocion)
    ramo = models.ManyToManyField(Ramo, through='AlumnoRamo')

class AlumnoRamo(models.Model):
    passed = models.IntegerField()
    alumno = models.ForeignKey(Alumno)
    ramo = models.ForeignKey(Ramo)

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    #Relaciones
    ramos = models.ManyToManyField(Ramo)
    jefeCarrera = models.OneToOneField(Profesor)

class Asignatura(models.Model):
    seccion = models.IntegerField()
    periodo =  models.IntegerField()

    #Relaciones
    ano = models.ForeignKey(Ano)
    profesor = models.ForeignKey(Profesor)
    carrera = models.ForeignKey(Carrera)
    ramo = models.ForeignKey(Ramo)
    alumnos = models.ManyToManyField(Alumno, through='AsignAlumno')

class AsignAlumno(models.Model):
    alumno = models.ForeignKey(Alumno)
    asignatura = models.ForeignKey(Asignatura)

class Prueba(models.Model):
    titulo = models.CharField(max_length=100)
    nota = models.FloatField()
    date = models.DateField()

    #Relaciones
    alumno = models.ForeignKey(Alumno)
    asignatura = models.ForeignKey(Asignatura)

class Solicitud(models.Model):
    tipoSolicitud = models.CharField(max_length=100)

    #Relaciones
    asignatura = models.ForeignKey(Asignatura)
    alumno = models.ForeignKey(Alumno)
