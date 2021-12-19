from Global import API
from utils import returnMessage, parseData
import secrets
import core.session
import core.chat
import core.db2json
from flask import request

ACTIVE_CLIENTS = []


@API.on('connect')
def connect():
    print('A new client is now connected.')
    ACTIVE_CLIENTS.append(request.sid)


@API.on('disconnect')
def disconnect():
    print('A client has disconnected.')
    ACTIVE_CLIENTS.remove(request.sid)


@API.on('resume-session')
@parseData
def resumeSession(sessionId):  # Client init - using previous identity
    print(
        f'Client init with sessionId: {sessionId}, attempting to resume session')
    session = core.session.getSession(sessionId)
    if session:
        print(f'Session {sessionId} resumed')
        session.socketId = request.sid
        session.save()
        return returnMessage(0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId)))
    else:
        print(f'Session {sessionId} not found')
        return returnMessage(-1, message='Session not found')


@API.on('destroy-session')
@parseData
def destroySession(sessionId):
    if core.session.deleteSession(sessionId):
        return returnMessage(0, message='Session destroyed')
    return returnMessaFge(-1, message='Session could not be destroyed')


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
    print(f'Discord verification for {discordId}')
    return returnMessage(-1)
