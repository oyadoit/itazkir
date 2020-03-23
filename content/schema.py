import graphene
from graphene_django import DjangoObjectType
from content.models import Content
from graphql import GraphQLError


from reminder.models import Reminder
from reminder.schema import ReminderType

class ContentType(DjangoObjectType):
    class Meta:
        model = Content


class Query(graphene.ObjectType):
    all_contents = graphene.List(ContentType, description="All contents available")
    content = graphene.Field(ContentType, id=graphene.Int(), title=graphene.String(), description="The content for a given id")
    reminder_content = graphene.List(ContentType, reminder_id=graphene.Int(), description="The contents for a given reminder")

    def resolve_all_contents(self, info, **kwargs):
        return Content.objects.all()
    
    def resolve_reminder_content(self, info, reminder_id=None):
        if reminder_id is not None:
            reminder = Reminder.objects.filter(id=reminder_id).first()
            return Content.objects.filter(reminder=reminder)
    
    def resolve_content(self, info, id=None, title=None):
        if id is not None:
            return Content.objects.get(pk=id)
        if title is not None:
            return Content.objects.filter(title=title).first()


class CreateContent(graphene.Mutation):
    id = graphene.Int()
    data = graphene.String()
    title = graphene.String()
    reminder = graphene.Field(ReminderType)

    class Arguments:
        reminder_id = graphene.Int()
        data = graphene.String()
        title = graphene.String()
    
    def mutate(self, info, reminder_id, data, title):
        reminder = Reminder.objects.get(pk=reminder_id)
        if not reminder:
            raise Exception('Invalid Reminder')
        content = Content(reminder=reminder, data=data, title=title)
        content.save()

        return CreateContent(
            id=content.id,
            data=content.data,
            title=title,
            reminder=content.reminder
        )


class Mutation(graphene.ObjectType):
    create_content = CreateContent.Field()
