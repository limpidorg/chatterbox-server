import core.session
from Global import API
import threading


def sendNotificationToSocketId(socketId, *args, **kw):
    API.emit(*args, **kw, to=socketId)


def sendNotificationToSocketIds(socketIds, *args, **kw):
    print('sendNotificationToSocketIds', socketIds, args, kw)
    # def sendNotification(*args, **kw):
    for socketId in socketIds:
        API.emit(*args, **kw, to=socketId)
    # threading.Thread(target=sendNotification, args=args, kwargs=kw).start()

def sendNotificationToSession(sessionId, *args, **kw):
    session = core.session.getSession(sessionId)
    if session:
        sendNotificationToSocketIds(session.socketIds, *args, **kw)
