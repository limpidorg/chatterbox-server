from mongoengine import connect, Document, StringField, FloatField, BooleanField, ListField, EmbeddedDocument, EmbeddedDocumentListField


class Session(Document):  # Basically userId
    sessionId = StringField(required=True, unique=True)
    discordId = StringField(defalt=None)
    created = FloatField(required=True)
    chatId = StringField(default=None)
    nickName = StringField(default='Anonymous')
    socketIds = ListField(StringField(), default=[])


class Conversation(EmbeddedDocument):
    sessionId = StringField(required=True)
    message = StringField(required=True)
    timestamp = FloatField(required=True)
    conversationId = StringField(required=True)


class Chat(Document):
    chatId = StringField(required=True, unique=True)
    sessionIds = ListField(StringField(), required=True)
    conversations = EmbeddedDocumentListField(Conversation, default=[])


connect('chatterbox')
