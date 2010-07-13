from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi_tests.polls.models import Poll, Choice

xml_poll_resource = Collection(
    queryset = Poll.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id', 'question', 'pub_date'),
    responder = XMLResponder(paginate_by = 10)
)

xml_choice_resource = Collection(
    queryset = Choice.objects.all(),
    permitted_methods = ('GET',),
    expose_fields = ('id', 'poll_id', 'choice'),
    responder = XMLResponder(paginate_by = 5)
)

urlpatterns = patterns('',
   url(r'^xml/polls/(.*?)/?$', xml_poll_resource),
   url(r'^xml/choices/(.*?)/?$', xml_choice_resource)
)

