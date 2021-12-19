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


@API.on('connect')
def connect():
    print('A new client is now connected.')
    ACTIVE_CLIENTS.append(request.sid)


@API.on('disconnect')
def disconnect():
    print('A client has disconnected.')
    ACTIVE_CLIENTS.remove(request.sid)
    session = core.session.getSessionBySocketId(request.sid)
    if session:
        print('removed socketId', request.sid, 'from session', session.sessionId)
        session.socketIds.remove(request.sid)
        session.save()


@API.on('resume-session')
@parseData
def resumeSession(sessionId):  # Client init - using previous identity
    print(
        f'Client init with sessionId: {sessionId}, attempting to resume session')
    session = core.session.getSession(sessionId)
    if session:
        if request.sid not in session.socketIds:
            session.socketIds.append(request.sid)
        session.save()
        print(f'Added {request.sid} to {sessionId}. {session.socketIds}')
        return returnMessage(0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId)))
    else:
        print(f'Session {sessionId} not found')
        return returnMessage(-1, message='Session not found')


@API.on('destroy-session')
@parseData
def destroySession(sessionId):
    session = core.session.getSession(sessionId)
    socketIds = session.socketIds
    if session:
        if core.session.deleteSession(sessionId):
            core.match.removeFromQueue(sessionId)
            core.notifications.sendNotificationToSocketIds(
                socketIds, 'session-destroyed')
            return returnMessage(0, message='Session destroyed')
    return returnMessage(-1, message='Session could not be destroyed')


@API.on('new-session')
@parseData
def newSession(discordId=None):  # Client init - get a new identity
    print('Creating a new session')
    sessionId = core.session.newSession(request.sid, discordId=discordId)
    print(f'New sessionId: {sessionId}')
    return returnMessage(0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId)))


@API.on('discord-verification')
@parseData
def discordVerification(discordId):
    if integrations.discordbot.discordVerification(discordId):
        return returnMessage(0, message='Discord verification successful')
    return returnMessage(-1)
