from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi.receiver import *
from django_restapi_tests.polls.models import Poll

fullxml_poll_resource = Collection(
    queryset = Poll.objects.all(), 
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    receiver = XMLReceiver(),
    responder = XMLResponder(),
)
fulljson_poll_resource = Collection(
    queryset = Poll.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    receiver = JSONReceiver(),
    responder = JSONResponder()
)

urlpatterns = patterns('',
   url(r'^fullxml/polls/(.*?)/?$', fullxml_poll_resource),
   url(r'^fulljson/polls/(.*?)/?$', fulljson_poll_resource)
)
