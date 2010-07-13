from django.db import models
from django.http import Http404

class Person(models.Model):
    name = models.CharField(max_length=20)
    friends = models.ManyToManyField('self')
    idols = models.ManyToManyField('self', symmetrical=False, related_name='stalkers')

    def __unicode__(self):
        return self.name

def get_friendship_list():
    people = Person.objects.filter(friends__isnull=False)
    friendships = []
    for person in people:
        for friend in person.friends.all():
            friendship = [person, friend]
            friendship.sort(cmp=lambda x, y: cmp(x.name, y.name))
            if friendship not in friendships:
                friendships.append(friendship)
    friendships.sort(cmp=lambda x, y: cmp(x[0].name, y[0].name))
    return friendships

def get_friendship(person_id, friend_id):
    person = Person.objects.get(id=person_id)
    try:
        friend = person.friends.get(id=friend_id)
    except Person.DoesNotExist:
        raise Http404
    friendship = [person, friend]
    friendship.sort(cmp=lambda x,y: cmp(x.name, y.name))
    return friendship