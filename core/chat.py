from database import Session, Chat
import secrets
import core.notifications
import core.session
from integrations.discordbot import getDiscordId, sendMessage
from utils import returnMessage


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


def newChat(sessionIds):
    chatId = secrets.token_hex(16)
    chat = Chat(chatId=chatId, sessionIds=sessionIds)
    try:
        chat.save()
        return chatId
    except:
        return None


def deleteChat(chatId):
    chat = getChat(chatId)
    if chat:
        for sessionId in chat.sessionIds:
            session = core.session.getSession(sessionId)
            if session:
                session.chatId = None
                session.save()
        chat.delete()
        return True
    return False


def initiateChat(chatId):
    "Initiates a chat after matching"
    chat = getChat(chatId)
    if chat:
        for sessionId in chat.sessionIds:
            session = core.session.getSession(sessionId)
            if session:
                discordId = session.discordId
                discord_internal_id = getDiscordId(discordId)

                session.chatId = chatId
                session.save()
            core.notifications.sendNotificationToSession(sessionId, "new-chat-found", returnMessage(0, chatId=chatId))

            if discord_internal_id != None:
                message = {
                    "title": "Hurry up",
                    "description": "We just found your new chatling! It could be the beginning of a great adventure 💙",
                }
                sendMessage(discord_internal_id, message)
        return True
    return False


def joinChat(sessionId, chatId):
    pass
