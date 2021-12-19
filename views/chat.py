from Global import API
from flask import request
from utils import returnMessage, parseData
import threading
import time
import core.session


@API.on("new-chat-request")
@parseData
def newChatRequest(sessionId):
    print(f'New chat request from {sessionId} (matching)')
    threading.Thread(target=matching, args=(sessionId,)).start()
    return returnMessage(0, chatId="test")


def matching(sessionId):
    time.sleep(5)
    socketId = core.session.getSession(sessionId).socketId
    print('Matched')
    API.emit("new-chat-found", returnMessage(0,
             chatId='sampleChatId'), to=socketId)
