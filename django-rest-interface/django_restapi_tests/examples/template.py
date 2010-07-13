from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi_tests.polls.models import Poll, Choice

template_poll_resource = Collection(
    queryset = Poll.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id', 'question', 'pub_date'),
    responder = TemplateResponder(
        template_dir = 'polls',
        template_object_name = 'poll',
        paginate_by = 10
    )
)

template_choice_resource = Collection(
    queryset = Choice.objects.all(),
    permitted_methods = ('GET',),
    expose_fields = ('id', 'poll_id', 'choice', 'votes'),
    responder = TemplateResponder(
        template_dir = 'polls',
        template_object_name = 'choice',
        paginate_by = 5
    )
)

urlpatterns = patterns('',
   url(r'^html/polls/creator/$', template_poll_resource.responder.create_form),
   url(r'^html/polls/(?P<pk>\d+)/editor/$', template_poll_resource.responder.update_form),
   url(r'^html/polls/(.*?)/?$', template_poll_resource),
   url(r'^html/choices/(.*?)/?$', template_choice_resource),
)
