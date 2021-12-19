def Session(Session):
    'For the sake of security & privacy, we would like to manually limit what information should be sent through'
    return {
        'sessionId': Session.sessionId,
        'created': Session.created,
        'chatId': Session.chatId,
        'name': Session.name,
    }

def Conversation(Conversation):
    return {
        'sessionId': Conversation.sessionId,
        'message': Conversation.message,
        'timestamp': Conversation.timestamp,
        'messageId': Conversation.messageId,
    }