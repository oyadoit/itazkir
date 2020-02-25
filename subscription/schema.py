import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from subscription.models import Subscription

from accounts.schema import UserType
from reminder.schema import ReminderType

from reminder.models import Reminder



class SubscriptionType(DjangoObjectType):

    class Meta:
        model = Subscription
    

class Query(graphene.ObjectType):
    user_subscriptions = graphene.List(
        SubscriptionType, description="Get all the subscriptions for a given user"
    )

    def resolve_user_subscription(self, info, **kwargs):
        user = info.context.user or None
        if user.is_anonymous:
            raise GraphQLError("Anonymous users don't have subscriptions")
        return Subscription.objects.filter(user=user)


class CreateSubscription(graphene.Mutation):
    id = graphene.Int()
    user = graphene.Field(UserType)
    reminder = graphene.Field(ReminderType)

    class Arguments:
        reminder_id = graphene.Int()
    
    def mutate(self, info, reminder_id):
        user = info.context.user or None
        reminder = Reminder.objects.get(pk=reminder_id)
        if not reminder:
            raise Exception("invalid Reminder")
        subscription = Subscription(reminder=reminder, user=user)
        subscription.save()

        return CreateSubscription(
            id=subscription.id,
            user= subscription.user,
            reminder=subscription.reminder
        )



class Mutation(graphene.ObjectType):
    create_subscription = CreateSubscription.Field()