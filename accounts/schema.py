import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from accounts.models import User
from reminder.models import Reminder


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)
    is_creator = graphene.Boolean()

    def resolve_is_creator(self, info):
        reminder = Reminder.objects.filter(owner=self).first()
        return True if reminder else False


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, first_name, last_name, password, email, phone=None):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    current_user = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()
    
    def resolve_current_user(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not logged in')
        return user

    


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
