import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User



class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, first_name, last_name, password, email, phone):
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

    def resolve_users(self, info):
        return get_user_model().objects.all()
    


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()