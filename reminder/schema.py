import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from reminder.models import Reminder


from reminder.models import Reminder
from accounts.schema import UserType

class ReminderType(DjangoObjectType):
    class Meta:
        model = Reminder


class Query(graphene.ObjectType):
    all_reminders = graphene.List(ReminderType, description="All the Reminder present")
    reminder = graphene.Field(ReminderType, id=graphene.Int(), name=graphene.String(), description="Single reminder")

    user_reminders = graphene.List(ReminderType, description="Get reminders created for the current user")

    def resolve_user_reminders(self, info, **kwargs):
        user = info.context.user or None
        
        if user.is_anonymous:
            raise GraphQLError("Anonymous users don't have reminders")
        # FIXME: Handle when reminder is empty for users (Maybe maybe not)
        return Reminder.objects.filter(owner=user)

    def resolve_all_reminders(self, info, **kwargs):
        return Reminder.objects.all()
    
    def resolve_reminder(self, info, id=None, name=None):
        if id is not None:
            return Reminder.objects.get(pk=id)
        if name is not None:
            return Reminder.objects.filter(name=name).first()

class CreateReminder(graphene.Mutation):
    id = graphene.Int()
    owner = graphene.Field(UserType)
    name = graphene.String()

    class Arguments:
        name = graphene.String()
    
    def mutate(self, info, name):
        user = info.context.user or None
        reminder = Reminder(name=name, owner=user)
        reminder.save()

        return CreateReminder(
            id=reminder.id,
            owner=reminder.owner,
            name=reminder.name
        )
    

class Mutation(graphene.ObjectType):
    create_reminder = CreateReminder.Field()