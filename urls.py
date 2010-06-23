from django.conf.urls.defaults import *
from sitioPrincipal.models import Alumno, Promocion, Carrera

#Rest API imports
from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder
from django_restapi.authentication import *
from django_restapi_tests.polls.models import Poll


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
    # Example:
    # (r'^studentManager/', include('studentManager.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^login/', 'studentManager.sitioPrincipal.views.Login'),
    (r'^malla/', 'studentManager.sitioPrincipal.views.Malla'),
    (r'^vista/', 'studentManager.sitioPrincipal.views.Vista'),
    (r'^xml/alumno/(.*?)/?$', alumno_ressource),
    (r'^xml/carrera/(.*?)/?$', carrera_ressource),
    (r'^xml/promocion/(.*?)/?$', promocion_ressource),
    (r'^xml/login/(.*?)/?$', login),

)
