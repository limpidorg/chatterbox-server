from mongoengine import connect, Document, StringField, FloatField, BooleanField, ListField

class Session(Document):  # Basically userId
    sessionId = StringField(required=True, unique=True)
    discordId = StringField(defalt=None)
    created = FloatField(required=True)
    activeChats = ListField(StringField(), default=[])
    nickName = StringField(default='Anonymous')

class Chat(Document):
    chatId = StringField(required=True, unique=True)
    chatKey = StringField(required=True)
    sessionIds = StringField(required=True)

connect('chatterbox')
