from database import Session
import secrets
import time


def newSession(socketId, discordId=None):
    sessionId = secrets.token_hex(16)
    session = Session(socketId=socketId, sessionId=sessionId,
                      discordId=discordId, created=time.time())
    try:
        session.save()
        return sessionId
    except:
        return None


def getSession(sessionId):
    try:
        session = Session.objects(sessionId=sessionId).first()
        return session
    except:
        return None


def deleteSession(sessionId):
    try:
        session = getSession(sessionId)
        if session:
            session.delete()
            return True
        return False
    except:
        return False


def getSessionBySocketId(socketId):
    try:
        session = Session.objects(socketId=socketId).first()
        return session
    except:
        return None
