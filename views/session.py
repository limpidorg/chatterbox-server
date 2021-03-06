from Global import API
import core.notifications
from utils import returnMessage, parseData
import secrets
import core.session
import core.chat
import core.db2json
from flask import request
import core.match
import integrations.discordbot

ACTIVE_CLIENTS = []


@API.on("connect")
def connect():
    print("A new client is now connected.")
    ACTIVE_CLIENTS.append(request.sid)


@API.on("disconnect")
def disconnect():
    print("A client has disconnected.")
    ACTIVE_CLIENTS.remove(request.sid)
    session = core.session.getSessionBySocketId(request.sid)
    if session:
        print("removed socketId", request.sid, "from session", session.sessionId)
        session.socketIds.remove(request.sid)
        session.save()
        if len(session.socketIds) == 0:
            # Notify Online
            print("notifyOffline", session.sessionId)
            core.chat.notifyOffline(session.sessionId)


@API.on("resume-session")
@parseData
def resumeSession(sessionId):  # Client init - using previous identity
    print(f"Client init with sessionId: {sessionId}, attempting to resume session")
    session = core.session.getSession(sessionId)
    if sessionId and session:
        if request.sid not in session.socketIds:
            session.socketIds.append(request.sid)
        session.save()
        print(f"Added {request.sid} to {sessionId}. {session.socketIds}")
        return returnMessage(
            0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId))
        )
    else:
        print(f"Session {sessionId} not found")
        return returnMessage(-1, message="Session not found")


@API.on("destroy-session")
@parseData
def destroySession(sessionId):
    session = core.session.getSession(sessionId)
    if session:
        socketIds = session.socketIds
        if core.session.deleteSession(sessionId):
            core.match.removeFromQueue(sessionId)
            core.notifications.sendNotificationToSocketIds(socketIds, "session-destroyed")
            chat = core.chat.getChatBySessionId(sessionId)
            if chat:
                chatId = chat.chatId
                core.chat.deleteChat(chatId)
                for _sessionId in chat.sessionIds:
                    core.notifications.sendNotificationToSession(
                        _sessionId, "chat-destroyed", returnMessage(0, sessionId=sessionId, chatId=chatId)
                    )
            return returnMessage(0, message="Session destroyed")
    return returnMessage(-1, message="Session could not be destroyed")


@API.on("new-session")
@parseData
def newSession(discordId=None, name="Anonymous"):  # Client init - get a new identity
    print("Creating a new session")
    print("Username session: ", name)
    sessionId = core.session.newSession(request.sid, discordId=discordId, name=name)
    print(f"New sessionId: {sessionId}")
    return returnMessage(0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId)))


@API.on("discord-verification")
@parseData
def discordVerification(discordId):
    try:
        joined = integrations.discordbot.discordVerification(discordId)
    except Exception as e:
        print(e)
        return returnMessage(-1, message="Timed out.")

    if joined:
        return returnMessage(0, message="Discord verification successful")
    return returnMessage(-1, message="Not joined.")


@API.on("get-username")
@parseData
def getUsername(selfSessionId):
    chat = core.chat.getChatBySessionId(selfSessionId)

    for sessionId in chat.sessionIds:
        if sessionId == selfSessionId:
            continue

        sessionOtherUser = core.session.getSession(sessionId)
        return returnMessage(0, username=sessionOtherUser.name)
