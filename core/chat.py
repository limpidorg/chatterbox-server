from database import Session, Chat

def getChat(chatId):
    try:
        chat = Chat.objects(chatId=chatId).first()
        return chat
    except:
        return None

def getChatBySessionId(sessionId):
    try:
        chat = Chat.objects(sessionId=sessionId).first()
        return chat
    except:
        return None