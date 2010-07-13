from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi_tests.polls.models import Poll, Choice

fixedend_poll_resource = Collection(
    queryset = Poll.objects.all(), 
    responder = XMLResponder(),
)
fixedend_choice_resource = Collection(
    queryset = Choice.objects.all(),
    responder = XMLResponder()
)

urlpatterns = patterns('',
   url(r'^polls/xml/$', fixedend_poll_resource),
   url(r'^polls/(.*)/xml/$', fixedend_poll_resource),
   url(r'^choices/xml/$', fixedend_choice_resource),
   url(r'^choices/(.*)/xml/$', fixedend_choice_resource)
)
