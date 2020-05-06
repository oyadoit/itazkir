import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from subscription.models import Subscription

from accounts.schema import UserType
from reminder.schema import ReminderType
from content.schema import ContentType

from reminder.models import Reminder
from content.models import Content



class SubscriptionType(DjangoObjectType):

    class Meta:
        model = Subscription
    

class Query(graphene.ObjectType):
    user_subscriptions = graphene.List(
        SubscriptionType, description="Get all the subscriptions for a given user"
    )

    user_contents = graphene.List(ContentType, description="Get subscription content for a user")

    def resolve_user_subscriptions(self, info, **kwargs):
        user = info.context.user or None
        # import pdb; pdb.set_trace()
        if user.is_anonymous:
            raise GraphQLError("Anonymous users don't have subscriptions")
        return Subscription.objects.filter(user=user)
    
    def resolve_user_contents(self, info, **kwargs):
        # TODO: Optimize this resolver. This is temporary to unblock the frontend
        user = info.context.user or None
        if user.is_anonymous:
            raise GraphQLError("Anonymouse users don't have subscribed content")

        user_subscriptions = Subscription.objects.filter(user=user)
        
        contents = []
        for subscription in user_subscriptions:
            contents.extend(Content.objects.filter(reminder=subscription.reminder))
        return contents


        
        


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