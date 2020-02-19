import graphene
from graphene_django import DjangoObjectType
from reminder.models import Reminder


from reminder.models import Reminder

class ReminderType(DjangoObjectType):
    class Meta:
        model = Reminder


class Query(graphene.ObjectType):
    all_reminders = graphene.List(ReminderType, description="All the Reminder present")
    reminder = graphene.Field(ReminderType, id=graphene.Int(), name=graphene.String(), description="Single reminder")

    # user_reminders = graphene.List(ReminderType, owner=)
    # user_reminder = graphene.Field(ReminderType, id=graphene.Int(), )

    def resolve_all_reminders(self, info, **kwargs):
        return Reminder.objects.all()
    
    def resolve_reminder(self, info, id=None):
        if id is not None:
            return Reminder.objects.get(pk=id)
