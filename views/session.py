from Global import API
from utils import returnMessage, parseData
import secrets
import core.session
import core.db2json


@API.on('connect')
def connect():
    print('A new client is now connected.')


@API.on('session')
@parseData
def connect(sessionId, discordId=None):  # Client init - get a new identity
    needSession = True
    if sessionId:
        print(
            f'Client init with sessionId: {sessionId}, attempting to resume session')
        session = core.session.getSession(sessionId)
        if session:
            print(f'Session {sessionId} resumed')
            needSession = False
        else:
            print(f'Session {sessionId} not found')

    if needSession:
        print('Creating a new session')
        sessionId = core.session.newSession(discordId=discordId)
        print(f'New sessionId: {sessionId}')

    return returnMessage(0, sessionId=sessionId, sessionInfo=core.db2json.Session(core.session.getSession(sessionId)))


@API.on('discord-verification')
@parseData
def discordVerification(discordId):
    print(f'Discord verification for {discordId}')
    return returnMessage(0, hasJoinedDiscord=True)
