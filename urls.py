from django.conf.urls.defaults import *
from sitioPrincipal.models import Alumno, Promocion, Carrera

#Rest API imports
from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder
from django_restapi.authentication import HttpBasicAuthentication


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

login = Collection(
    queryset = Alumno.objects.all(),
    responder = XMLResponder(),
    authentication = HttpBasicAuthentication()
)

alumno_ressource = Collection(
    queryset = Alumno.objects.all(),
    responder = XMLResponder()
)

carrera_ressource = Collection(
    queryset = Carrera.objects.all(),
    responder = XMLResponder()
)

promocion_ressource = Collection(
    queryset = Promocion.objects.all(),
    responder = XMLResponder()
)

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', 'studentManager.sitioPrincipal.views.login.log'),
    (r'^accounts/login/', 'studentManager.sitioPrincipal.views.login.log'),
    (r'^logout/', 'studentManager.sitioPrincipal.views.login.logOut'),
    (r'^accounts/logout/', 'studentManager.sitioPrincipal.views.login.logOut'),
    (r'^malla/', 'studentManager.sitioPrincipal.views.malla.malla'),
    (r'^vista/', 'studentManager.sitioPrincipal.views.vista.vista'),
    (r'^menu/', 'studentManager.sitioPrincipal.views.menu.menu'),
    (r'^addStudent/', 'studentManager.sitioPrincipal.views.profesor.addStudent'),
    (r'^addPromocion/', 'studentManager.sitioPrincipal.views.profesor.addPromocion'),
    (r'^addRamo/', 'studentManager.sitioPrincipal.views.profesor.addRamo'),
    (r'^addAsignatura/', 'studentManager.sitioPrincipal.views.profesor.addAsignatura'),
    (r'^addAlumnoAsignatura/', 'studentManager.sitioPrincipal.views.profesor.addAlumnoAsignatura'),
    (r'^addAlumnoPassed/', 'studentManager.sitioPrincipal.views.profesor.addAlumnoPassed'),
    (r'^viewStudents/', 'studentManager.sitioPrincipal.views.profesor.viewStudents'),
    (r'^xml/alumno/(.*?)/?$', alumno_ressource),
    (r'^xml/carrera/(.*?)/?$', carrera_ressource),
    (r'^xml/promocion/(.*?)/?$', promocion_ressource),
    (r'^xml/login/(.*?)/?$', login),
)
