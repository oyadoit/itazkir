import graphene
from graphene_django import DjangoObjectType
from content.models import Content
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

import cloudinary
import cloudinary.uploader
import cloudinary.api


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
    file_location = graphene.String()
    reminder = graphene.Field(ReminderType)

    class Arguments:
        reminder_id = graphene.Int()
        data = graphene.String()
        title = graphene.String()
        file = Upload()

    def mutate(self, info, **kwargs):
        reminder_id = kwargs.get('reminder_id')
        data = kwargs.get('data')
        title = kwargs.get('title')
        file = kwargs.get('file')
        reminder = Reminder.objects.get(pk=reminder_id)
        if not reminder:
            raise Exception('Invalid Reminder')
        content = Content(reminder=reminder, data=data, title=title)
        if file:
            upload_response = cloudinary.uploader.upload(file)
            content.content_image = upload_response.get('secure_url')

        content.save()

        return CreateContent(
            id=content.id,
            data=content.data,
            title=title,
            reminder=content.reminder,
            file_location=content.content_image
        )


class Mutation(graphene.ObjectType):
    create_content = CreateContent.Field()
