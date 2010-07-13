from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

class Poll(models.Model):
    question = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    pub_date = models.DateTimeField(_('date published'), default=datetime.now)
    class Admin:
        pass
    def __str__(self):
        return self.question
    def get_choice_list(self):
        return list(self.choice_set.order_by('id'))
    def get_choice_from_num(self, choice_num):
        try:
            return self.get_choice_list()[int(choice_num)-1]
        except IndexError:
            raise Choice.DoesNotExist

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    class Admin:
        pass
    def __str__(self):
        return self.choice
    def get_num(self):
        try:
            return self.poll.get_choice_list().index(self)+1
        except ValueError:
            raise Choice.DoesNotExist