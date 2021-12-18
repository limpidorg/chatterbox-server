from database import Session
import secrets
import time

def newSession(discordId = None):
    sessionId = secrets.token_hex(16)
    session = Session(sessionId=sessionId, discordId=discordId, created = time.time())
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