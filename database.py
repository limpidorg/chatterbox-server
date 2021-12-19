from mongoengine import connect, Document, StringField, FloatField, BooleanField, ListField


class Session(Document):  # Basically userId
    sessionId = StringField(required=True, unique=True)
    discordId = StringField(defalt=None)
    created = FloatField(required=True)
    chatId = StringField(default=None)
    nickName = StringField(default='Anonymous')
    socketIds = ListField(StringField(), default=[])

class Chat(Document):
    chatId = StringField(required=True, unique=True)
    # chatKey = StringField(required=True)
    sessionIds = ListField(StringField(), required=True)


connect('chatterbox')
