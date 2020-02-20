import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

import accounts.schema
import reminder.schema


class Query(accounts.schema.Query, reminder.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")

class Mutation(accounts.schema.Mutation, reminder.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)