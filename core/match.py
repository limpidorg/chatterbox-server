import core.notifications
import core.chat

Queue = []


def findMatchFor(sessionId):
    if sessionId not in Queue:
        Queue.append(sessionId)
    for i in Queue:
        if i != sessionId:
            # New chat
            chatId = core.chat.newChat([sessionId, i])
            if chatId:
                Queue.remove(i)
                Queue.remove(sessionId)
                core.chat.initiateChat(chatId)

def removeFromQueue(sessionId):
    if sessionId in Queue:
        Queue.remove(sessionId)
