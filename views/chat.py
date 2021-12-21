from Global import API
from flask import request
from utils import returnMessage, parseData
import core.match
import threading
import time
import core.session
import core.notifications
import core.chat
import core.db2json
import core.filter


@API.on("new-chat-request")
@parseData
def newChatRequest(sessionId):
    print(f'New chat request from {sessionId} (matching)')
    core.match.findMatchFor(sessionId)
    return returnMessage(0, message='New chat request received')


@API.on("cancel-chat-request")
@parseData
def newChatRequest(sessionId):
    print(f'Cancel chat request from {sessionId} (matching)')
    core.match.removeFromQueue(sessionId)
    # Notify the cancellation
    core.notifications.sendNotificationToSession(
        sessionId, 'chat-request-cancelled', returnMessage(0, message='Chat request cancelled'))
    return returnMessage(0, message='Cancellation received')


@API.on('join-chat')
@parseData
def joinChat(sessionId, chatId):
    print(f'Join chat {chatId}: {sessionId}')
    # Permission check
    chat = core.chat.getChat(chatId)
    if chat:
        if sessionId not in chat.sessionIds:
            return returnMessage(-1, message='You are not a member of this conversation.')
        # Can join the chat
        messages = []
        for message in chat.conversations:
            messages.append(core.db2json.Conversation(message))
        core.notifications.sendNotificationToSession(
            sessionId, 'chat-joined', returnMessage(0, sessionId=sessionId, chatId=chatId))
        
        session = core.session.getSession(sessionId)
        if session:
            if len(session.socketIds) == 1: # Just joined the chat 
                print('notifyOnline', session.sessionId)
                core.chat.notifyOnline(sessionId)

        return returnMessage(0, conversations=messages)
    else:
        return returnMessage(-1, message='Chat not found')


@API.on('send-message')
@parseData
def sendMessage(sessionId, chatId, message):
    print(f'Send message {message} to {chatId}')
    chat = core.chat.getChat(chatId)
    if chat:
        if sessionId not in chat.sessionIds:
            return returnMessage(-1, message='You are not a member of this conversation.')

        if not core.filter.messageValidation(sessionId, chatId, message, request.sid):
            return returnMessage(1, message='The message has been filtered.')

        # Can send the message
        conversation = core.chat.addConversation(sessionId, chatId, message)
        if conversation:
            for sessionId in chat.sessionIds:
                core.notifications.sendNotificationToSession(
                    sessionId, 'new-message', returnMessage(0, sessionId=sessionId, chatId=chatId, message=core.db2json.Conversation(conversation)))
            return returnMessage(0, message='Message sent')
        else:
            returnMessage(-1, message='Could not add message to chat')
    else:
        return returnMessage(-1, message='Chat not found')


@API.on('leave-chat')
@parseData
def leaveChat(sessionId, chatId):
    print(f'Leave chat {chatId}: {sessionId}')
    # Permission check
    chat = core.chat.getChat(chatId)
    if chat:
        if sessionId not in chat.sessionIds:
            return returnMessage(-1, message='You are not a member of this conversation.')
        if core.chat.deleteChat(chatId):
            for _sessionId in chat.sessionIds:
                core.notifications.sendNotificationToSession(
                    _sessionId, 'chat-destroyed', returnMessage(0, sessionId=sessionId, chatId=chatId))
            return returnMessage(0)
        else:
            return returnMessage(-1, message='Failed to leave the chat.')
    else:
        return returnMessage(-1, message='Chat not found')
