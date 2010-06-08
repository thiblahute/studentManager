from django.db import models

class Ramo(models.Model):
    pass

class Profesor(models.Model):
    pass

class Promocion(models.Model):
    pass

class Alumno(models.Model):
    pass

class Ano(models.Model):
    pass

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    #Relaciones
    ramos = models.ManyToManyField(Ramo)
    jefeCarrera = models.OneToOneField(Profesor)

# Create your models here.
class Profesor(models.Model):
    rut = models.CharField(max_length=30, primary_key=True)
    apelido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    #Relaciones
    jefeCarrera = models.OneToOneField(Carrera)

class Alumno(models.Model):
    rut = models.CharField(max_length=30, primary_key=True)
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
    solicitud = models.ManyToManyField(Alumno, through='Solicitud')

class Ramo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    #Relaciones
    profesor = models.ForeignKey(Profesor)
    estudiantes = models.ManyToManyField(Alumno)

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)

    #Relaciones
    ramos = models.ManyToManyField(Ramo)
    jefeCarrera = models.OneToOneField(Profesor)

class Promocion(models.Model):
    #Relaciones
    ano = models.ForeignKey(Ano)

class Ano(models.Model):
    ano = models.IntegerField(primary_key=True)
    #Relaciones

class Asignatura(models.Model):
    seccion = models.IntegerField()
    periodo =  models.IntegerField()

    #Relaciones
    carrera = models.ForeignKey(Carrera)
    alumnos = models.ManyToManyField(Alumno, through='Prueba')

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
