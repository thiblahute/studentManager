from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi_tests.people.models import *

# Urls for a resource that does not map 1:1 
# to Django models.

class FriendshipCollection(Resource):
    def read(self, request):
        friendships = get_friendship_list()
        context = {'friendships':friendships}
        return render_to_response('people/friends_list.html', context)

class FriendshipEntry(Resource):
    def read(self, request, person_id, friend_id):
        friendship = get_friendship(person_id, friend_id)
        context = {'friendship':friendship}
        return render_to_response('people/friends_detail.html', context)
    def delete(self, request, person_id, friend_id):
        friendship = get_friendship(person_id, friend_id)
        friendship[0].friends.remove(friendship[1])
        return HttpResponseRedirect('/friends/')

urlpatterns = patterns('',
   url(r'^friends/$', FriendshipCollection()),
   url(r'^friends/(?P<person_id>\d+)-(?P<friend_id>\d+)/$', FriendshipEntry(permitted_methods=('GET','DELETE'))),
)