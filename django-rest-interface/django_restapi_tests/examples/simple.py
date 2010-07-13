from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi_tests.polls.models import Poll, Choice

simple_poll_resource = Collection(
    queryset = Poll.objects.all(), 
    responder = XMLResponder(),
)
simple_choice_resource = Collection(
    queryset = Choice.objects.all(),
    responder = XMLResponder()
)

urlpatterns = patterns('',
   url(r'^api/poll/(.*?)/?$', simple_poll_resource),
   url(r'^api/choice/(.*?)/?$', simple_choice_resource)
)
