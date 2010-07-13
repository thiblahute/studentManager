from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection, Entry, reverse
from django_restapi.responder import *
from django_restapi_tests.polls.models import Poll, Choice

# JSON Test API URLs
#
# Polls are available at /json/polls/ and 
# /json/polls/[poll_id]/.
#
# Different (manual) URL structure for choices:
# /json/polls/[poll_id]/choices/[number of choice]/
# Example: /json/polls/121/choices/2/ identifies the second 
# choice for the poll with ID 121.

class ChoiceCollection(Collection):
    
    def read(self, request):
        poll_id = int(request.path.split("/")[3])
        filtered_set = self.queryset._clone()
        filtered_set = filtered_set.filter(poll__id=poll_id)
        return self.responder.list(request, filtered_set)
    
    def get_entry(self, poll_id, choice_num):
        poll = Poll.objects.get(id=int(poll_id))
        choice = poll.get_choice_from_num(int(choice_num))
        return ChoiceEntry(self, choice)

    def get_url(self):
        return reverse(self, (), {'poll_id':self.model.poll.id})

class ChoiceEntry(Entry):
    
    def get_url(self):
        choice_num = self.model.get_num()
        return reverse(self.collection, (), {'poll_id':self.model.poll.id, 'choice_num':choice_num})

json_poll_resource = Collection(
    queryset = Poll.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id', 'question', 'pub_date'),
    responder = JSONResponder(paginate_by=10)
)

json_choice_resource = ChoiceCollection(
    queryset = Choice.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
    expose_fields = ('id', 'poll_id', 'choice', 'votes'),
    responder = JSONResponder(paginate_by=5),
    entry_class = ChoiceEntry
)

urlpatterns = patterns('',
   url(r'^json/polls/(?P<poll_id>\d+)/choices/(?P<choice_num>\d+)/$', json_choice_resource, {'is_entry':True}),
   url(r'^json/polls/(?P<poll_id>\d+)/choices/$', json_choice_resource, {'is_entry':False}),
   url(r'^json/polls/(.*?)/?$', json_poll_resource)
)
