from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from django_restapi.authentication import *
from django_restapi_tests.polls.models import Poll

# HTTP Basic
#
# No auth function specified
# -> django.contrib.auth.models.User is used.
# Test with username 'rest', password 'rest'.

basicauth_poll_resource = Collection(
    queryset = Poll.objects.all(), 
    responder = XMLResponder(),
    authentication = HttpBasicAuthentication()
)

# HTTP Digest

def digest_authfunc(username, realm):
    """
    Exemplary authfunc for HTTP Digest. In production situations,
    the combined hashes of realm, username and password are usually
    stored in an external file/db.
    """
    hashes = {
        ('realm1', 'john') : '3014aff1d0d0f0038e23c1195301def3', # Password: johnspass
        ('realm2', 'jim') : '5bae77fe607e161b831c8f8026a2ceb2'   # Password: jimspass
    }
    return hashes[(username, realm)]

digestauth_poll_resource = Collection(
    queryset = Poll.objects.all(),
    responder = XMLResponder(),
    authentication = HttpDigestAuthentication(digest_authfunc, 'realm1')
)

urlpatterns = patterns('',
   url(r'^basic/polls/(.*?)/?$', basicauth_poll_resource),
   url(r'^digest/polls/(.*?)/?$', digestauth_poll_resource)
)