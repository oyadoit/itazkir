import graphene
from graphene_django import DjangoObjectType
from reminder.models import Reminder


from reminder.models import Reminder

class ReminderType(DjangoObjectType):
    class Meta:
        model = Reminder


